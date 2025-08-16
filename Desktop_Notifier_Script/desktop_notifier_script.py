from plyer import notification
import requests
import xml.etree.ElementTree as ET
import time
import threading

# News Fetcher
class NewsFetcher:
    def __init__(self, rss_feed_url):
        self.rss_feed_url = rss_feed_url

    def fetch_news(self):
        try:
            resp = requests.get(self.rss_feed_url)
            root = ET.fromstring(resp.content)
            news_items = []
            for item in root.findall('./channel/item'):
                news = {}
                news['title'] = item.find('title').text
                news['description'] = item.find('description').text
                news_items.append(news)
            return news_items
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

# Desktop Notifier
class DesktopNotifier:
    def __init__(self):
        self.notifications = []

    def notify(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name="Desktop Notifier",
            timeout=10,
        )

    def add_notification(self, title, message):
        self.notifications.append((title, message))

    def display_notifications(self):
        for title, message in self.notifications:
            self.notify(title, message)

# Email, Message, Call Notifier
class CommunicationNotifier:
    def __init__(self):
        self.email_notifier = DesktopNotifier()
        self.message_notifier = DesktopNotifier()
        self.call_notifier = DesktopNotifier()

    def notify_email(self, subject, message):
        self.email_notifier.add_notification(f"Email: {subject}", message)

    def notify_message(self, sender, message):
        self.message_notifier.add_notification(f"Message from {sender}", message)

    def notify_call(self, caller):
        self.call_notifier.add_notification(f"Call from {caller}", "Incoming call")

# Main Function
def main():
    news_fetcher = NewsFetcher("http://www.hindustantimes.com/rss/topnews/rssfeed.xml")
    desktop_notifier = DesktopNotifier()
    communication_notifier = CommunicationNotifier()

    # Simulate notifications
    communication_notifier.notify_email("Meeting Reminder", "You have a meeting at 2 PM")
    communication_notifier.notify_message("John Doe", "Hey, how are you?")
    communication_notifier.notify_call("Jane Doe")

    while True:
        news_items = news_fetcher.fetch_news()
        for news in news_items:
            desktop_notifier.notify(news['title'], news['description'])
            time.sleep(15)  # wait 15 seconds before next notification

        communication_notifier.email_notifier.display_notifications()
        communication_notifier.message_notifier.display_notifications()
        communication_notifier.call_notifier.display_notifications()

        time.sleep(60)  # wait 1 minute before checking for new notifications

if __name__ == "__main__":
    main()