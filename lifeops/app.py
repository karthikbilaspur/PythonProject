"""
Personal Life OS - All in ONE file
==================================
Your own offline dashboard. 100% your data, no scraping, no API keys.

Features:
  1. Dashboard - Today at a glance
  2. Expenses - Add expense, monthly chart, category breakdown, savings rate
  3. Habits - Daily habits, streaks, weekly heatmap
  4. To-Do - Tasks with priority, due date, done %
  5. Focus Timer - Pomodoro 25/5 timer
  6. Wellness - Mood (1-5), Sleep hours, Workout log + charts
  7. Journal - Daily notes, search, word count

Run:
    pip install streamlit pandas
    streamlit run personal_life_os.py

Data: Saved locally to life_os_data.json in same folder. Delete it to reset.
"""

import json
import os
from datetime import date, datetime, timedelta
from typing import Any, TypedDict, cast

import pandas as pd
import streamlit as st

DATA_FILE = "life_os_data.json"
DEFAULT_HABITS = ["Workout", "Read 20 min", "Meditate", "No Sugar", "Drink Water", "Code / Learn"]
EXPENSE_CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Health", "Fun", "Other"]
MOODS = {1: "😞 Rough", 2: "😐 Meh", 3: "🙂 Okay", 4: "😊 Good", 5: "🤩 Great"}


class Expense(TypedDict):
    amount: float
    category: str
    date: str
    note: str


class Todo(TypedDict):
    title: str
    priority: str
    due: str
    done: bool
    created: str


class WellnessEntry(TypedDict):
    date: str
    mood: int
    sleep: float
    workout: str
    note: str


class JournalEntry(TypedDict):
    date: str
    text: str


class LifeData(TypedDict):
    expenses: list[Expense]
    habits_log: dict[str, dict[str, bool]]
    todos: list[Todo]
    wellness: list[WellnessEntry]
    journal: list[JournalEntry]

# ---------- Storage ----------
def load_data() -> LifeData:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                d = cast(dict[str, Any], json.load(f))
                # ensure keys exist
                for k in ["expenses", "habits_log", "todos", "wellness", "journal"]:
                    d.setdefault(k, [] if k != "habits_log" else {})
                return cast(LifeData, d)
        except Exception:
            pass
    return {"expenses": [], "habits_log": {}, "todos": [], "wellness": [], "journal": []}


def get_data() -> LifeData:
    return cast(LifeData, st.session_state["data"])

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(get_data(), f, indent=2, ensure_ascii=False)

if "data" not in st.session_state:
    st.session_state.data = load_data()

# ---------- Helpers ----------
def today_str():
    return date.today().isoformat()

def streak_for_habit(habit: str) -> int:
    log = st.session_state.data["habits_log"]
    streak = 0
    d = date.today()
    # if today not done yet, start from yesterday
    if log.get(d.isoformat(), {}).get(habit) is not True:
        d -= timedelta(days=1)
    while log.get(d.isoformat(), {}).get(habit) is True:
        streak += 1
        d -= timedelta(days=1)
    return streak

def money(n: int | float):
    return f"₹{n:,.0f}"

# Streamlit type stubs can mark these as partially unknown in some editors.
# Wrap them in strongly-typed Any helpers so Pyright doesn't complain here.
def st_write(*args: Any, **kwargs: Any) -> None:
    cast(Any, st).write(*args, **kwargs)


def st_dataframe(*args: Any, **kwargs: Any) -> Any:
    return cast(Any, st).dataframe(*args, **kwargs)


def st_bar_chart(data: Any, **kwargs: Any) -> Any:
    return cast(Any, st).bar_chart(data, **kwargs)


def st_line_chart(data: Any, **kwargs: Any) -> Any:
    return cast(Any, st).line_chart(data, **kwargs)


# ---------- App ----------
st.set_page_config(page_title="Personal Life OS", page_icon="🧬", layout="wide")
st.title("🧬 Personal Life OS")
st.caption("Your day, money, habits, focus & mood — in one place. All data stays on your computer.")

tabs = st.tabs(["🏠 Dashboard", "💰 Expenses", "✅ Habits", "📝 To-Do", "⏱️ Focus", "💪 Wellness", "📓 Journal"])

# ================= DASHBOARD =================
with tabs[0]:
    data = get_data()
    c1, c2, c3, c4 = st.columns(4)
    today = today_str()
    today_exp = sum(e["amount"] for e in data["expenses"] if e["date"] == today)
    done_todos = sum(1 for t in data["todos"] if t["done"])
    total_todos = len(data["todos"])
    today_habits = data["habits_log"].get(today, {})
    habits_done = sum(1 for v in today_habits.values() if v)
    c1.metric("Spent Today", money(today_exp))
    c2.metric("Habits Done Today", f"{habits_done}/{len(DEFAULT_HABITS)}")
    c3.metric("Tasks Done", f"{done_todos}/{total_todos}" if total_todos else "0/0")
    # mood today
    mood_today = next((w for w in data["wellness"] if w["date"] == today), None)
    c4.metric("Mood Today", MOODS.get(mood_today["mood"], "—") if mood_today else "Not logged")

    st.divider()
    colA, colB = st.columns(2)
    with colA:
        st.subheader("💰 Last 7 Days Spending")
        if data["expenses"]:
            expenses_df: pd.DataFrame = pd.DataFrame(data["expenses"])
            expenses_df["amount"] = pd.to_numeric(expenses_df["amount"], errors="coerce").fillna(0.0)
            expenses_df["date"] = pd.to_datetime(expenses_df["date"], errors="coerce")
            expenses_df = expenses_df.dropna(subset=["date"]).copy()
            last7 = expenses_df[expenses_df["date"] >= pd.Timestamp.today() - pd.Timedelta(days=6)]
            if not last7.empty:
                daily = last7.groupby(last7["date"].dt.date)["amount"].sum()
                daily_df: pd.DataFrame = daily.to_frame(name="amount")
                cast(Any, st).bar_chart(daily_df)
            else:
                st.info("No expenses in last 7 days.")
        else:
            st.info("Add your first expense in the Expenses tab →")
    with colB:
        st.subheader("✅ Today's Habits")
        for h in DEFAULT_HABITS:
            done = today_habits.get(h, False)
            cast(Any, st).write(f"{'✅' if done else '⬜'} {h} — 🔥 {streak_for_habit(h)} day streak")
        st.subheader("📝 Top 3 Pending Tasks")
        pending = [t for t in data["todos"] if not t["done"]][:3]
        if pending:
            for t in pending:
                cast(Any, st).write(f"• **{t['title']}** — {t['priority']} · due {t['due'] or '—'}")
        else:
            st.info("No pending tasks. Nice.")

# ================= EXPENSES =================
with tabs[1]:
    st.subheader("Add Expense")
    with st.form("expense_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        amt = c1.number_input("Amount ₹", min_value=0.0, step=10.0)
        cat = c2.selectbox("Category", EXPENSE_CATEGORIES)
        d = cast(date, c3.date_input("Date", value=date.today()))
        note = st.text_input("Note (optional)", placeholder="e.g. Lunch with friends, Metro, Groceries")
        if st.form_submit_button("➕ Add Expense"):
            if amt <= 0:
                st.error("Amount must be > 0")
            else:
                st.session_state.data["expenses"].append({
                    "amount": float(amt),
                    "category": cat,
                    "date": d.isoformat(),
                    "note": note,
                })
                save_data()
                st.success(f"Added {money(amt)} — {cat}")

    st.divider()
    data_exp = get_data()["expenses"]
    if data_exp:
        df: pd.DataFrame = pd.DataFrame(data_exp)
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        clean_df: pd.DataFrame = df.dropna(subset=["date"]).copy()
        if not clean_df.empty:
            month = st.selectbox("Month", sorted(clean_df["date"].dt.strftime("%Y-%m").unique(), reverse=True))
            month_df: pd.DataFrame = cast(
                pd.DataFrame,
                df.loc[df["date"].dt.strftime("%Y-%m") == month],
            ).copy()
            month_df["amount"] = pd.to_numeric(month_df["amount"], errors="coerce").fillna(0.0)

            month_total = float(month_df["amount"].sum())
            transaction_count = int(len(month_df))
            daily_avg = month_total / max(1, int(month_df["date"].dt.date.nunique()))

            c1, c2, c3 = st.columns(3)
            c1.metric("Total This Month", money(month_total))
            c2.metric("Transactions", transaction_count)
            c3.metric("Daily Avg", money(daily_avg))

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("By Category")
                category_totals = month_df.groupby("category", dropna=False)["amount"].sum().sort_values(ascending=False).to_frame(name="amount")
                st.bar_chart(category_totals)
            with col2:
                st.subheader("Daily Trend")
                daily_totals = month_df.groupby(month_df["date"].dt.date, as_index=False)["amount"].sum()
                st.line_chart(daily_totals.set_index("date")[["amount"]])

            st.subheader("All Expenses")
            show = month_df.sort_values("date", ascending=False).copy()
            show["date"] = show["date"].dt.date
            st.dataframe(show, use_container_width=True, hide_index=True)
            if st.button("🗑️ Clear All Expenses"):
                get_data()["expenses"] = []
                save_data()
                st.rerun()
        else:
            st.info("No valid expense dates found.")
    else:
        st.info("No expenses yet. Your first one goes here.")

# ================= HABITS =================
with tabs[2]:
    st.subheader("Today's Habits")
    today = today_str()
    log = get_data()["habits_log"]
    log.setdefault(today, {})
    for h in DEFAULT_HABITS:
        checked = st.checkbox(f"{h}  —  🔥 {streak_for_habit(h)} day streak", value=log[today].get(h, False), key=f"habit_{today}_{h}")
        log[today][h] = checked
    if st.button("💾 Save Habits"):
        save_data()
        st.success("Saved!")
        st.rerun()

    st.divider()
    st.subheader("Last 7 Days")
    rows: list[dict[str, str]] = []
    for i in range(6, -1, -1):
        d = (date.today() - timedelta(days=i)).isoformat()
        row: dict[str, str] = {"Date": d}
        for h in DEFAULT_HABITS:
            row[h] = "✅" if log.get(d, {}).get(h) else "⬜"
        rows.append(row)
    st_dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ================= TO-DO =================
with tabs[3]:
    st.subheader("Add Task")
    with st.form("todo_form", clear_on_submit=True):
        title = st.text_input("Task", placeholder="e.g. Finish portfolio, Call mom, Gym")
        c1, c2 = st.columns(2)
        prio = c1.selectbox("Priority", ["🔴 High", "🟡 Medium", "🟢 Low"])
        due = cast(date | None, c2.date_input("Due Date (optional)", value=None))
        if st.form_submit_button("➕ Add Task"):
            if title.strip():
                get_data()["todos"].append({"title": title.strip(), "priority": prio, "due": due.isoformat() if due else "", "done": False, "created": today_str()})
                save_data()
                st.rerun()

    st.divider()
    todos = get_data()["todos"]
    if not todos:
        st.info("No tasks yet.")
    else:
        for i, t in enumerate(todos):
            c1, c2, c3 = st.columns([0.08, 0.82, 0.10])
            done = c1.checkbox("", value=t["done"], key=f"todo_{i}")
            if done != t["done"]:
                t["done"] = done
                save_data()
                st.rerun()
            label = f"~~{t['title']}~~" if t["done"] else f"**{t['title']}** — {t['priority']} · due {t['due'] or '—'}"
            c2.markdown(label)
            if c3.button("🗑️", key=f"del_todo_{i}"):
                todos.pop(i)
                save_data()
                st.rerun()
        done_n = sum(1 for t in todos if t["done"])
        st.progress(done_n / len(todos) if todos else 0)
        st.caption(f"{done_n}/{len(todos)} done")

# ================= FOCUS =================
with tabs[4]:
    st.subheader("⏱️ Pomodoro Focus Timer")
    st.text("25 min focus → 5 min break. Use the timer below, or just log a session when you finish.")
    col1, col2 = st.columns(2)
    focus_min = int(col1.number_input("Focus minutes", value=25, min_value=5, max_value=120))
    task = col2.text_input("What are you focusing on?", placeholder="e.g. DSA, Portfolio, Reading")
    # Simple countdown using placeholder + manual start
    if "timer_end" not in st.session_state:
        st.session_state.timer_end = None
    if st.button("▶️ Start Focus Session"):
        st.session_state.timer_end = datetime.now() + timedelta(minutes=int(focus_min))
        st.session_state.focus_task = task
        st.rerun()
    if st.session_state.timer_end:
        remaining = st.session_state.timer_end - datetime.now()
        if remaining.total_seconds() > 0:
            mins, secs = divmod(int(remaining.total_seconds()), 60)
            st.markdown(f"### 🎯 Focusing on: **{st.session_state.get('focus_task','')}**")
            st.markdown(f"## {mins:02d}:{secs:02d} remaining")
            st.progress(1 - remaining.total_seconds() / (focus_min * 60))
            st.caption("Press Rerun / wait — Streamlit refreshes on interaction. For a live ticking timer, keep this tab open and click below.")
            if st.button("🔄 Refresh Timer"):
                st.rerun()
            if st.button("✅ Mark Session Done"):
                st.session_state.timer_end = None
                st.success("Nice work! Session logged in your head — and your streak.")
        else:
            st.session_state.timer_end = None
            st.balloons()
            st.success("🎉 Focus session complete! Take a 5 min break.")
    st.info("Tip: Put your phone on silent. One task, one timer.")

# ================= WELLNESS =================
with tabs[5]:
    st.subheader("Log Today")
    with st.form("wellness_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        mood = c1.selectbox("Mood", list(MOODS.keys()), format_func=lambda x: MOODS[x])
        sleep = c2.number_input("Sleep (hours)", min_value=0.0, max_value=16.0, step=0.5, value=7.0)
        workout = c3.selectbox("Workout", ["None", "Gym", "Run", "Walk", "Yoga", "Home Workout", "Sports"])
        note = st.text_input("Note", placeholder="e.g. Felt energetic, sore legs")
        if st.form_submit_button("💾 Log Today"):
            # replace if today already exists
            data = get_data()["wellness"]
            data[:] = [w for w in data if w["date"] != today_str()]
            data.append({"date": today_str(), "mood": int(mood), "sleep": float(sleep), "workout": workout, "note": note})
            save_data()
            st.success("Logged!")

    st.divider()
    wdata = get_data()["wellness"]
    if wdata:
        df: pd.DataFrame = pd.DataFrame(wdata)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Mood Over Time")
            st_line_chart(df.set_index("date")["mood"])
        with c2:
            st.subheader("Sleep Over Time")
            st_line_chart(df.set_index("date")["sleep"])
        st.subheader("Workout Count")
        st_bar_chart(df["workout"].value_counts())
        st_dataframe(df.sort_values("date", ascending=False), use_container_width=True, hide_index=True)
    else:
        st.info("No wellness logs yet.")

# ================= JOURNAL =================
with tabs[6]:
    st.subheader("Write Today's Entry")
    journal = get_data()["journal"]
    today_entry = next((j for j in journal if j["date"] == today_str()), None)
    text = st.text_area("How was today?", value=today_entry["text"] if today_entry else "", height=150, placeholder="3 wins today...\n1 thing I learned...\n1 thing to improve tomorrow...")
    if st.button("💾 Save Journal"):
        data = journal
        data[:] = [j for j in data if j["date"] != today_str()]
        data.append({"date": today_str(), "text": text})
        save_data()
        st.success("Saved!")

    st.divider()
    st.subheader("Search Past Entries")
    q = st.text_input("Search", placeholder="e.g. gym, interview, mom")
    entries = sorted(journal, key=lambda x: x["date"], reverse=True)
    if q:
        entries = [e for e in entries if q.lower() in e["text"].lower()]
    total_words = sum(len(e["text"].split()) for e in entries)
    st.caption(f"{len(entries)} entries · {total_words} words total")
    for e in entries[:10]:
        with st.expander(f"📓 {e['date']} — {len(e['text'].split())} words"):
            cast(Any, st).write(e["text"])

st.divider()
st.caption("Built in one file • Data in life_os_data.json • Made for you, by you.")
