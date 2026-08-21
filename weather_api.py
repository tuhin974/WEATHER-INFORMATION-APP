import os
from datetime import datetime

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city):
    """
    Fetch current weather information for a city
    from the OpenWeatherMap API.
    """

    if not API_KEY:
        return {
            "success": False,
            "error": "API key is not configured."
        }

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        if response.status_code == 401:
            return {
                "success": False,
                "error": "Invalid OpenWeatherMap API key."
            }

        if response.status_code == 404:
            return {
                "success": False,
                "error": f"City '{city}' was not found."
            }

        if response.status_code == 429:
            return {
                "success": False,
                "error": "API request limit exceeded. Please try again later."
            }

        response.raise_for_status()

        data = response.json()

        weather_data = {
            "City": data["name"],
            "Country": data["sys"]["country"],
            "Temperature": data["main"]["temp"],
            "Feels Like": data["main"]["feels_like"],
            "Humidity": data["main"]["humidity"],
            "Pressure": data["main"]["pressure"],
            "Wind Speed": data["wind"]["speed"],
            "Weather": data["weather"][0]["main"],
            "Description": data["weather"][0]["description"],
            "Icon": data["weather"][0]["icon"],
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return {
            "success": True,
            "data": weather_data
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Weather API request timed out."
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Unable to connect to the weather service."
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Weather API error: {e}"
        }

    except (KeyError, TypeError, ValueError):
        return {
            "success": False,
            "error": "Unexpected data received from the weather API."
        }