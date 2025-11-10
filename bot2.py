import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(aliases=['hi', 'hey', 'yo', 'salut', 'hola', 'greetings'])
async def hello(ctx):
    responses = [
        'Hello!',
        'Hi there!',
        'Hey!',
        'Yo!',
        'Salut!',
        'Hola!',
        'Greetings!',
        "What's up?"
    ]
    await ctx.send(random.choice(responses))

bot.run(TOKEN)