from dotenv import load_dotenv
from utils.fetcher import fetch_weather, parse_weather_data, get_coordinates

load_dotenv()


def config(city):
    try:
        lang = 'pl'
        # Get longitude and latitude data
        lat, lon = get_coordinates(city)
        # Get weather data for longitude and latitude
        data = fetch_weather(city, lat, lon, lang)
        # Prepare message with data
        msg = parse_weather_data(data, city)
        return msg
    except Exception as e:
        return f'[Error] /utils -> config.py -> config() -> occured: {e}'
