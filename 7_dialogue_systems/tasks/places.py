import os
import requests
from spacy import Language
from typing import Union
from dotenv import load_dotenv

# load api keys
load_dotenv()

PLACES_API_KEY = os.getenv("PLACES_API_KEY")
assert PLACES_API_KEY, "No Places API key specified"


def handle_place(statement: Language) -> str:
    # find location name by spacy named entity recognition
    location = None
    for ent in statement.ents:
        if ent.label_ == "GPE" or ent.label_ == "ORG":  # geopolitical entity
            location = ent.text
            break

    # no entity found
    if location == None:
        return "You need to tell a location"

    location_address = get_place(location)
    if location_address != None:
        return f"The address for {location} is: {location_address}"
    else:
        return "Something went wrong"


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
