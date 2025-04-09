import asyncio
import os

from utils.config import config
from discord import Intents, Client
from utils.users_init import add_city, init_users
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

users = init_users() # Making the dict -> {id:{'cities': 'Krakow','counter': 0,'tasks':None}}
print(f'Users dict: {users}')

intents = Intents.default()
client = Client(intents=intents)


@client.event
async def on_ready():
    print(f'BOT is online -> {client.user}')
    await send_welcome_mssg()

#{id:{'cities': 'Krakow','counter': 0,'tasks':None}}
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$city') and users[message.author.id]['cities'] != '':
        z = message.content[len('$city '):]
        for char in message.content[z]:
            if char in '.()[]{}/\<>!@#$%^&*-_=+`~;:?|':
                await message.channel.send(
                    f'Dear Human you can\'t use {char} in your city name.')
                return
            elif char == ',':
                pass
        add_city(message.author.id, z.capitalize())
        await message.channel.send(
            f'Dear Human your city is added \'{z}\'')
        print(f'{message.author.name} added {z} to dict', users[message.author.id])

    if message.content.startswith('$start') and users[message.author.id]['counter'] == 0:
        await enable_dm(message.author.id)
        users[str(message.author.id)][0] += 1
        await message.channel.send(
            f'Dear Human you have started the weather forecast if you want to make changes write $stop')
    elif message.content.startswith('$start') and users[message.author.id]['counter'] != 0:
        await message.channel.send(
            f'Dear Human you have already started the weather forecast please write $stop to stop and make changes')
    elif message.content.startswith('$start') and users[message.author.id]['cities'] == '':
        await message.channel.send(
            f'Dear Human you have not added city please write $city <miasto>')

    if message.content.startswith('$stop') and users[message.author.id]['counter'] != 0:
        await stop_dm(message.author.id)
        users[str(message.author.id)][0] -= 1
    elif message.content.startswith('$stop') and users[message.author.id]['counter'] == 0:
        await message.channel.send(
            f'Dear Human you have not started the weather forecast please write $start')



async def enable_dm(user_id):
    await client.wait_until_ready()

    async def send_weather_updates():
        while not client.is_closed():
            try:
                user = await client.fetch_user(user_id)
                if user_id in users:
                    for city in users[user_id]['cities']:
                        await user.send(config(city))
                else:
                    print(f'[Error] main.py -> enable_dm() -> Unknown user {user_id}')
                print(f'Sent message to {user.name}')
            except Exception as e:
                print(f'[Error]Could not send data to ID:{user_id} ({user.name}): {e}')
            await asyncio.sleep(86400)

    users[user_id]['tasks'] = asyncio.create_task(send_weather_updates())
    print(users)


async def stop_dm(user_id: int):
    if user_id in users:
        if users[user_id]:
            for task in users[user_id]:
                task.cancel()
            users[user_id].clear()
            print(f'Stopped sending messages to {user_id}')
    else:
        print(f'[Error] main.py -> stop_dm() -> Unknown user {user_id}')


async def send_welcome_mssg():
    for user_ids in users:
        try:
            user = await client.fetch_user(user_ids)
            await user.send(
                'Welcome Human:\n$city <miasto> <- dodajesz miasta do sprawdzenia pogody oddzielajac przecinkiem,\n$start <- codzienna rutyna ')
            print(f'Sent welcome message to  {user_ids} ({user.name})') # todo change to english version
        except Exception as e:
            print(f'[Error] Couldnt not send welcome message to ID {user_ids} ({user.name}): {e}')


client.run(TOKEN)
