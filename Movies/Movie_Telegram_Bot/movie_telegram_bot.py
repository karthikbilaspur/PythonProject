import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import decouple
import requests
from bs4 import BeautifulSoup

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = decouple.config("API_KEY")

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'What can this bot do?\n\nThis bot gives brief information about any movie from IMDb website'
        + '\nSend /name movie_name to know the genre and rating of the movie.\nSend /genre genre_name to'
        + 'get the list of movies belonging to that genre'
    )

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def get_movie_info(movie):
    """Get movie info from IMDb"""
    try:
        url = f"https://www.imdb.com/find?q={movie}&ref_=nv_sr_sm}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        movie_links = soup.find_all("a", href=True)
        movie_info = []
        for link in movie_links:
            href = link["href"]
            if href.startswith("/title/tt"):
                movie_url = f"https://www.imdb.com{href}"
                movie_response = requests.get(movie_url)
                movie_soup = BeautifulSoup(movie_response.text, "html.parser")
                title = movie_soup.find("title").text.replace("- IMDb", "")
                genres = [genre.text.strip() for genre in movie_soup.select("span.genre a")]
                rating = movie_soup.find("span", itemprop="ratingValue")
                if rating:
                    rating = rating.text
                else:
                    rating = "Not rated"
                movie_info.append({
                    "title": title,
                    "genres": genres,
                    "rating": rating,
                    "url": movie_url
                })
        return movie_info
    except Exception as e:
        logger.error(f"Error getting movie info: {e}")
        return None

def name(update, context):
    """Send the first 3 search results of the movie name in IMDb site when the command /name is issued."""
    try:
        movie = update.message.text.split(" ", 1)[1]
        movie_info = get_movie_info(movie)
        if movie_info:
            for info in movie_info[:3]:
                update.message.reply_text(
                    f"Title: {info['title']}\n"
                    f"Genres: {', '.join(info['genres'])}\n"
                    f"Rating: {info['rating']}\n"
                    f"URL: {info['url']}"
                )
        else:
            update.message.reply_text("No movies found")
    except Exception as e:
        logger.error(f"Error handling /name command: {e}")

def get_movies_by_genre(genre):
    """Get movies by genre from IMDb"""
    try:
        url = f"https://www.imdb.com/search/title/?genres={genre}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        movie_links = soup.find_all("a", href=True)
        movies = []
        for link in movie_links:
            href = link["href"]
            if href.startswith("/title/tt"):
                movie_url = f"https://www.imdb.com{href}"
                movie_title = link.text.strip()
                movies.append((movie_title, movie_url))
        return movies
    except Exception as e:
        logger.error(f"Error getting movies by genre: {e}")
        return None

def genre(update, context):
    """Send a list of movies when the command /genre is issued."""
    try:
        genre = update.message.text.split(" ", 1)[1]
        movies = get_movies_by_genre(genre)
        if movies:
            for movie in movies[:10]:
                update.message.reply_text(
                    f"{movie[0]}\n"
                    f"URL: {movie[1]}"
                )
        else:
            update.message.reply_text("No movies found")
    except Exception as e:
        logger.error(f"Error handling /genre command: {e}")

def get_movie_details(movie_url):
    """Get movie details from IMDb"""
    try:
        response = requests.get(movie_url)
        soup = BeautifulSoup(response.text, "html.parser")
        details = []
        for item in soup.find_all("div", class_="see-more"):
            details.append(item.text.strip())
        return details
    except Exception as e:
        logger.error(f"Error getting movie details: {e}")
        return None

def details(update, context):
    """Send movie details when the command /details is issued."""
    try:
        movie_url = update.message.text.split(" ", 1)[1]
        details = get_movie_details(movie_url)
        if details:
            update.message.reply_text("\n".join(details))
        else:
            update.message.reply_text("No details found")
    except Exception as e:
        logger.error(f"Error handling /details command: {e}")

def search_movies(query):
    """Search movies on IMDb"""
    try:
        url = f"https://www.imdb.com/find?q={query}&ref_=nv_sr_sm}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        movie_links = soup.find_all("a", href=True)
        movies = []
        for link in movie_links:
            href = link["href"]
            if href.startswith("/title/tt"):
                movie_url = f"https://www.imdb.com{href}"
                movie_title = link.text.strip()
                movies.append((movie_title, movie_url))
        return movies
    except Exception as e:
        logger.error(f"Error searching movies: {e}")
        return None

def search(update, context):
    """Send search results when the command /search is issued."""
    try:
        query = update.message.text.split(" ", 1)[1]
        movies = search_movies(query)
        if movies:
            for movie in movies[:10]:
                update.message.reply_text(
                    f"{movie[0]}\n"
                    f"URL: {movie[1]}"
                )
        else:
            update.message.reply_text("No movies found")
    except Exception as e:
        logger.error(f"Error handling /search command: {e}")

def get_genres():
    """Get list of genres"""
    try:
        url = "https://www.imdb.com/feature/genre/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        genres = []
        for item in soup.find_all("a", href=True):
            if item["href"].startswith("/search/title?genres="):
                genres.append(item.text.strip())
        return genres
    except Exception as e:
        logger.error(f"Error getting genres: {e}")
        return None

def genres(update, context):
    """Send list of genres when the command /genres is issued."""
    try:
        genres = get_genres()
        if genres:
            update.message.reply_text("\n".join(genres))
        else:
            update.message.reply_text("No genres found")
    except Exception as e:
        logger.error(f"Error handling /genres command: {e}")

def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("name", name))
    dp.add_handler(CommandHandler("genre", genre))
    dp.add_handler(CommandHandler("details", details))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(CommandHandler("genres.add_handler(genres))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()