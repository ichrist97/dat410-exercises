import spacy
from spacy import Language
from tasks.places import handle_place
from tasks.weather import handle_weather
from tasks.finance import handle_stock
from tasks.help import handle_help
from typing import List

# load language model
nlp = spacy.load("en_core_web_md")

"""
Tasks:
- weather forecast
- find a location
- find stock price
"""

# maps intents to actions
INTENT_HANDLER = {
    "weather": handle_weather,
    "place": handle_place,
    "stock": handle_stock,
    "help": handle_help,
}


def calc_similarities(tasks: List[Language], statement: Language):
    res = []
    # calc all similarities for the nlp tasks
    for key, lang in tasks:
        sim = lang.similarity(statement)
        res.append((key, sim))
    # sort by similarity ascending
    res.sort(key=lambda y: y[1])
    return res


def chatbot(statement: str) -> str:
    weather = ("weather", nlp("Current weather in a city"))
    place = ("place", nlp("Where is this place"))
    stock = ("stock", nlp("What is the stock price"))
    helper = ("help", nlp("What can this chatbot do?"))
    tasks = [weather, place, stock, helper]

    statement = nlp(statement)

    min_similarity = 0.7

    # calc similarities
    sims = calc_similarities(tasks, statement)
    intent_name, intent_sim = sims[-1]

    if intent_sim >= min_similarity:
        return INTENT_HANDLER[intent_name](statement)
    else:
        return "Sorry I don't know understand that. Please rephrase your statement"


def start() -> None:
    while True:
        phrase = input("How can I help you?\nType 'Exit' to exit the chatbot\n> ")

        # exit check
        if phrase.lower() == "exit":
            quit()

        # TODO ask for missing entities

        response = chatbot(phrase)
        print(response)


start()
