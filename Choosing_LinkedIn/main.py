import requests
from requests_oauthlib import OAuth2Session
import json
import os

# LinkedIn API credentials
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "YOUR_REDIRECT_URI"
authorization_base_url = "https://www.linkedin.com/oauth/v2/authorization"
token_url = "https://www.linkedin.com/oauth/v2/accessToken"

# Authorization scope
scope = ["w_share", "r_liteprofile"]

def get_access_token():
    # Check if token file exists
    if os.path.exists("token.json"):
        with open("token.json", "r") as f:
            token = json.load(f)
        return token.get("access_token")

    # Create an OAuth2 session
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

    # Fetch authorization URL
    authorization_url, state = oauth.authorization_url(authorization_base_url)

    print(f"Please go to {authorization_url} and authorize the app.")

    # Get authorization response URL
    authorization_response = input("Enter the full callback URL: ")

    # Fetch access token
    token = oauth.fetch_token(token_url, client_secret=client_secret, authorization_response=authorization_response)

    # Save token to file
    with open("token.json", "w") as f:
        json.dump(token, f)

    return token.get("access_token")

def refresh_access_token(refresh_token):
    # Refresh access token
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

def post_update(access_token, text, media=None):
    # Set API endpoint and headers
    url = "https://api.linkedin.com/v2/shares"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Set share data
    data = {
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.Post": {
                "shareMediaCategory": "NONE",
                "text": {
                    "text": text
                }
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    if media:
        data["specificContent"]["com.linkedin.ugc.Post"]["shareMediaCategory"] = "ARTICLE"
        data["specificContent"]["com.linkedin.ugc.Post"]["media"] = [
            {
                "status": "READY",
                "description": {
                    "text": media.get("description")
                },
                "originalUrl": media.get("url"),
                "title": {
                    "text": media.get("title")
                }
            }
        ]

    # Post update
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("Update posted successfully!")
    else:
        print(f"Error posting update: {response.text}")

def get_profile(access_token):
    # Set API endpoint and headers
    url = "https://api.linkedin.com/v2/me"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Get profile data
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    access_token = get_access_token()
    while True:
        print("\n1. Post update")
        print("2. Get profile")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            text = input("Enter your LinkedIn update text: ")
            media = None
            if input("Do you want to add media? (yes/no): ").lower() == "yes":
                media = {
                    "title": input("Enter media title: "),
                    "description": input("Enter media description: "),
                    "url": input("Enter media URL: ")
                }
            post_update(access_token, text, media)
        elif choice == "2":
            profile = get_profile(access_token)
            print(json.dumps(profile, indent=4))
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()import requests
from requests_oauthlib import OAuth2Session
import json
import os

# LinkedIn API credentials
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "YOUR_REDIRECT_URI"
authorization_base_url = "https://www.linkedin.com/oauth/v2/authorization"
token_url = "https://www.linkedin.com/oauth/v2/accessToken"

# Authorization scope
scope = ["w_share", "r_liteprofile"]

def get_access_token():
    # Check if token file exists
    if os.path.exists("token.json"):
        with open("token.json", "r") as f:
            token = json.load(f)
        return token.get("access_token")

    # Create an OAuth2 session
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

    # Fetch authorization URL
    authorization_url, state = oauth.authorization_url(authorization_base_url)

    print(f"Please go to {authorization_url} and authorize the app.")

    # Get authorization response URL
    authorization_response = input("Enter the full callback URL: ")

    # Fetch access token
    token = oauth.fetch_token(token_url, client_secret=client_secret, authorization_response=authorization_response)

    # Save token to file
    with open("token.json", "w") as f:
        json.dump(token, f)

    return token.get("access_token")

def refresh_access_token(refresh_token):
    # Refresh access token
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

def post_update(access_token, text, media=None):
    # Set API endpoint and headers
    url = "https://api.linkedin.com/v2/shares"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Set share data
    data = {
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.Post": {
                "shareMediaCategory": "NONE",
                "text": {
                    "text": text
                }
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    if media:
        data["specificContent"]["com.linkedin.ugc.Post"]["shareMediaCategory"] = "ARTICLE"
        data["specificContent"]["com.linkedin.ugc.Post"]["media"] = [
            {
                "status": "READY",
                "description": {
                    "text": media.get("description")
                },
                "originalUrl": media.get("url"),
                "title": {
                    "text": media.get("title")
                }
            }
        ]

    # Post update
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("Update posted successfully!")
    else:
        print(f"Error posting update: {response.text}")

def get_profile(access_token):
    # Set API endpoint and headers
    url = "https://api.linkedin.com/v2/me"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Get profile data
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    access_token = get_access_token()
    while True:
        print("\n1. Post update")
        print("2. Get profile")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            text = input("Enter your LinkedIn update text: ")
            media = None
            if input("Do you want to add media? (yes/no): ").lower() == "yes":
                media = {
                    "title": input("Enter media title: "),
                    "description": input("Enter media description: "),
                    "url": input("Enter media URL: ")
                }
            post_update(access_token, text, media)
        elif choice == "2":
            profile = get_profile(access_token)
            print(json.dumps(profile, indent=4))
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()