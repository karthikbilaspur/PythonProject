import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import re

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define a few command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hi! I am your Telegram bot. How can I assist you?')

async def hi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /hi is issued."""
    await update.message.reply_text('Hi! I am telebot...How is it going.')

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /play is issued."""
    await update.message.reply_text("Let's have fun!Repeat this tongue twister 5 times:She sells seashells by the seashore.")

async def dog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a dog picture when the command /dog is issued."""
    url = image_urll()
    await update.message.reply_photo(photo=url)

async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a meme when the command /meme is issued."""
    img = image_url()
    await update.message.reply_photo(photo=img)

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send weather information when a city name is provided."""
    city = update.message.text
    response = requests.get("http://api.weatherapi.com/v1/current.json?key={}&q={}".format("2d3f4a2bd175414aa45175205221408", city)).json()
    await update.message.reply_text(format_response_to_human_readable(response))

def image_urll():
    extension = ['jpg', 'jpeg', 'png']
    ext = ''
    while ext not in extension:
        url = gett()
        ext = re.search("([^.]*)$", url).group(1).lower()
    return url

def gett():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def image_url():
    extension = ['jpg', 'jpeg', 'png']
    ext = ''
    while ext not in extension:
        img = get()
        ext = re.search("([^.]*)$", img).group(-(1)).lower()
    return img

def get():
    contents = requests.get('https://xkcd.com/info.0.json').json()
    img = contents['img']
    return img

def format_response_to_human_readable(response: dict) -> str:
    location = response["location"]
    current = response["current"]
    astronomy = response["forecast"]["forecastday"][0]["astro"]

    return "Weather Information for {}\n"\
           "Temperature: {}°C\n"\
           "Wind: {} kph, {}\n"\
           "Humidity: {}%\n"\
           "Pressure: {} mb\n"\
           "Sunrise: {}\n"\
           "Sunset: {}\n"\
           "Day Length: {} hours {} minutes".format(
               location["name"],
               current["temp_c"],
               current["wind_kph"],
               current["wind_dir"],
               current["humidity"],
               current["pressure_mb"],
               astronomy["sunrise"],
               astronomy["sunset"],
               astronomy["sunrise"],
               astronomy["sunset"],
               astronomy["moon_phase"]
           )

def main() -> None:
    """Start the bot."""
    application = ApplicationBuilder().token("YOUR-TOKEN-HERE").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hi", hi))
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CommandHandler("dog", dog))
    application.add_handler(CommandHandler("meme", meme))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, weather))

    application.run_polling()

if __name__ == '__main__':
    main()