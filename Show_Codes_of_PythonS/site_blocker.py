import time
import os
import sys

# Define the list of websites to block
websites_to_block = [
    'www.facebook.com',
    'facebook.com',
    'www.instagram.com',
    'instagram.com',
    # Add more websites to block here
]

# Define the hosts file path
hosts_path = '/etc/hosts'  # For Linux and Mac
# hosts_path = 'C:\Windows\System32\drivers\etc\hosts'  # For Windows

# Define the redirect IP address
redirect_ip = '127.0.0.1'

def block_websites():
    while True:
        # Check if the current time is within the block time
        current_time = time.strftime('%H:%M')
        if '09:00' <= current_time <= '17:00':  # Block websites between 9am and 5pm
            # Open the hosts file in write mode
            with open(hosts_path, 'r+') as file:
                content = file.read()
                for website in websites_to_block:
                    if website not in content:
                        # Add the website to the hosts file
                        file.write(redirect_ip + ' ' + website + '\n')
        else:
            # Remove the websites from the hosts file
            with open(hosts_path, 'r+') as file:
                content = file.readlines()
                file.seek(0)
                for line in content:
                    if not any(website in line for website in websites_to_block):
                        file.write(line)
                file.truncate()
        time.sleep(60)  # Check every 60 seconds

if __name__ == '__main__':
    if os.name == 'nt':  # For Windows
        # Run the script with admin privileges
        if not os.getuid() == 0:
            print('Please run the script with admin privileges.')
            sys.exit(1)
    block_websites()