# Backup Script README

Overview
This script generates backups of files and directories with optional encryption and compression.
Features
Full Backups: Backup entire directories with file compression and encryption
Incremental Backups: Backup only files that have changed since the last backup
Encryption: Use Fernet encryption to secure backup files
Compression: Compress backup files using gzip
Logging: Log backup operations to a file
Usage
Run the script and enter the source directory and backup directory paths.
Choose whether to use encryption and generate a key.
Select whether to perform a full or incremental backup.
Requirements
Python 3.x
os, shutil, datetime, logging, gzip, and cryptography libraries
