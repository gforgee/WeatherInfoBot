import os

from tools.fetcher import fetch_weather, parse_weather_data
from tools.message import send_weather_message, schedule_daily_weather_message
from dotenv import load_dotenv

load_dotenv()

city = 'Czaplinek'
lang = 'pl'
phone_number = os.getenv('PHONE_NUMBER')
if not phone_number:
    raise ValueError("No phone number provided")
send_weather_message(fetch_weather(parse_weather_data()), phone_number)
# schedule_daily_weather_message(fetch_weather, parse_weather_data, phone_number)
