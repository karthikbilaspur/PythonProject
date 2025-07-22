import requests
import os
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_file(url, filename, chunk_size=1024):
    """Downloads a file from the specified URL and saves it locally."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors

        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
                downloaded_size += len(chunk)
                logging.info(f"Downloading {filename}: {downloaded_size / total_size * 100 if total_size > 0 else 0:.2f}%")

        logging.info(f"File downloaded and saved as {filename}")
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while downloading: {e}")


def upload_file(url, filename, chunk_size=1024):
    """Uploads a file to the specified URL."""
    try:
        with open(filename, "rb") as file:
            total_size = os.path.getsize(filename)
            uploaded_size = 0

            def read_in_chunks(file_object, chunk_size):
                while True:
                    data = file_object.read(chunk_size)
                    if not data:
                        break
                    yield data

            response = requests.post(url, files={'file': (filename, read_in_chunks(file, chunk_size), 'application/octet-stream')})
            response.raise_for_status()  # Raise an exception for HTTP errors

            logging.info(f"File uploaded successfully. Status code: {response.status_code}")
    except FileNotFoundError:
        logging.error(f"File {filename} not found.")
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while uploading: {e}")


def main():
    parser = argparse.ArgumentParser(description='Download and upload files')
    parser.add_argument('-d', '--download_url', required=True, help='URL to download the file from')
    parser.add_argument('-u', '--upload_url', required=True, help='URL to upload the file to')
    parser.add_argument('-f', '--filename', required=True, help='Filename to save the downloaded file as')
    args = parser.parse_args()

    download_file(args.download_url, args.filename)
    upload_file(args.upload_url, args.filename)


if __name__ == "__main__":
    main()