import os
import requests
from typing import Union
from dotenv import load_dotenv

# load api keys
load_dotenv()

PLACES_API_KEY = os.getenv("PLACES_API_KEY")
assert PLACES_API_KEY, "No Places API key specified"


def get_place(place_name: str) -> Union[str, None]:
    fields = "formatted_address"
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?fields={fields}&input={place_name}&inputtype=textquery&key={PLACES_API_KEY}"
    response = requests.get(url)
    response_dict = response.json()
    place = response_dict["candidates"][0]
    address = place["formatted_address"]

    if response.status_code == 200:
        return address
    else:
        print("[!] HTTP {0} calling [{1}]".format(response.status_code, url))
        return None
