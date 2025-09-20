import socket
import sys

def get_ip_from_hostname(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror as e:
        return f"Invalid hostname: {e}"

def get_local_machine_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return hostname, ip_address

def main():
    if len(sys.argv) > 1:
        hostname = sys.argv[1]
        ip_address = get_ip_from_hostname(hostname)
        print(f"The IP address of {hostname} is: {ip_address}")
    else:
        print("1. Get IP address from hostname")
        print("2. Get local machine IP address")
        choice = input("Enter your choice (1/2): ")
        
        if choice == "1":
            hostname = input("Enter the hostname: ")
            ip_address = get_ip_from_hostname(hostname)
            print(f"The IP address of {hostname} is: {ip_address}")
        elif choice == "2":
            hostname, ip_address = get_local_machine_ip()
            print(f"Hostname: {hostname}")
            print(f"IP Address: {ip_address}")
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()