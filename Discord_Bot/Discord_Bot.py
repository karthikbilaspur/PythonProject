import discord
from discord.ext import commands
import random

# Bot configuration
TOKEN = 'YOUR_BOT_TOKEN'
PREFIX = '!'

# Create bot instance
bot = commands.Bot(command_prefix=PREFIX)

# Event to indicate bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Command to ping the bot
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

# Command to say hello
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')

# Command to roll a dice
@bot.command(name='roll')
async def roll(ctx, sides=6):
    roll_result = random.randint(1, sides)
    await ctx.send(f'You rolled a {roll_result} on a {sides}-sided dice!')

# Command to generate a random joke
@bot.command(name='joke')
async def joke(ctx):
    jokes = [
        'Why was the math book sad? Because it had too many problems.',
        'Why did the scarecrow win an award? Because he was outstanding in his field.',
        'What do you call a fake noodle? An impasta.'
    ]
    await ctx.send(random.choice(jokes))

# Error handling for unknown commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command. Use !help for available commands.')

# Run the bot
bot.run(TOKEN)