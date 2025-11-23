import tweepy
import sqlite3
from sqlite3 import Error

# Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Function to connect to the SQL Database
def sql_connection():
    try:
        con = sqlite3.connect('tweetsDatabase.db')
        return con
    except Error:
        print(Error)

# Function to create table
def sql_table(con: sqlite3.Connection):
    cursorObj = con.cursor()
    cursorObj.execute(
        "CREATE TABLE IF NOT EXISTS tweets(hashtag text, tweet text)")
    con.commit()

# Function to insert into table
def sql_insert(con: sqlite3.Connection, entities: 'tuple'):
    cursorObj = con.cursor()
    cursorObj.execute(
        'INSERT INTO tweets(hashtag, tweet) VALUES(?, ?)', entities)
    con.commit()

# Function to fetch tweets from database
def sql_fetch(con: sqlite3.Connection):
    searchHashtag = input("\nEnter hashtag whose tweets you want to display: ")
    isEmptySearch = True
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM tweets')
    rows = cursorObj.fetchall()

    print("\n")

    for row in rows:
        if (searchHashtag in row):
            print(row[1]+'\n')
            isEmptySearch = False

    if (isEmptySearch):
        print("\nNo tweets with #"+searchHashtag+" fetched into database \n")

# Function to delete tweets
def delete_tweets():
    # Path to the extracted Twitter Archive JSON file
    archive_path = "PATH_TO_YOUR_TWITTER_ARCHIVE/data/js/tweets/"

    # Delete all tweets
    with open(archive_path + "tweet.js", "r") as file:
        tweets = json.load(file)

        for tweet in tweets:
            tweet_id = tweet["tweet"]["id_str"]
            try:
                api.destroy_status(tweet_id)
                print(f"Deleted tweet with ID: {tweet_id}")
            except tweepy.TweepError as e:
                print(f"Failed to delete tweet with ID: {tweet_id}\nError: {e}")

def main():
    con = sql_connection()
    sql_table(con: sqlite3.Connection)

    while True:
        print("\n1. Fetch tweets")
        print("2. Search tweets")
        print("3. Delete tweets")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            hashTag = input("\nEnter hashtag to search: ")
            numberOfTweets = int(input("How many tweets do you want to fetch? "))
            search_words = "#"+hashTag
            new_search = search_words + " -filter:retweets"

            try:
                for tweet in tweepy.Cursor(api.search, q=new_search, count=5, lang="en", since_id=0).items(numberOfTweets):
                    entities = (hashTag, tweet.text)
                    sql_insert(con, entities)
                print("Saved successfully in Database")
            except Error:
                print(Error)
        elif choice == "2":
            sql_fetch(con)
        elif choice == "3":
            delete_tweets()
        elif choice == "4":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()