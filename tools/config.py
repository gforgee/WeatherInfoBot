from dotenv import load_dotenv
from tools.fetcher import fetch_weather, parse_weather_data, get_coordinates

load_dotenv()


def config(city):
    lang = 'pl'
    # Pobierz dane
    lat, lon = get_coordinates(city)
    data = fetch_weather(city, lat, lon, lang)
    msg = parse_weather_data(data, city)
    return msg
