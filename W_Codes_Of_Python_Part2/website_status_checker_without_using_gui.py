import requests

def check_status(url: str) -> None:
    try:
        response = requests.head(url)
        status_code = response.status_code
        if status_code == 200:
            print(f"Website {url} is up and running")
        else:
            print(f"Website {url} is down. Status code: {status_code}")
    except requests.RequestException as e:
        print(f"Error: {e}")

def main():
    url = input("Enter website URL: ")
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    check_status(url)

if __name__ == "__main__":
    main()