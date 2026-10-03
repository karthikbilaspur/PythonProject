import requests
import os
import argparse
import logging
import sys
from typing import Any, BinaryIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def download_file(url: str, filename: str, chunk_size: int = 8192) -> bool:
    """Downloads a file with proper progress."""
    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()

            total_size = int(r.headers.get('content-length', 0))

            with open(filename, "wb") as f:
                downloaded = 0
                last_percent = 0

                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total_size > 0:
                            percent = int((downloaded / total_size) * 100)
                            # Log only every 10%
                            if percent >= last_percent + 10 or percent == 100:
                                logging.info(f"Downloading {filename}: {percent}% ({downloaded}/{total_size} bytes)")
                                last_percent = percent
                        else:
                            logging.info(f"Downloading {filename}: {downloaded} bytes")

        logging.info(f"Download complete: {filename}")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Download failed: {e}")
        if os.path.exists(filename):
            os.remove(filename)  # cleanup partial file
        return False


def upload_file(url: str, filename: str) -> bool:
    """Uploads a file with proper streaming and progress tracking."""
    if not os.path.exists(filename):
        logging.error(f"File {filename} not found.")
        return False

    try:
        file_size = os.path.getsize(filename)

        class ProgressFile:
            def __init__(self, file_obj: BinaryIO) -> None:
                self.file_obj = file_obj
                self.read_bytes = 0
                self.last_percent = 0

            def read(self, size: int = -1) -> bytes:
                data = self.file_obj.read(size)
                if data:
                    self.read_bytes += len(data)
                    if file_size > 0:
                        percent = int((self.read_bytes / file_size) * 100)
                        if percent >= self.last_percent + 10 or percent == 100:
                            logging.info(f"Uploading {filename}: {percent}%")
                            self.last_percent = percent
                return data

            def __getattr__(self, attr: str) -> Any:
                return getattr(self.file_obj, attr)

        with open(filename, "rb") as f:
            progress_file = ProgressFile(f)

            files = {'file': (os.path.basename(filename), progress_file, 'application/octet-stream')}
            response = requests.post(url, files=files, timeout=60)
            response.raise_for_status()

        logging.info(f"Upload successful! Status: {response.status_code} - {response.text[:200]}")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Upload failed: {e}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description='Download and upload files with progress')
    parser.add_argument('-d', '--download_url', required=True, help='URL to download from')
    parser.add_argument('-u', '--upload_url', required=True, help='URL to upload to')
    parser.add_argument('-f', '--filename', required=True, help='Local filename')
    parser.add_argument('--no-upload', action='store_true', help='Only download, dont upload')
    args = parser.parse_args()

    if download_file(args.download_url, args.filename):
        if not args.no_upload:
            upload_file(args.upload_url, args.filename)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()