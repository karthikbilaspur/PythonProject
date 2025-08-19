import discord
from discord.ext import commands
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Bot configuration
TOKEN = 'YOUR_BOT_TOKEN'
PREFIX = '!'

# Load pre-trained model and tokenizer
model_name = 't5-base'
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create bot instance
bot = commands.Bot(command_prefix=PREFIX)

# Event to indicate bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Command to generate response
@bot.command(name='chat')
async def chat(ctx, *, message):
    input_ids = tokenizer.encode(message, return_tensors='pt')
    output = model.generate(input_ids, max_length=100)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    await ctx.send(response)

# Command to converse with the bot
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith(PREFIX):
        await bot.process_commands(message)
    else:
        input_ids = tokenizer.encode(message.content, return_tensors='pt')
        output = model.generate(input_ids, max_length=100)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        await message.channel.send(response)

# Run the bot
bot.run(TOKEN)
