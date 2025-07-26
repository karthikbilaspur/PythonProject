import psutil
import time
import os

def get_bandwidth_usage():
    # Get the network I/O statistics
    net_io = psutil.net_io_counters()

    # Get the bytes sent and received
    bytes_sent = net_io.bytes_sent
    bytes_recv = net_io.bytes_recv

    return bytes_sent, bytes_recv

def calculate_bandwidth_usage(bytes_sent_prev, bytes_recv_prev):
    # Get the current bytes sent and received
    bytes_sent, bytes_recv = get_bandwidth_usage()

    # Calculate the bandwidth usage
    bytes_sent_diff = bytes_sent - bytes_sent_prev
    bytes_recv_diff = bytes_recv - bytes_recv_prev

    # Convert to kilobytes
    kb_sent = bytes_sent_diff / 1024
    kb_recv = bytes_recv_diff / 1024

    # Convert to human-readable format
    if kb_sent >= 1024:
        sent_str = f"{kb_sent / 1024:.2f} MB/s"
    else:
        sent_str = f"{kb_sent:.2f} KB/s"

    if kb_recv >= 1024:
        recv_str = f"{kb_recv / 1024:.2f} MB/s"
    else:
        recv_str = f"{kb_recv:.2f} KB/s"

    return sent_str, recv_str

def clear_screen():
    # Clear the screen for different operating systems
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def main():
    # Get the initial bytes sent and received
    bytes_sent_prev, bytes_recv_prev = get_bandwidth_usage()

    while True:
        # Clear the screen
        clear_screen()

        # Calculate the bandwidth usage
        sent_str, recv_str = calculate_bandwidth_usage(bytes_sent_prev, bytes_recv_prev)

        # Update the previous bytes sent and received
        bytes_sent_prev, bytes_recv_prev = get_bandwidth_usage()

        # Print the bandwidth usage
        print(f"Bandwidth Monitor")
        print("------------------")
        print(f"Upload: {sent_str} | Download: {recv_str}")

        # Wait for 1 second
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting Bandwidth Monitor...")