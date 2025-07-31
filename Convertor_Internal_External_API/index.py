import requests
import json

def check_api_status(api_url):
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            return f"API {api_url} is up and running."
        else:
            return f"API {api_url} is down with status code {response.status_code}."
    except requests.exceptions.RequestException as e:
        return f"Error checking API {api_url}: {str(e)}"

def check_internal_api_status():
    internal_api_url = "http://localhost:8080"  # replace with your internal API URL
    return check_api_status(internal_api_url)

def check_external_api_status():
    external_api_url = "https://jsonplaceholder.typicode.com/todos/1"  # replace with your external API URL
    return check_api_status(external_api_url)

def main():
    print("API Status Checker")
    print("--------------------")
    internal_api_status = check_internal_api_status()
    external_api_status = check_external_api_status()
    print(f"Internal API Status: {internal_api_status}")
    print(f"External API Status: {external_api_status}")

if __name__ == "__main__":
    main()