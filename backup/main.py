import os
import shutil
import tarfile
import gzip
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import argparse
import json
import getpass
import subprocess
from typing import Any

# Configuration
config: dict[str, Any] = {
    "backup_sources": [],
    "backup_schedule": "daily",
    "compression": True,
    "encryption": True,
    "notification": {
        "enabled": True,
        "smtp_server": "",
        "smtp_port": 587,
        "from_email": "",
        "to_email": "",
        "password": ""
    }
}

# Logging
logging.basicConfig(filename="backup.log", level=logging.INFO)

def load_config(config_file: str) -> None:
    try:
        with open(config_file, "r") as f:
            config.update(json.load(f))
    except FileNotFoundError:
        logging.error(f"Config file {config_file} not found")
        exit(1)
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in config file {config_file}")
        exit(1)

def save_config(config_file: str) -> None:
    try:
        with open(config_file, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to save config: {str(e)}")

def backup(source: str, destination: str) -> None:
    try:
        # Create destination directory if it doesn't exist
        if not os.path.exists(destination):
            os.makedirs(destination)

        # Perform incremental backup using rsync
        subprocess.run(
            ["rsync", "-avz", "--delete", f"{source}/", f"{destination}/"],
            check=True,
        )

        # Compress backup
        if config["compression"]:
            compress_backup(destination)

        # Encrypt backup
        if config["encryption"]:
            encrypt_backup(destination)

        logging.info(f"Backup completed successfully for {source}")
        send_notification(f"Backup completed successfully for {source}")
    except Exception as e:
        logging.error(f"Backup failed for {source}: {str(e)}")
        send_notification(f"Backup failed for {source}: {str(e)}")

def compress_backup(destination: str) -> None:
    try:
        # Create a tarball of the backup
        tarball_name = f"{destination}.tar"
        with tarfile.open(tarball_name, "w") as tar:
            tar.add(destination)

        # Compress the tarball using gzip
        with open(tarball_name, "rb") as f_in, gzip.open(f"{tarball_name}.gz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

        # Remove the original tarball
        os.remove(tarball_name)
    except Exception as e:
        logging.error(f"Compression failed: {str(e)}")

def encrypt_backup(destination: str) -> None:
    try:
        # Encrypt the compressed backup using a tool like OpenSSL
        encrypted_file_name = f"{destination}.enc"
        password = getpass.getpass("Enter encryption password: ")
        subprocess.run(
            [
                "openssl",
                "enc",
                "-aes-256-cbc",
                "-in",
                f"{destination}.tar.gz",
                "-out",
                encrypted_file_name,
                "-pass",
                f"pass:{password}",
            ],
            check=True,
        )

        # Remove the original compressed file
        os.remove(f"{destination}.tar.gz")
    except Exception as e:
        logging.error(f"Encryption failed: {str(e)}")

def send_notification(message: str) -> None:
    if config["notification"]["enabled"]:
        try:
            # Set up SMTP server
            server = smtplib.SMTP(config["notification"]["smtp_server"], config["notification"]["smtp_port"])
            server.starttls()
            server.login(config["notification"]["from_email"], config["notification"]["password"])

            # Create email message
            msg = MIMEMultipart()
            msg["From"] = config["notification"]["from_email"]
            msg["To"] = config["notification"]["to_email"]
            msg["Subject"] = "Backup Notification"
            msg.attach(MIMEText(message, "plain"))

            # Send email
            server.sendmail(config["notification"]["from_email"], config["notification"]["to_email"], msg.as_string())
            server.quit()
        except Exception as e:
            logging.error(f"Notification failed: {str(e)}")

def schedule_backup() -> float:
    intervals = {"daily": 86400.0, "weekly": 604800.0, "monthly": 2592000.0}
    return intervals.get(str(config["backup_schedule"]), intervals["daily"])

def run_backup() -> None:
    sources = config["backup_sources"]
    if isinstance(sources, list):
        for backup_source in sources:
            if isinstance(backup_source, dict):
                source = backup_source.get("source")
                destination = backup_source.get("destination")
                if isinstance(source, str) and isinstance(destination, str):
                    backup(source, destination)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup script")
    parser.add_argument("-c", "--config", help="Path to config file")
    args = parser.parse_args()

    if args.config:
        load_config(args.config)
    else:
        logging.error("No config file specified")
        exit(1)

    interval = schedule_backup()
    while True:
        run_backup()
        time.sleep(interval)