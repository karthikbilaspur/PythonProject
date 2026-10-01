import os
import shutil
import datetime
import logging
import gzip
import hashlib
from cryptography.fernet import Fernet

# Set up logging
logging.basicConfig(filename='backup.log', level=logging.INFO)

def generate_key():
    key = Fernet.generate_key()
    return key

def encrypt_file(key, file_path):
    cipher_suite = Fernet(key)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def compress_file(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    compressed_data = gzip.compress(file_data)
    with open(file_path + '.gz', 'wb') as file:
        file.write(compressed_data)

def backup_files(src_dir, backup_dir, key=None):
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Get current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create backup folder with current date and time
    backup_folder = os.path.join(backup_dir, f"backup_{current_datetime}")
    os.makedirs(backup_folder)

    # Copy files from source directory to backup folder
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, src_dir)
            backup_file = os.path.join(backup_folder, rel_path)
            os.makedirs(os.path.dirname(backup_file), exist_ok=True)
            shutil.copy2(src_file, backup_file)

            # Compress file
            compress_file(backup_file)

            # Encrypt file if key is provided
            if key:
                encrypt_file(key, backup_file + '.gz')

            # Log backup operation
            logging.info(f"Backed up {src_file} to {backup_file}")

    print(f"Backup generated successfully at {backup_folder}")

def incremental_backup(src_dir, backup_dir, last_backup_dir, key=None):
    # Get list of files that have changed since last backup
    changed_files = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, src_dir)
            last_backup_file = os.path.join(last_backup_dir, rel_path)
            if not os.path.exists(last_backup_file) or os.path.getmtime(src_file) > os.path.getmtime(last_backup_file):
                changed_files.append(src_file)

    # Backup changed files
    for file in changed_files:
        rel_path = os.path.relpath(file, src_dir)
        backup_file = os.path.join(backup_dir, rel_path)
        os.makedirs(os.path.dirname(backup_file), exist_ok=True)
        shutil.copy2(file, backup_file)

        # Compress file
        compress_file(backup_file)

        # Encrypt file if key is provided
        if key:
            encrypt_file(key, backup_file + '.gz')

        # Log backup operation
        logging.info(f"Backed up {file} to {backup_file}")

    print(f"Incremental backup generated successfully at {backup_dir}")

def main():
    src_dir = input("Enter source directory path: ")
    backup_dir = input("Enter backup directory path: ")
    key = generate_key()
    print(f"Generated key: {key}")
    use_key = input("Use key for encryption? (yes/no): ")
    if use_key.lower() == "yes":
        backup_files(src_dir, backup_dir, key)
    else:
        backup_files(src_dir, backup_dir)

    incremental_backup_option = input("Perform incremental backup? (yes/no): ")
    if incremental_backup_option.lower() == "yes":
        last_backup_dir = input("Enter last backup directory path: ")
        if use_key.lower() == "yes":
            incremental_backup(src_dir, backup_dir, last_backup_dir, key)
        else:
            incremental_backup(src_dir, backup_dir, last_backup_dir)

if __name__ == "__main__":
    main()