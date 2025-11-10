import discord
import os
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    greetings = ['hello', 'hi', 'hey', 'yo', 'salut', 'hola']
    if any(message.content.lower().startswith(greet) for greet in greetings):
        responses = [
            'Hello!',
            'Hi there!',
            'Hey!',
            'Yo!',
            'Salut!',
            'Hola!',
            'Greetings!',
            'What\'s up?'
        ]
        await message.channel.send(random.choice(responses))

client.run(TOKEN)