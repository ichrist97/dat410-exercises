import os
import requests
from spacy import Language
from typing import Union
from dotenv import load_dotenv

# load api keys
load_dotenv()

FINANCE_API_KEY = os.getenv("FINANCE_API_KEY")
assert FINANCE_API_KEY, "No Finance API key specified"


def handle_stock(statement: Language) -> str:
    # find stock name
    stock = None
    for ent in statement.ents:
        if ent.label_ == "ORG":  # organization
            stock = ent.text
            break

    # missing entity
    if stock == None:
        return "You need to tell a stock"

    stock_price = get_stock_price(stock)
    if stock_price != None:
        return f"Last day the stock price of {stock} was: ${stock_price}"
    return "Something went wrong"


def get_stock_price(stock_name: str) -> Union[str, None]:
    # map company name to stock name to stock symbol
    # TODO

    # call finance api
    stock_symbol = stock_name
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={FINANCE_API_KEY}&outputsize=compact"
    response = requests.get(url)
    response_dict = response.json()

    # extract stock price
    price = response_dict["Time Series (Daily)"].values()[0]["4. close"]

    if response.status_code == 200:
        return f"${round(price, 2)}"

    print("[!] HTTP {0} calling [{1}]".format(response.status_code, url))
    return None


def map_stock_symbol(stock_name: str) -> str:
    # TODO
    pass
