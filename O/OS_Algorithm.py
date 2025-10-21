import psutil
import time
import os
import platform
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_cpu_threshold(threshold, interval=10):
    """
    Monitor CPU usage and alert when it exceeds the threshold.

    Args:
        threshold (int): CPU usage threshold in percentage.
        interval (int): Time interval between checks in seconds. Defaults to 10.
    """
    while True:
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            logging.info(f"Current CPU Usage: {cpu_percent}%")

            if cpu_percent > threshold:
                logging.warning("CPU usage exceeds threshold!")
                alert_high_cpu_usage()

            time.sleep(interval)
        except KeyboardInterrupt:
            logging.info("Stopping CPU monitor...")
            break
        except Exception as e:
            logging.error(f"Error: {str(e)}")

def alert_high_cpu_usage():
    """
    Alert the user when CPU usage exceeds the threshold.

    This function uses platform-specific commands to alert the user.
    """
    current_platform = platform.system()
    if current_platform == "Darwin":  # macOS
        os.system("say 'High CPU usage detected!'")
    elif current_platform == "Windows":
        os.system("powershell -Command Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('High CPU usage detected!', 'Alert', 0, [System.Windows.Forms.MessageBoxIcon]::Warning)")
    elif current_platform == "Linux":
        os.system("notify-send 'High CPU usage detected!'")

if __name__ == "__main__":
    threshold_percent = 80  # Define the CPU usage threshold in percentage
    interval_seconds = 10  # Define the time interval between checks in seconds
    monitor_cpu_threshold(threshold_percent, interval_seconds)