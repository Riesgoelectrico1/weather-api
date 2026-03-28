import requests
from django.conf import settings


OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather_data(city):
    """
    Consulta la API de OpenWeatherMap para una ciudad dada.
    Retorna un dict con temperature y humidity, o lanza una excepción.
    """
    api_key = settings.OPENWEATHER_API_KEY

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    response = requests.get(OPENWEATHER_URL, params=params, timeout=10)

    if response.status_code == 404:
        raise ValueError(f"Ciudad '{city}' no encontrada.")

    if response.status_code == 401:
        raise PermissionError("API key inválida o no autorizada.")

    response.raise_for_status()

    data = response.json()
    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
    }
