# Backup Script
================

A Python script for automating backups of important files and directories.

## Features
------------

*   **Configurable backup sources and destinations**: Specify multiple backup sources and destinations using a configuration file.
*   **Incremental backups**: Perform incremental backups using `rsync` to save storage space and reduce backup time.
*   **Compression and encryption**: Compress backups using `gzip` and encrypt them using `OpenSSL`.
*   **Automated backup scheduling**: Schedule backups using the `schedule` library.
*   **Notification and logging**: Send notifications via email and log backup events using the `logging` library.

## Requirements
---------------

*   Python 3.6 or later
*   `schedule` library
*   `rsync` command-line tool
*   `gzip` command-line tool
*   `OpenSSL` command-line tool
*   `smtplib` library for email notifications

## Usage
-----

1.  Create a configuration file (e.g., `config.json`) with the following format:

```json
{
    "backup_sources": [
        {"source": "/path/to/source1", "destination": "/path/to/destination1"},
        {"source": "/path/to/source2", "destination": "/path/to/destination2"}
    ],
    "backup_schedule": "daily",
    "compression": true,
    "encryption": true,
    "notification": {
        "enabled": true,
        "smtp_server": "smtp.example.com",
        "smtp_port": 587,
        "from_email": "backup@example.com",
        "to_email": "admin@example.com",
        "password": "password"
    }
}