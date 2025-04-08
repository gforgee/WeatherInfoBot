from dotenv import load_dotenv
import os

from tools.fetcher import fetch_weather, parse_weather_data
from tools.message import send_weather_message

load_dotenv()
api_key = os.getenv('API_KEY')
city = 'Czaplinek'
lang = 'pl'
lat = 53.52
lon = 16.17
# Pobierz dane
data = fetch_weather(city, lat, lon, lang)
msg = parse_weather_data(data, city)

# Numer telefonu (z .env)
phone_number = os.getenv("WHATSAPP_NUMBER")

# Ustaw godzinę i minutę testu
from datetime import datetime, timedelta

now = datetime.now() + timedelta(minutes=1)
hour = now.hour
minute = now.minute + 1


# Wyślij testową wiadomość
send_weather_message(msg, phone_number, hour, minute)
