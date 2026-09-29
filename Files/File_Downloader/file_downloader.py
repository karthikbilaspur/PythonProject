import requests
from tqdm import tqdm

def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    t = tqdm(total=total_size, unit='B', unit_scale=True)

    with open(filename, 'wb') as f:
        for data in response.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()

    if total_size != 0 and t.n != total_size:
        print("Error: Download failed")
    else:
        print("Download complete")

def main():
    url = input("Enter the URL of the file: ")
    filename = input("Enter the filename to save as: ")
    download_file(url, filename)

if __name__ == "__main__":
    main()