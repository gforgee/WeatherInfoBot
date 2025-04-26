import asyncio
import os
from discord import Intents, Client

from utils.config import config
from utils.users_init import init_users
from utils.dateprinter import print_date
from utils.cities import add_city
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
date = print_date()
users = init_users()  # Making the dict -> {id:{'cities': 'Krakow','counter': 0,'tasks':None}}
print(f'Users dict: {users}')

intents = Intents.default()
client = Client(intents=intents)


@client.event
async def on_ready():
    print(f'({date})  BOT is online -> {client.user}')
    await send_welcome_mssg()


# {id:{'cities': 'Krakow','counter': 0,'tasks':None}}
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$city'):
        z = message.content[len('$city '):]
        adding_info = add_city(users, z, message.author.id)
        if isinstance(adding_info, str):
            await message.channel.send(f'Dear Human, the city "{z}" is already in the forecast.')
        else:
            await message.channel.send(
                f'Dear Human i shall add city/cities to the forecast -> {z}')
        print(f'({date})  user {message.author.id} ({message.author.name}) added {z} to dict',
              users[message.author.id]['cities'])

    elif message.content.startswith('$start'):
        if users[message.author.id]['counter'] == 0:
            if not users[message.author.id]['cities']:
                await message.channel.send(
                    f'Dear Human you have not added city please write $city <city-name>')
            else:
                await enable_dm(message.author.id)
                users[message.author.id]['counter'] += 1
                await message.channel.send(
                    f'Dear Human you have started the weather forecast\n\n')
        elif users[message.author.id]['counter'] != 0:
            await message.channel.send(
                f'Dear Human you have already started the weather forecast please write $stop to stop and make changes')
        else:
            print(
                f'({date})  {message.author.id} ({message.author.name}) should not start the forecast without city')

    elif message.content.startswith('$stop'):
        if users[message.author.id]['counter'] != 0:
            await stop_dm(message.author.id)
            users[message.author.id]['counter'] -= 1
            await message.channel.send(
                f'Dear Human you have stopped the weather forecast\n\n')
        elif users[message.author.id]['counter'] == 0:
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
                    print(f'({date}) [Error] main.py -> enable_dm() -> Unknown user {user_id}')
                print(f'({date})  Sent message to {user.name}')
            except Exception as e:
                print(f'({date})  [Error]Could not send data to ID:{user_id} ({user_id.name}): {e}')
            await asyncio.sleep(86400)

    users[user_id]['tasks'] = asyncio.create_task(send_weather_updates())
    print(f'({date})  User {user_id} created a task (started forecast): {users[user_id]["tasks"]}')


async def stop_dm(user_id: int):
    if user_id in users:
        if users[user_id]:
            if users[user_id]['tasks']:
                users[user_id]['tasks'].cancel()
                users[user_id]['tasks'] = None
            print(f'({date})  Stopped sending messages to {user_id}')
    else:
        print(f'({date})  [Error] main.py -> stop_dm() -> Unknown user {user_id}')


async def send_welcome_mssg():  # TODO this function should be called only once not after restart
    for user_ids in users:
        try:
            user = await client.fetch_user(user_ids)
            await user.send(
                'Welcome Human:\n$city <miasto> <- dodajesz miasta do sprawdzenia pogody oddzielajac przecinkiem,\n$start <- codzienna rutyna ')
            print(f'({date})  Sent welcome message to  {user_ids}')  # todo change to english version
        except Exception as e:
            print(f'({date})  [Error] Couldnt not send welcome message to ID {user_ids} {e}')


client.run(TOKEN)
