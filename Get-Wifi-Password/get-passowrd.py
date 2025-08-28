import subprocess
import platform
import re

def get_wifi_password_windows(network_name):
    try:
        # Use subprocess to run the command to retrieve WiFi password
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', network_name, 'key=clear']).decode('utf-8').split('\n')
        
        # Extract the password from the output
        for line in data:
            if "Key Content" in line:
                password = line.split(":")[1].strip()
                return password
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def get_wifi_password_linux(network_name):
    try:
        # Use subprocess to run the command to retrieve WiFi password
        data = subprocess.check_output(['sudo', 'cat', f'/etc/NetworkManager/system-connections/{network_name}']).decode('utf-8').split('\n')
        
        # Extract the password from the output
        for line in data:
            if "psk=" in line:
                password = line.split("=")[1].strip()
                return password
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def get_wifi_password(network_name):
    current_os = platform.system()
    if current_os == "Windows":
        return get_wifi_password_windows(network_name)
    elif current_os == "Linux":
        return get_wifi_password_linux(network_name)
    else:
        print("Unsupported operating system.")
        return None

def get_all_wifi_networks():
    current_os = platform.system()
    if current_os == "Windows":
        try:
            # Use subprocess to run the command to retrieve all WiFi networks
            data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
            
            # Extract the network names from the output
            networks = []
            for line in data:
                if "All User Profile" in line:
                    network = line.split(":")[1].strip()
                    networks.append(network)
            return networks
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []
    elif current_os == "Linux":
        try:
            # Use subprocess to run the command to retrieve all WiFi networks
            data = subprocess.check_output(['sudo', 'ls', '/etc/NetworkManager/system-connections/']).decode('utf-8').split('\n')
            
            # Extract the network names from the output
            networks = []
            for line in data:
                if line:
                    networks.append(line)
            return networks
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []
    else:
        print("Unsupported operating system.")
        return []

def main():
    print("WiFi Password Retrieval Tool")
    print("-------------------------------")
    print("1. Get WiFi password for a network")
    print("2. Get all WiFi networks")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        network_name = input("Enter the WiFi network name: ")
        password = get_wifi_password(network_name)
        if password:
            print(f"The WiFi password for {network_name} is: {password}")
        else:
            print(f"Unable to retrieve password for {network_name}.")
    elif choice == "2":
        networks = get_all_wifi_networks()
        if networks:
            print("Available WiFi networks:")
            for network in networks:
                print(network)
        else:
            print("No WiFi networks found.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
    