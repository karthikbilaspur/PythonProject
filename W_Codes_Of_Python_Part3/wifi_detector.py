import speedtest
import time
import matplotlib.pyplot as plt
import os

def wifi_speed_test([string]) -> tuple[float, float]:
    """
    Test the WiFi speed.

    Returns:
        tuple[float, float]: The download and upload speeds in Mbps.
    """
    # Create a Speedtest object
    s = speedtest.Speedtest()

    # Get the best server
    s.get_best_server()

    # Test download speed
    download_speed = s.download() / (1024 * 1024)  # Convert to Mbps
    print(f"Download speed: {download_speed:.2f} Mbps")

    # Test upload speed
    upload_speed = s.upload() / (1024 * 1024)  # Convert to Mbps
    print(f"Upload speed: {upload_speed:.2f} Mbps")

    return download_speed, upload_speed

def wifi_speed_monitor(interval: int, duration: int):
    """
    Monitor the WiFi speed over time.

    Args:
        interval (int): The interval between speed tests in seconds.
        duration (int): The duration of the monitoring in seconds.

    Returns:
        None
    """
    download_speeds = []
    upload_speeds = []
    times = []

    start_time = time.time()
    while time.time() - start_time < duration:
        download_speed, upload_speed = wifi_speed_test()
        download_speeds.append(download_speed)
        upload_speeds.append(upload_speed)
        times.append(time.time() - start_time)
        time.sleep(interval)

    # Plot the results
    plt.plot(times, download_speeds, label='Download speed')
    plt.plot(times, upload_speeds, label='Upload speed')
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (Mbps)')
    plt.title('WiFi Speed Monitor')
    plt.legend()
    plt.show()

def save_wifi_speed_test_results(download_speed: float, upload_speed: float):
    """
    Save the WiFi speed test results to a file.

    Args:
        download_speed (float): The download speed in Mbps.
        upload_speed (float): The upload speed in Mbps.

    Returns:
        None
    """
    with open('wifi_speed_test_results.txt', 'a') as f:
        f.write(f"Download speed: {download_speed:.2f} Mbps, Upload speed: {upload_speed:.2f} Mbps\n")

if __name__ == "__main__":
    print("WiFi Speed Detector")
    print("1. Test WiFi speed")
    print("2. Monitor WiFi speed")
    print("3. Exit")

    while True:
        choice = input("Enter your choice: ")

        if choice == '1':
            download_speed, upload_speed = wifi_speed_test()
            save_wifi_speed_test_results(download_speed, upload_speed)
        elif choice == '2':
            interval = int(input("Enter the interval between speed tests in seconds: "))
            duration = int(input("Enter the duration of the monitoring in seconds: "))
            wifi_speed_monitor(interval, duration)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")