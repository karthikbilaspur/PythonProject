
import speedtest
import csv
import time
import statistics

def perform_speed_test():
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    download_speed = s.download() / (1024 * 1024)  # in Mbps
    upload_speed = s.upload() / (1024 * 1024)  # in Mbps
    ping = s.results.ping  # in seconds

    return download_speed, upload_speed, ping

def log_results(filename, results):
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'download_speed', 'upload_speed', 'ping']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(results)

def main():
    filename = 'speed_test_results.csv'
    num_runs = int(input("Enter the number of runs: "))
    interval = int(input("Enter the interval between runs (in seconds): "))
    threshold_download = float(input("Enter the download speed threshold (in Mbps): "))
    threshold_upload = float(input("Enter the upload speed threshold (in Mbps): "))

    download_speeds = []
    upload_speeds = []
    pings = []

    for i in range(num_runs):
        print(f"Run {i+1}...")
        download_speed, upload_speed, ping = perform_speed_test()
        print(f"Download Speed: {download_speed:.2f} Mbps")
        print(f"Upload Speed: {upload_speed:.2f} Mbps")
        print(f"Ping: {ping:.2f} seconds")

        log_results(filename, {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'download_speed': download_speed,
            'upload_speed': upload_speed,
            'ping': ping
        })

        download_speeds.append(download_speed)
        upload_speeds.append(upload_speed)
        pings.append(ping)

        if download_speed < threshold_download or upload_speed < threshold_upload:
            print("Speed below threshold! Check your connection.")

        if i < num_runs - 1:
            time.sleep(interval)

    print("\nAverage Speeds:")
    print(f"Download Speed: {statistics.mean(download_speeds):.2f} Mbps")
    print(f"Upload Speed: {statistics.mean(upload_speeds):.2f} Mbps")
    print(f"Ping: {statistics.mean(pings):.2f} seconds")

if __name__ == "__main__":
    main()