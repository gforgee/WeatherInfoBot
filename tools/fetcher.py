import os
import requests
from datetime import datetime

DEFAULT_CITY = 'WARSAW'
DEFAULT_LAT = 52.22
DEFAULT_LON = 20.98
DEFAULT_LANG = 'pl'
WEATHER_EMOJI_MAP = {
    "bezchmurnie": "☀️",
    "pochmurno": "☁️",
    "zachmurzenie małe": "🌤️",
    "częściowe zachmurzenie": "⛅",
    "zachmurzenie umiarkowane": "⛅",
    "zachmurzenie duże": "☁️",
    "przeważnie pochmurno": "🌥️",
    "rozproszone chmury": "🌤️",
    "duże zachmurzenie z przejaśnieniami": "🌥️",
    "zachmurzenie całkowite": "☁️",
    "mgła": "🌫️",
    "zamglenie": "🌫️",
    "mżawka": "🌦️",
    "lekkie opady deszczu": "🌧️",
    "umiarkowane opady deszczu": "🌧️",
    "silne opady deszczu": "🌧️",
    "burza": "🌩️",
    "burza z deszczem": "⛈️",
    "śnieg": "❄️",
    "lekkie opady śniegu": "🌨️",
    "marznący deszcz": "🌧️❄️",
    "zadymka śnieżna": "🌨️🌬️",
    "wiatr": "💨",
    "piasek": "🏜️",
    "pył": "🌪️",
    "tornado": "🌪️",
    "dym": "💨",
    "popiół wulkaniczny": "🌋",
    "nieznana pogoda": "❓"
}


def fetch_weather(city: str = DEFAULT_CITY, lat: float = DEFAULT_LAT, lon: float = DEFAULT_LON,
                  lang: str = DEFAULT_LANG):
    # Read api key
    api_key = os.getenv('API_KEY')
    # Fetch data from openWeather
    if not api_key:
        raise Exception('API key not set')
    API_BASE_URL = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&lang={lang}'
    try:
        response = requests.get(API_BASE_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'[Error] Couldnt get weather data {e}')
        return {}


def parse_weather_data(data: dict, city: str) -> str:
    if not data or "main" not in data:
        return "Missing weather data"

    try:
        description = data['weather'][0]['description']
        emoji = WEATHER_EMOJI_MAP.get(description.lower(), "🌈")
        feel_like = float(data['main']['feels_like']) - 273.15
        temp_min = float(data['main']['temp_min']) - 273.15
        temp_max = float(data['main']['temp_max']) - 273.15
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        return (
            f"Raport dla dnia {datetime.now().strftime('%D:%H:%M:%S')}\n"
            f"📍 Pogoda dla {city}:\n"
            f"{emoji} {description.capitalize()}\n"
            f"🌡️ Odczuwalna temperatura: {feel_like:.2f}°C\n"
            f"🧊 Temperatura min: {temp_min:.2f}:C\n"
            f"🔥 Temperatura maks: {temp_max:.2f}°C\n"
            f"💧 Wilgotność: {humidity}%\n"
            f"💨 Wiatr: {wind_speed} m/s\n")

    except (KeyError, IndexError, TypeError) as e:
        return f"Error while parsing weather data: {e}"


def get_coordinates(city: str, limit: int = 2):
    # Get api key
    api_key = os.getenv('API_KEY')
    # Fetch data from openWeather
    geo_api_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city},pl&limit={limit}&appid={api_key}'
    try:
        response = requests.get(geo_api_url)
        response.raise_for_status()
        data = response.json()
        if data:
            lon = data[0]['lon']
            lat = data[0]['lat']
            return lat, lon
        else:
            print("❌ Location not found.")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f'[Error] Couldnt get weather data {e}')
        return {}
