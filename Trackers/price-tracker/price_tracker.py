import requests
from bs4 import BeautifulSoup

TrackingInfo = dict[str, str]


class AmazonTracker:
    def __init__(self, tracking_id: str):
        self.tracking_id = tracking_id
        self.api_url = f"https://www.amazon.com/gp/tracking?orderId={tracking_id}&packageId=1"
        self.headers: dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def track_package(self) -> TrackingInfo:
        try:
            response = requests.get(self.api_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            tracking_info_elements = soup.select("div.a-box-group.a-spacing-base.shipment")
            tracking_info_list: list[TrackingInfo] = []
            for tracking_info in tracking_info_elements:
                tracking_status_element = tracking_info.find("span", class_="a-size-base")
                tracking_date_element = tracking_info.find("span", class_="a-size-base a-color-secondary")

                if tracking_status_element is None or tracking_date_element is None:
                    continue

                tracking_info_list.append({
                    "tracking_id": self.tracking_id,
                    "tracking_status": tracking_status_element.get_text(strip=True),
                    "tracking_date": tracking_date_element.get_text(strip=True),
                })

            if tracking_info_list:
                return tracking_info_list[0]

            return {
                "tracking_id": self.tracking_id,
                "message": "Tracking information not found",
            }
        except requests.exceptions.RequestException as e:
            return {
                "tracking_id": self.tracking_id,
                "message": f"Request failed: {e}",
            }

    def send_notification(self, tracking_info: TrackingInfo) -> None:
        try:
            tracking_id = tracking_info.get("tracking_id", "Unknown")
            tracking_status = tracking_info.get("tracking_status", "Unknown")
            tracking_date = tracking_info.get("tracking_date", "Unknown")
            print(f"Tracking update for {tracking_id}: {tracking_status} on {tracking_date}")
        except Exception as e:
            print(f"Error sending notification: {e}")


def main() -> None:
    tracking_id = input("Enter your Amazon tracking ID: ")
    tracker = AmazonTracker(tracking_id)
    tracking_info = tracker.track_package()
    if "message" in tracking_info:
        print(tracking_info["message"])
    else:
        print(f"Tracking ID: {tracking_info.get('tracking_id', 'Unknown')}")
        print(f"Tracking Status: {tracking_info.get('tracking_status', 'Unknown')}")
        print(f"Tracking Date: {tracking_info.get('tracking_date', 'Unknown')}")
        tracker.send_notification(tracking_info)


if __name__ == "__main__":
    main()