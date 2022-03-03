import spacy
from tasks.places import get_place
from tasks.weather import get_weather

# load language model
nlp = spacy.load("en_core_web_md")

"""
Tasks:
- weather forecast
- find a restaurant / location
- find the next bus / tram
"""


def chatbot(statement):
    weather = nlp("Current weather in a city")
    statement = nlp(statement)

    min_similarity = 0.7
    if weather.similarity(statement) >= min_similarity:
        # find city name by spacy named entity recognition
        print(statement.ents)
        for ent in statement.ents:
            if ent.label_ == "GPE":  # geopolitical entity
                city = ent.text
                break
            else:
                return "You need to tell a city"

        city_weather = get_weather(city)
        if city_weather != None:
            return f"In {city} the current weather is: {city_weather}"
        else:
            return "Something went wrong"
    else:
        return "Sorry I don't know understand that. Please rephrase your statement"
