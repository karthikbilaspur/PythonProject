"""
MailForge Pro — upgraded single-operator Streamlit email scheduler.

Highlights:
- SQLite/PostgreSQL support with per-operation connections and schema migration.
- UTC timestamps internally, configurable display/scheduling timezone (APP_TIMEZONE).
- Atomic job claiming, bounded retries, stale-claim recovery, and separate worker mode.
- Scheduled attachment bytes persisted and reloaded for delivery.
- Secrets read from environment / Streamlit secrets; credentials are never stored in the DB.
- Input validation, attachment/recipient limits, improved logging, and optional access gate.
- Run UI:     streamlit run mailforge.py
- Run worker: python mailforge.py --worker
  Run the worker as a persistent service/process. Streamlit Cloud app sleep/restarts
  are not a reliable background scheduler.
"""

from __future__ import annotations

import base64
import email.utils
import importlib
import json
import logging
import os
import re
import smtplib
import ssl
import sys
import time
import uuid
from datetime import date, datetime, time as dt_time, timedelta, timezone
from email.message import EmailMessage
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import streamlit as st

APP_NAME = "MailForge Pro"
DB_URL = os.getenv("DATABASE_URL") or None
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
MAX_ATTACHMENT_MB = int(os.getenv("MAX_ATTACHMENT_MB", "10"))
MAX_TOTAL_ATTACHMENT_MB = int(os.getenv("MAX_TOTAL_ATTACHMENT_MB", "20"))
MAX_RECIPIENTS = int(os.getenv("MAX_RECIPIENTS", "50"))
MAX_RETRIES = int(os.getenv("MAX_EMAIL_RETRIES", "3"))
WORKER_POLL_SECONDS = max(10, int(os.getenv("WORKER_POLL_SECONDS", "30")))
DB_PATH = os.getenv("MAILFORGE_DB_PATH", "mailforge.db")
LOG = logging.getLogger("mailforge")
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


def secret_value(name: str, default: str = "") -> str:
    """Read a secret from environment first, then Streamlit secrets."""
    value = os.getenv(name)
    if value:
        return value
    try:
        value = st.secrets.get(name, default)
        return str(value) if value is not None else default
    except Exception:
        return default


def get_timezone() -> ZoneInfo:
    name = secret_value("APP_TIMEZONE", "UTC")
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError:
        LOG.warning("Unknown APP_TIMEZONE %r; using UTC", name)
        return ZoneInfo("UTC")


APP_TZ = get_timezone()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def as_utc(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        dt = value
    else:
        raw = str(value).strip()
        try:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return None
    if dt.tzinfo is None:
        # Legacy SQLite timestamps were naive local times. Interpret them in APP_TZ.
        dt = dt.replace(tzinfo=APP_TZ)
    return dt.astimezone(timezone.utc)


def local_display(value: Any) -> str:
    dt = as_utc(value)
    return dt.astimezone(APP_TZ).strftime("%Y-%m-%d %H:%M %Z") if dt else "—"


def db_connection():
    """Create a fresh connection per operation; never share SQLite connections across threads."""
    if DB_URL:
        psycopg2 = importlib.import_module("psycopg2")
        return psycopg2.connect(DB_URL, connect_timeout=10)
    import sqlite3
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout = 30000")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def sql_placeholder() -> str:
    return "%s" if DB_URL else "?"


def init_db() -> None:
    conn = db_connection()
    cur = conn.cursor()
    if DB_URL:
        statements = [
            """CREATE TABLE IF NOT EXISTS scheduled_emails (
                id BIGSERIAL PRIMARY KEY,
                to_emails TEXT NOT NULL,
                cc_emails TEXT NOT NULL DEFAULT '',
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                attachments_meta TEXT NOT NULL DEFAULT '[]',
                schedule_time TIMESTAMPTZ NOT NULL,
                repeat_type TEXT NOT NULL DEFAULT 'once',
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                last_sent TIMESTAMPTZ,
                sender_email TEXT NOT NULL,
                attempts INTEGER NOT NULL DEFAULT 0,
                last_error TEXT,
                claim_token TEXT,
                claimed_at TIMESTAMPTZ
            )""",
            """CREATE TABLE IF NOT EXISTS sent_log (
                id BIGSERIAL PRIMARY KEY,
                to_emails TEXT NOT NULL,
                subject TEXT NOT NULL,
                sent_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                status TEXT NOT NULL,
                error TEXT NOT NULL DEFAULT ''
            )""",
        ]
        for stmt in statements:
            cur.execute(stmt)
        migrations = [
            "ALTER TABLE scheduled_emails ADD COLUMN IF NOT EXISTS attachments_meta TEXT NOT NULL DEFAULT '[]'",
            "ALTER TABLE scheduled_emails ADD COLUMN IF NOT EXISTS attempts INTEGER NOT NULL DEFAULT 0",
            "ALTER TABLE scheduled_emails ADD COLUMN IF NOT EXISTS last_error TEXT",
            "ALTER TABLE scheduled_emails ADD COLUMN IF NOT EXISTS claim_token TEXT",
            "ALTER TABLE scheduled_emails ADD COLUMN IF NOT EXISTS claimed_at TIMESTAMPTZ",
        ]
        for stmt in migrations:
            cur.execute(stmt)
        # Older MailForge versions created schedule_time as TEXT. Convert it to
        # TIMESTAMPTZ once, preserving legacy HH:MM entries as their next UTC occurrence.
        cur.execute("""
            SELECT data_type FROM information_schema.columns
            WHERE table_schema = current_schema()
              AND table_name = 'scheduled_emails' AND column_name = 'schedule_time'
        """)
        schedule_type_row = cur.fetchone()
        if schedule_type_row and schedule_type_row[0] in ("text", "character varying", "character"):
            cur.execute("""
                ALTER TABLE scheduled_emails
                ALTER COLUMN schedule_time TYPE TIMESTAMPTZ
                USING (
                    CASE
                      WHEN schedule_time ~ '^[0-9]{2}:[0-9]{2}$' THEN
                        CASE
                          WHEN (CURRENT_DATE + schedule_time::time) AT TIME ZONE 'UTC' <= NOW()
                            THEN (CURRENT_DATE + schedule_time::time + INTERVAL '1 day') AT TIME ZONE 'UTC'
                          ELSE (CURRENT_DATE + schedule_time::time) AT TIME ZONE 'UTC'
                        END
                      ELSE schedule_time::timestamptz
                    END
                )
            """)
    else:
        cur.execute("""CREATE TABLE IF NOT EXISTS scheduled_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            to_emails TEXT NOT NULL,
            cc_emails TEXT NOT NULL DEFAULT '',
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            attachments_meta TEXT NOT NULL DEFAULT '[]',
            schedule_time TEXT NOT NULL,
            repeat_type TEXT NOT NULL DEFAULT 'once',
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            last_sent TEXT,
            sender_email TEXT NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0,
            last_error TEXT,
            claim_token TEXT,
            claimed_at TEXT
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS sent_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            to_emails TEXT NOT NULL,
            subject TEXT NOT NULL,
            sent_at TEXT NOT NULL,
            status TEXT NOT NULL,
            error TEXT NOT NULL DEFAULT ''
        )""")
        existing = {row[1] for row in cur.execute("PRAGMA table_info(scheduled_emails)").fetchall()}
        migrations = {
            "attachments_meta": "TEXT NOT NULL DEFAULT '[]'",
            "attempts": "INTEGER NOT NULL DEFAULT 0",
            "last_error": "TEXT",
            "claim_token": "TEXT",
            "claimed_at": "TEXT",
        }
        for column, definition in migrations.items():
            if column not in existing:
                cur.execute(f"ALTER TABLE scheduled_emails ADD COLUMN {column} {definition}")
        # Normalize legacy daily/weekly HH:MM rows so the due-job query can compare
        # ISO timestamps consistently. Old naive ISO values are interpreted as APP_TZ.
        legacy = cur.execute(
            "SELECT id, schedule_time, repeat_type FROM scheduled_emails WHERE length(schedule_time)=5 AND schedule_time LIKE '__:__'"
        ).fetchall()
        now_local = datetime.now(APP_TZ)
        for row in legacy:
            try:
                hh, mm = map(int, row[1].split(':'))
                target = now_local.replace(hour=hh, minute=mm, second=0, microsecond=0)
                if target <= now_local:
                    target += timedelta(days=1)
                cur.execute(
                    "UPDATE scheduled_emails SET schedule_time=? WHERE id=?",
                    (target.astimezone(timezone.utc).isoformat(), row[0]),
                )
            except Exception:
                LOG.exception("Could not migrate legacy schedule row id=%s", row[0])
    conn.commit()
    conn.close()


def rows_as_dicts(cur: Any) -> list[dict[str, Any]]:
    rows = cur.fetchall()
    if not rows:
        return []
    if DB_URL:
        names = [d[0] for d in cur.description]
        return [dict(zip(names, row)) for row in rows]
    return [dict(row) for row in rows]


def validate_email_list(raw: str, *, dns_check: bool = False) -> tuple[list[str], list[str]]:
    values = [part.strip() for part in (raw or "").replace(";", ",").split(",") if part.strip()]
    valid: list[str] = []
    invalid: list[str] = []
    seen: set[str] = set()
    pattern = re.compile(r"^[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?(?:\.[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?)+$", re.I)
    resolver = None
    if dns_check:
        try:
            resolver = importlib.import_module("dns.resolver")
        except ImportError:
            dns_check = False
    for email in values:
        key = email.lower()
        if key in seen:
            continue
        seen.add(key)
        if len(email) > 254 or not pattern.fullmatch(email):
            invalid.append(email)
            continue
        if dns_check and resolver:
            domain = email.rsplit("@", 1)[1]
            try:
                try:
                    resolver.resolve(domain, "MX", lifetime=3)
                except Exception:
                    resolver.resolve(domain, "A", lifetime=3)
            except Exception:
                invalid.append(f"{email} (domain has no usable DNS record)")
                continue
        valid.append(email)
    return valid, invalid


def spam_score(text: str) -> tuple[int, list[str]]:
    keywords = [
        "buy now", "limited time offer", "click here", "winner", "prize",
        "urgent cash", "free money", "act now", "guaranteed income",
    ]
    low = (text or "").lower()
    hits = [word for word in keywords if word in low]
    score = min(95, len(hits) * 15 + (15 if (text or "").count("!") > 3 else 0))
    return score, hits


def read_uploads(uploaded_files: list[Any]) -> list[dict[str, Any]]:
    attachments: list[dict[str, Any]] = []
    total_bytes = 0
    per_file_limit = MAX_ATTACHMENT_MB * 1024 * 1024
    total_limit = MAX_TOTAL_ATTACHMENT_MB * 1024 * 1024
    for upload in uploaded_files or []:
        content = upload.getvalue()
        if len(content) > per_file_limit:
            raise ValueError(f"{upload.name} exceeds the {MAX_ATTACHMENT_MB} MB per-file limit.")
        total_bytes += len(content)
        if total_bytes > total_limit:
            raise ValueError(f"Total attachments exceed {MAX_TOTAL_ATTACHMENT_MB} MB.")
        attachments.append({
            "name": Path(upload.name).name,
            "content_type": getattr(upload, "type", None) or "application/octet-stream",
            "data_b64": base64.b64encode(content).decode("ascii"),
        })
    return attachments


def attachment_bytes(meta: str | list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    if isinstance(meta, str):
        try:
            items = json.loads(meta or "[]")
        except json.JSONDecodeError:
            items = []
    else:
        items = meta or []
    result: list[dict[str, Any]] = []
    for item in items:
        try:
            raw = base64.b64decode(item["data_b64"], validate=True)
            result.append({
                "name": Path(str(item.get("name", "attachment"))).name,
                "content_type": str(item.get("content_type") or "application/octet-stream"),
                "content": raw,
            })
        except Exception:
            LOG.exception("Skipping malformed attachment metadata")
    return result


def send_email_smtp(
    sender_email: str,
    sender_pass: str,
    to_emails: str,
    cc_emails: str,
    subject: str,
    body: str,
    attachments: list[dict[str, Any]] | None = None,
) -> None:
    if not sender_email or not sender_pass:
        raise ValueError("SMTP sender email and app password must be configured.")
    to_list, bad_to = validate_email_list(to_emails)
    cc_list, bad_cc = validate_email_list(cc_emails)
    if bad_to or bad_cc or not to_list:
        raise ValueError(f"Invalid recipient address(es): {bad_to + bad_cc}")
    if len(set(x.lower() for x in to_list + cc_list)) > MAX_RECIPIENTS:
        raise ValueError(f"Maximum recipients per email is {MAX_RECIPIENTS}.")
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = ", ".join(to_list)
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)
    msg["Subject"] = subject.strip()
    msg["Date"] = email.utils.formatdate(localtime=True)
    msg["Message-ID"] = email.utils.make_msgid()
    msg.set_content(body or "")
    for item in attachments or []:
        content = item["content"]
        content_type = item.get("content_type", "application/octet-stream")
        main_type, _, sub_type = content_type.partition("/")
        if not main_type or not sub_type:
            main_type, sub_type = "application", "octet-stream"
        msg.add_attachment(
            content,
            maintype=main_type,
            subtype=sub_type,
            filename=Path(item["name"]).name,
        )
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=30) as server:
        server.login(sender_email, sender_pass)
        server.send_message(msg)


def generate_ai(prompt: str, occasion: str, recipient: str, sender_name: str,
                provider: str, api_key: str) -> str:
    task = (
        f"Write a concise, polished {occasion} email. Recipient: {recipient}. "
        f"Sender: {sender_name}. Context/instructions: {prompt}. "
        "Use a professional, natural tone. Do not invent facts. Return only the email body."
    )
    if api_key and provider == "OpenAI":
        from openai import OpenAI
        client = OpenAI(api_key=api_key, timeout=30, max_retries=2)
        response = client.chat.completions.create(
            model=secret_value("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You are a careful email-writing assistant."},
                {"role": "user", "content": task},
            ],
            max_tokens=500,
        )
        return (response.choices[0].message.content or "").strip()
    if api_key and provider == "Gemini":
        genai = importlib.import_module("google.generativeai")
        genai.configure(api_key=api_key)
        model_name = secret_value("GEMINI_MODEL", "gemini-2.5-flash")
        model = genai.GenerativeModel(model_name)
        result = model.generate_content(task, request_options={"timeout": 30})
        return (getattr(result, "text", None) or "").strip()
    templates = {
        "birthday": f"Hi {recipient},\n\nHappy birthday! Wishing you a wonderful year ahead filled with happiness and success.\n\nBest,\n{sender_name}",
        "thank_you": f"Hi {recipient},\n\nThank you for your time and support. I really appreciate it.\n\nBest regards,\n{sender_name}",
        "follow_up": f"Hi {recipient},\n\nI wanted to follow up on {prompt or 'my previous message'}. Please let me know if you have any updates when convenient.\n\nBest regards,\n{sender_name}",
        "cold_outreach": f"Hi {recipient},\n\nI came across your work and wanted to introduce myself. I would welcome the opportunity to connect and see whether there may be a fit to collaborate.\n\nWould you be available for a brief conversation?\n\nBest,\n{sender_name}",
        "professional": f"Dear {recipient},\n\nI am reaching out regarding {prompt or 'our current discussion'}. Please let me know a convenient time to discuss this further.\n\nSincerely,\n{sender_name}",
    }
    return templates.get(occasion, templates["professional"])


def add_log(to_emails: str, subject: str, status: str, error: str = "") -> None:
    conn = db_connection()
    cur = conn.cursor()
    p = sql_placeholder()
    if DB_URL:
        cur.execute(
            f"INSERT INTO sent_log (to_emails, subject, sent_at, status, error) VALUES ({p},{p},{p},{p},{p})",
            (to_emails, subject, utc_now(), status, error[:4000]),
        )
    else:
        cur.execute(
            f"INSERT INTO sent_log (to_emails, subject, sent_at, status, error) VALUES ({p},{p},{p},{p},{p})",
            (to_emails, subject, utc_now().isoformat(), status, error[:4000]),
        )
    conn.commit()
    conn.close()


def create_schedule(data: dict[str, Any]) -> int:
    conn = db_connection()
    cur = conn.cursor()
    p = sql_placeholder()
    scheduled = data["schedule_time"]
    if DB_URL:
        cur.execute(
            f"""INSERT INTO scheduled_emails
            (to_emails, cc_emails, subject, body, attachments_meta, schedule_time,
             repeat_type, status, created_at, sender_email, attempts)
            VALUES ({p},{p},{p},{p},{p},{p},{p},'pending',{p},{p},0)
            RETURNING id""",
            (
                data["to"], data["cc"], data["subject"], data["body"],
                json.dumps(data["attachments"]), scheduled, data["repeat_type"],
                utc_now(), data["sender"],
            ),
        )
        row = cur.fetchone()
        job_id = row[0] if row is not None else None
    else:
        cur.execute(
            f"""INSERT INTO scheduled_emails
            (to_emails, cc_emails, subject, body, attachments_meta, schedule_time,
             repeat_type, status, created_at, sender_email, attempts)
            VALUES ({p},{p},{p},{p},{p},{p},{p},'pending',{p},{p},0)""",
            (
                data["to"], data["cc"], data["subject"], data["body"],
                json.dumps(data["attachments"]), scheduled.isoformat(), data["repeat_type"],
                utc_now().isoformat(), data["sender"],
            ),
        )
        job_id = cur.lastrowid
    if job_id is None:
        conn.rollback()
        conn.close()
        raise RuntimeError("Failed to create scheduled email")
    conn.commit()
    conn.close()
    return int(job_id)


def list_schedules(limit: int = 100) -> list[dict[str, Any]]:
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT id,to_emails,cc_emails,subject,body,attachments_meta,schedule_time,repeat_type,status,created_at,last_sent,sender_email,attempts,last_error FROM scheduled_emails ORDER BY created_at DESC LIMIT {int(limit)}"
    )
    rows = rows_as_dicts(cur)
    conn.close()
    return rows


def list_logs(limit: int = 100) -> list[dict[str, Any]]:
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM sent_log ORDER BY sent_at DESC LIMIT {int(limit)}")
    rows = rows_as_dicts(cur)
    conn.close()
    return rows


def delete_schedule(job_id: int) -> None:
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM scheduled_emails WHERE id={sql_placeholder()}", (job_id,))
    conn.commit()
    conn.close()


def recover_stale_claims() -> None:
    cutoff = utc_now() - timedelta(minutes=10)
    conn = db_connection()
    cur = conn.cursor()
    p = sql_placeholder()
    if DB_URL:
        cur.execute(
            f"""UPDATE scheduled_emails SET status='pending', claim_token=NULL, claimed_at=NULL,
                last_error=COALESCE(last_error,'') || ' [Recovered stale worker claim]'
                WHERE status='sending' AND claimed_at < {p}""",
            (cutoff,),
        )
    else:
        cur.execute(
            f"""UPDATE scheduled_emails SET status='pending', claim_token=NULL, claimed_at=NULL,
                last_error=COALESCE(last_error,'') || ' [Recovered stale worker claim]'
                WHERE status='sending' AND claimed_at < {p}""",
            (cutoff.isoformat(),),
        )
    conn.commit()
    conn.close()


def claim_due_jobs(batch_size: int = 10) -> list[dict[str, Any]]:
    """Atomically claim due jobs so concurrent workers don't process the same row."""
    now = utc_now()
    token = str(uuid.uuid4())
    conn = db_connection()
    cur = conn.cursor()
    p = sql_placeholder()
    claimed: list[dict[str, Any]] = []
    try:
        if DB_URL:
            cur.execute("BEGIN")
            cur.execute(
                f"""SELECT id FROM scheduled_emails
                    WHERE status='pending' AND schedule_time <= {p}
                    ORDER BY schedule_time
                    LIMIT {int(batch_size)} FOR UPDATE SKIP LOCKED""",
                (now,),
            )
            ids = [r[0] for r in cur.fetchall()]
            for job_id in ids:
                cur.execute(
                    f"""UPDATE scheduled_emails SET status='sending', claim_token={p},
                        claimed_at={p} WHERE id={p} AND status='pending'""",
                    (token, now, job_id),
                )
            conn.commit()
            if ids:
                cur.execute(
                    f"SELECT * FROM scheduled_emails WHERE claim_token={p} AND status='sending'",
                    (token,),
                )
                claimed = rows_as_dicts(cur)
        else:
            cur.execute("BEGIN IMMEDIATE")
            cur.execute(
                f"""SELECT id FROM scheduled_emails
                    WHERE status='pending' AND schedule_time <= {p}
                    ORDER BY schedule_time LIMIT {int(batch_size)}""",
                (now.isoformat(),),
            )
            ids = [r["id"] for r in cur.fetchall()]
            for job_id in ids:
                cur.execute(
                    f"""UPDATE scheduled_emails SET status='sending', claim_token={p},
                        claimed_at={p} WHERE id={p} AND status='pending'""",
                    (token, now.isoformat(), job_id),
                )
            conn.commit()
            if ids:
                cur.execute(
                    f"SELECT * FROM scheduled_emails WHERE claim_token={p} AND status='sending'",
                    (token,),
                )
                claimed = rows_as_dicts(cur)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return claimed


def update_job_after_send(job: dict[str, Any]) -> None:
    now = utc_now()
    repeat = str(job.get("repeat_type") or "once").lower()
    old_schedule = as_utc(job.get("schedule_time")) or now
    conn = db_connection()
    cur = conn.cursor()
    p = sql_placeholder()
    if repeat == "once":
        if DB_URL:
            cur.execute(
                f"""UPDATE scheduled_emails SET status='sent',last_sent={p},last_error=NULL,
                    claim_token=NULL,claimed_at=NULL WHERE id={p}""",
                (now, job["id"]),
            )
        else:
            cur.execute(
                f"""UPDATE scheduled_emails SET status='sent',last_sent={p},last_error=NULL,
                    claim_token=NULL,claimed_at=NULL WHERE id={p}""",
                (now.isoformat(), job["id"]),
            )
    else:
        step = timedelta(days=1 if repeat == "daily" else 7)
        next_run = old_schedule
        while next_run <= now:
            next_run += step
        if DB_URL:
            cur.execute(
                f"""UPDATE scheduled_emails SET status='pending',schedule_time={p},last_sent={p},
                    attempts=0,last_error=NULL,claim_token=NULL,claimed_at=NULL WHERE id={p}""",
                (next_run, now, job["id"]),
            )
        else:
            cur.execute(
                f"""UPDATE scheduled_emails SET status='pending',schedule_time={p},last_sent={p},
                    attempts=0,last_error=NULL,claim_token=NULL,claimed_at=NULL WHERE id={p}""",
                (next_run.isoformat(), now.isoformat(), job["id"]),
            )
    conn.commit()
    conn.close()


def update_job_failed(job: dict[str, Any], error: str) -> None:
    attempts = int(job.get("attempts") or 0) + 1
    terminal = attempts >= MAX_RETRIES
    status = "failed" if terminal else "pending"
    # Exponential backoff; cap at 1 hour. Retry the next time the worker checks after this delay.
    delay = min(3600, 30 * (2 ** (attempts - 1)))
    retry_at = utc_now() + timedelta(seconds=delay)
    conn = db_connection()
    cur = conn.cursor()
    p = sql_placeholder()
    if DB_URL:
        cur.execute(
            f"""UPDATE scheduled_emails SET status={p},attempts={p},last_error={p},
                schedule_time=CASE WHEN {p}='pending' THEN {p} ELSE schedule_time END,
                claim_token=NULL,claimed_at=NULL WHERE id={p}""",
            (status, attempts, error[:4000], status, retry_at, job["id"]),
        )
    else:
        cur.execute(
            f"""UPDATE scheduled_emails SET status={p},attempts={p},last_error={p},
                schedule_time=CASE WHEN {p}='pending' THEN {p} ELSE schedule_time END,
                claim_token=NULL,claimed_at=NULL WHERE id={p}""",
            (status, attempts, error[:4000], status, retry_at.isoformat(), job["id"]),
        )
    conn.commit()
    conn.close()
    add_log(str(job.get("to_emails", "")), str(job.get("subject", "")), "failed", error)


def run_worker_once(sender_email: str, sender_pass: str) -> int:
    recover_stale_claims()
    jobs = claim_due_jobs()
    for job in jobs:
        try:
            job_sender = str(job.get("sender_email") or sender_email)
            if job_sender.lower() != sender_email.lower():
                raise ValueError(
                    "This scheduled job uses a different sender than the worker's configured "
                    "SENDER_EMAIL. Run a dedicated worker with matching credentials."
                )
            attachments = attachment_bytes(job.get("attachments_meta"))
            send_email_smtp(
                job_sender, sender_pass, str(job["to_emails"]), str(job.get("cc_emails") or ""),
                str(job["subject"]), str(job["body"]), attachments,
            )
            add_log(str(job["to_emails"]), str(job["subject"]), "sent")
            update_job_after_send(job)
            LOG.info("Sent scheduled email id=%s", job["id"])
        except Exception as exc:
            LOG.exception("Scheduled email id=%s failed", job.get("id"))
            update_job_failed(job, f"{type(exc).__name__}: {exc}")
    return len(jobs)


def worker_loop() -> None:
    sender_email = secret_value("SENDER_EMAIL")
    sender_pass = secret_value("SENDER_APP_PASSWORD")
    if not sender_email or not sender_pass:
        raise SystemExit(
            "Worker requires SENDER_EMAIL and SENDER_APP_PASSWORD environment variables "
            "or Streamlit secrets."
        )
    init_db()
    LOG.info("MailForge worker started; poll interval=%ss; timezone=%s",
             WORKER_POLL_SECONDS, APP_TZ.key)
    while True:
        try:
            run_worker_once(sender_email, sender_pass)
        except Exception:
            LOG.exception("Worker cycle failed")
        time.sleep(WORKER_POLL_SECONDS)


def require_access() -> bool:
    """Optional single-operator access gate. Set MAILFORGE_ACCESS_PASSWORD in secrets."""
    required = secret_value("MAILFORGE_ACCESS_PASSWORD")
    if not required:
        return True
    if st.session_state.get("access_granted"):
        return True
    st.title("🔐 MailForge Pro")
    with st.form("access_form"):
        entered = st.text_input("Access password", type="password")
        submitted = st.form_submit_button("Unlock")
    if submitted:
        import hmac
        if hmac.compare_digest(entered, required):
            st.session_state["access_granted"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.caption("This is a single shared access gate, not multi-user authentication.")
    return False


def app() -> None:
    st.set_page_config(page_title=APP_NAME, page_icon="📧", layout="wide")
    if not require_access():
        st.stop()
    init_db()

    sender_email_default = secret_value("SENDER_EMAIL")
    sender_pass_default = secret_value("SENDER_APP_PASSWORD")
    gemini_key_default = secret_value("GEMINI_API_KEY")
    openai_key_default = secret_value("OPENAI_API_KEY")

    with st.sidebar:
        st.title("⚙️ MailForge Pro")
        st.caption(f"Database: {'PostgreSQL' if DB_URL else 'SQLite'}")
        st.caption(f"Schedule timezone: {APP_TZ.key}")
        sender_email = st.text_input("Gmail / SMTP sender", value=sender_email_default)
        sender_pass = st.text_input(
            "Gmail App Password",
            value=sender_pass_default,
            type="password",
            help="Use a provider app password. Never commit it to source control.",
        )
        provider = st.selectbox("AI provider", ["Gemini", "OpenAI", "Templates only"])
        if provider == "Gemini":
            ai_key = st.text_input("Gemini API key", value=gemini_key_default, type="password")
        elif provider == "OpenAI":
            ai_key = st.text_input("OpenAI API key", value=openai_key_default, type="password")
        else:
            ai_key = ""
        st.divider()
        st.caption("For reliable cloud scheduling, run `python mailforge.py --worker` as a separate persistent service.")
        if not DB_URL:
            st.warning("SQLite mode: suitable for local/demo use. Use PostgreSQL for multi-process deployments.")

    st.title("📧 MailForge Pro")
    st.caption("AI compose · recipient validation · spam heuristics · scheduled delivery · sent log")

    tab_compose, tab_queue, tab_logs = st.tabs(["✍️ Compose & Send", "⏰ Scheduled Queue", "📜 Sent Log"])

    with tab_compose:
        if "draft_to_insert" in st.session_state:
            st.session_state["email_body"] = st.session_state.pop("draft_to_insert")
        left, right = st.columns([2, 1])
        with left:
            to_emails = st.text_input("To", placeholder="person@example.com, team@example.com")
            cc_emails = st.text_input("CC (optional)")
            subject = st.text_input("Subject")
            body = st.text_area("Email body", height=250, key="email_body")
            uploads = st.file_uploader(
                "Attachments",
                accept_multiple_files=True,
                help=f"{MAX_ATTACHMENT_MB} MB per file; {MAX_TOTAL_ATTACHMENT_MB} MB total.",
            )
            a, b, c = st.columns(3)
            with a:
                if st.button("Validate recipients", use_container_width=True):
                    valid_to, invalid_to = validate_email_list(to_emails)
                    valid_cc, invalid_cc = validate_email_list(cc_emails)
                    if invalid_to or invalid_cc:
                        st.error(f"Invalid addresses: {invalid_to + invalid_cc}")
                    else:
                        st.success(f"Syntax valid for {len(valid_to)} To and {len(valid_cc)} CC address(es). This does not prove inbox existence.")
            with b:
                if st.button("Check spam signals", use_container_width=True):
                    score, hits = spam_score(subject + "\n" + body)
                    st.progress(score)
                    st.write(f"Heuristic score: {score}/95")
                    st.write("Matched phrases: " + (", ".join(hits) if hits else "none"))
            with c:
                st.metric("Attachments", len(uploads or []))

            send_col, schedule_col = st.columns(2)
            with send_col:
                if st.button("🚀 Send now", type="primary", use_container_width=True):
                    try:
                        if not sender_email or not sender_pass:
                            raise ValueError("Configure sender email and app password in the sidebar.")
                        if not subject.strip():
                            raise ValueError("Subject is required.")
                        valid_to, bad_to = validate_email_list(to_emails)
                        valid_cc, bad_cc = validate_email_list(cc_emails)
                        if bad_to or bad_cc or not valid_to:
                            raise ValueError(f"Invalid or missing recipient(s): {bad_to + bad_cc}")
                        attachments: list[dict[str, Any]] = [
                            {"name": Path(f.name).name, "content_type": f.type or "application/octet-stream", "content": f.getvalue()}
                            for f in (uploads or [])
                        ]
                        if sum(len(a["content"]) for a in attachments) > MAX_TOTAL_ATTACHMENT_MB * 1024 * 1024:
                            raise ValueError(f"Total attachments exceed {MAX_TOTAL_ATTACHMENT_MB} MB.")
                        for attachment in attachments:
                            if len(attachment["content"]) > MAX_ATTACHMENT_MB * 1024 * 1024:
                                raise ValueError(f"{attachment['name']} exceeds {MAX_ATTACHMENT_MB} MB.")
                        send_email_smtp(sender_email, sender_pass, to_emails, cc_emails, subject, body, attachments)
                        add_log(to_emails, subject, "sent")
                        st.success("Email sent.")
                    except Exception as exc:
                        try:
                            add_log(to_emails, subject, "failed", f"{type(exc).__name__}: {exc}")
                        except Exception:
                            LOG.exception("Could not write send failure to log")
                        st.error(f"Send failed: {exc}")
            with schedule_col:
                st.markdown("**Schedule delivery**")
                schedule_date = st.date_input("Date", value=date.today(), min_value=date.today(), key="schedule_date")
                schedule_clock = st.time_input("Time", value=(datetime.now(APP_TZ) + timedelta(minutes=5)).time().replace(second=0, microsecond=0), key="schedule_clock")
                repeat_type = st.selectbox("Repeat", ["once", "daily", "weekly"])
                if st.button("⏰ Save schedule", use_container_width=True):
                    try:
                        if not sender_email:
                            raise ValueError("Sender email is required.")
                        if not subject.strip():
                            raise ValueError("Subject is required.")
                        valid_to, bad_to = validate_email_list(to_emails)
                        valid_cc, bad_cc = validate_email_list(cc_emails)
                        if bad_to or bad_cc or not valid_to:
                            raise ValueError(f"Invalid or missing recipient(s): {bad_to + bad_cc}")
                        if len(set(x.lower() for x in valid_to + valid_cc)) > MAX_RECIPIENTS:
                            raise ValueError(f"Maximum recipients per email is {MAX_RECIPIENTS}.")
                        local_target = datetime.combine(schedule_date, schedule_clock).replace(tzinfo=APP_TZ)
                        if repeat_type == "once" and local_target.astimezone(timezone.utc) <= utc_now():
                            raise ValueError("Choose a future date and time.")
                        attachments_meta = read_uploads(uploads or [])
                        job_id = create_schedule({
                            "to": ", ".join(valid_to),
                            "cc": ", ".join(valid_cc),
                            "subject": subject.strip(),
                            "body": body,
                            "attachments": attachments_meta,
                            "schedule_time": local_target.astimezone(timezone.utc),
                            "repeat_type": repeat_type,
                            "sender": sender_email.strip(),
                        })
                        st.success(f"Scheduled job #{job_id} for {local_target.strftime('%Y-%m-%d %H:%M %Z')}.")
                    except Exception as exc:
                        st.error(f"Could not schedule email: {exc}")

        with right:
            st.subheader("✨ AI Studio")
            occasion = st.selectbox("Email type", ["professional", "follow_up", "thank_you", "birthday", "cold_outreach"])
            recipient_name = st.text_input("Recipient name", value="there")
            sender_name = st.text_input("Your name", value=sender_email.split("@")[0].replace(".", " ").title() if "@" in sender_email else "")
            context = st.text_area("Context / instructions", placeholder="Ask for a meeting about the Q3 report.")
            if st.button("Generate email", use_container_width=True):
                try:
                    result = generate_ai(context or occasion, occasion, recipient_name, sender_name, provider, ai_key)
                    st.session_state["generated_email"] = result
                except Exception as exc:
                    st.error(f"AI generation failed: {type(exc).__name__}: {exc}")
            if "generated_email" in st.session_state:
                generated = st.text_area("Generated draft", value=st.session_state["generated_email"], height=220, key="generated_draft")
                if st.button("Use generated draft"):
                    st.session_state["draft_to_insert"] = generated
                    st.rerun()

    with tab_queue:
        st.subheader("Scheduled queue")
        try:
            jobs = list_schedules()
            if not jobs:
                st.info("No scheduled emails yet.")
            for job in jobs:
                with st.container(border=True):
                    cols = st.columns([3, 2, 1, 1])
                    with cols[0]:
                        st.markdown(f"**{job.get('subject', '(no subject)')}**")
                        st.caption(f"To: {job.get('to_emails', '')}")
                        st.caption(f"{job.get('repeat_type', 'once')} · {local_display(job.get('schedule_time'))}")
                    with cols[1]:
                        st.write(f"Status: **{job.get('status', 'unknown')}**")
                        st.caption(f"Attempts: {job.get('attempts', 0)} · Attachments: {len(attachment_bytes(job.get('attachments_meta')))}")
                        if job.get("last_error"):
                            st.error(str(job["last_error"])[:500])
                    with cols[2]:
                        st.caption(f"Created: {local_display(job.get('created_at'))}")
                    with cols[3]:
                        if st.button("Delete", key=f"delete_{job['id']}"):
                            delete_schedule(int(job["id"]))
                            st.rerun()
        except Exception as exc:
            st.error(f"Could not load schedule queue: {exc}")

    with tab_logs:
        st.subheader("Sent and failed delivery log")
        try:
            logs = list_logs()
            if logs:
                import pandas as pd
                normalized: list[dict[str, Any]] = []
                for row in logs:
                    item = dict(row)
                    item["sent_at"] = local_display(item.get("sent_at"))
                    normalized.append(item)
                getattr(st, "dataframe")(pd.DataFrame(normalized), use_container_width=True, hide_index=True)
            else:
                st.info("No email activity recorded.")
        except Exception as exc:
            st.error(f"Could not load logs: {exc}")

    st.divider()
    st.caption("MailForge Pro · Keep secrets out of source control. Use a dedicated worker and PostgreSQL for reliable hosted scheduling.")


if __name__ == "__main__":
    if "--worker" in sys.argv:
        worker_loop()
    else:
        app()
