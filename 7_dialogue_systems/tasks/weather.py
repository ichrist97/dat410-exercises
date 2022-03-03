import os
import requests
from spacy import Language
from typing import Union
from dotenv import load_dotenv

# load api keys
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
assert WEATHER_API_KEY, "No Weather API key specified"


def handle_weather(statement: Language) -> str:
    # find city name by spacy named entity recognition
    city = None
    for ent in statement.ents:
        if ent.label_ == "GPE":  # geopolitical entity
            city = ent.text
            break

    # no entity found
    if city == None:
        return "You need to tell a city"

    city_weather = get_weather(city)
    if city_weather != None:
        return f"In {city} the current weather is: {city_weather}"
    else:
        return "Something went wrong"


def get_weather(city_name: str) -> Union[str, None]:
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}"
    response = requests.get(api_url)
    response_dict = response.json()
    weather_desc = response_dict["weather"][0]["description"]
    weather_temp_kelvin = response_dict["main"]["temp"]
    weather_temp_celsius = round(weather_temp_kelvin - 273.15)
    weather = f"{weather_desc} at {weather_temp_celsius} °C"

    if response.status_code == 200:
        return weather
    else:
        print("[!] HTTP {0} calling [{1}]".format(response.status_code, api_url))
        return None
