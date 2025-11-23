import hashlib
import sqlite3

class URLShortener:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls
            (short_url TEXT PRIMARY KEY, original_url TEXT)
        ''')
        self.conn.commit()

    def shorten_url(self, original_url: str) -> str:
        # Generate a short URL using hashlib
        short_url = hashlib.sha256(original_url.encode()).hexdigest()[:6]
        self.cursor.execute('INSERT INTO urls VALUES (?, ?)', (short_url, original_url))
        self.conn.commit()
        return short_url

    def get_original_url(self, short_url: str) -> str | None:
        self.cursor.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,))
        result = self.cursor.fetchone()
        return result[0] if result else None

def main():
    url_shortener = URLShortener('urls.db')
    
    while True:
        print("\n1. Shorten URL")
        print("2. Get Original URL")
        print("3. Quit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            original_url = input("Enter the URL to shorten: ")
            short_url = url_shortener.shorten_url(original_url)
            print(f"Short URL: {short_url}")
        elif choice == '2':
            short_url = input("Enter the short URL: ")
            original_url = url_shortener.get_original_url(short_url)
            if original_url:
                print(f"Original URL: {original_url}")
            else:
                print("URL not found")
        elif choice == '3':
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main()