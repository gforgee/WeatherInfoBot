import asyncio
import os
from tools.config import config
from discord import Intents, Client
from users_init import dodaj_miasto,init_users
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

users = init_users()
print(users)
intents = Intents.default()
client = Client(intents=intents)


@client.event
async def on_ready():
    print(f'BOT is online -> {client.user}')
    await wyslij_powitanie()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$miasto'):
        z = message.content[len('$miasto '):]
        dodaj_miasto(message.author.id, z)
        await message.channel.send(
            f'Szanowny Człowieku, jest mi niezmiernie miło dodać tę opcje do twoich miast,dzięki czemu otrzymasz niezbędne dane dot. tej pierdolonej pogody {z}')
        print(f'{message.author.name} added {z} to dict')
    if message.content.startswith('$start'):
        await enable_dm(message.author.id)


async def enable_dm(user_id):
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            user = await client.fetch_user(user_id)
            if str(user_id) in users:
                for city in users[str(user_id)]:
                    print(city)
                    await user.send(config(city))
            else:
                print(f'Nieznany user {user_id}')
            print(f'Wysłano wiadomość do {user.name}')
        except Exception as e:
            print(f'[Error]Nie udało się wysłać wiadomości do ID {user_id}: {e}')
        await asyncio.sleep(86400)


async def wyslij_powitanie():
    for user_ids in users:
        try:
            user = await client.fetch_user(user_ids)
            await user.send(
                'Dzień dobry napisz:\n$miasto {miasto} <-> dodajesz miasto do sprawdzania pogody,\n$start <- codzienna rutyna ')
            print(f'Wyslano powitalna wiadomosc do {user_ids}')
        except Exception as e:
            print(f'[Error]Nie udalo sie wyslac wiadomosci do ID {user_ids}')


client.run(TOKEN)


