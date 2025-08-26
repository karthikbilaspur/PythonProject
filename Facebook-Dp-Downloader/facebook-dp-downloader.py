import requests
import os

def download_profile_picture(fb_id):
    url = f"https://graph.facebook.com/{fb_id}/picture?type=large&width=720&height=720"
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        # Create a folder to store the profile picture
        folder_name = "profile_pictures"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Save the profile picture
        file_name = f"{fb_id}.jpg"
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Profile picture downloaded successfully: {file_path}")
    else:
        print("Failed to download profile picture")

def main():
    print("Facebook Profile Picture Downloader")
    print("------------------------------------")
    fb_id = input("Enter the Facebook ID: ")
    download_profile_picture(fb_id)

if __name__ == "__main__":
    main()
'''
Disclaimer 
Please note that this script is for educational purposes only and should not be used for malicious activities or in violation of Facebook's terms of service.'
Facebook's Graph API usage policies and guidelines should be reviewed and followed when using this script. 
Additionally, be mindful of the potential risks and consequences of downloading and storing profile pictures without consent. 
Use this script responsibly and at your own risk.
'''