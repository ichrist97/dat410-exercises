from spacy import Language


def handle_help(statement: Language) -> str:
    return "The chatbot can help you with the following topics:\n\
        1. Giving you a weather forecast\n\
        2. Address of some location\n\
        3. Telling you the latest stock price of some company\n"
