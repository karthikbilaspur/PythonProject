import subprocess
import platform
import json

def get_wifi_passwords():
    wifi_passwords = {}

    if platform.system() == 'Windows':
        # Get WiFi profiles
        profiles = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
        profiles = [profile.split(':')[1][1:-1] for profile in profiles if 'All User Profile' in profile]

        # Get WiFi passwords
        for profile in profiles:
            password = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8').split('\n')
            password = [line.split(':')[1][1:-1] for line in password if 'Key Content' in line]
            wifi_passwords[profile] = password[0] if password else None

    elif platform.system() == 'Linux':
        # Get WiFi profiles
        profiles = subprocess.check_output(['ls', '/etc/NetworkManager/system-connections/']).decode('utf-8').split('\n')
        profiles = [profile for profile in profiles if profile]

        # Get WiFi passwords
        for profile in profiles:
            try:
                with open(f'/etc/NetworkManager/system-connections/{profile}', 'r') as f:
                    lines = f.readlines()
                    password = [line.split('=')[1].strip() for line in lines if 'psk=' in line]
                    wifi_passwords[profile] = password[0] if password else None
            except Exception as e:
                print(f'Error reading {profile}: {e}')

    return wifi_passwords

def save_wifi_passwords(passwords, filename='wifi_passwords.json'):
    with open(filename, 'w') as f:
        json.dump(passwords, f, indent=4)

def main():
    wifi_passwords = get_wifi_passwords()
    save_wifi_passwords(wifi_passwords)
    print('WiFi passwords saved to wifi_passwords.json')

if __name__ == '__main__':
    main()