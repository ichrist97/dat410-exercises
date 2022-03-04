# 7 Dialogue systems

The chatbot uses three public APIs for its tasks.

In order to use them you must generate your own API keys from the API providers:

- AlphaVantage (Finance)
- OpenWeather (Weather)
- Google Places API (Places)

## Set the API keys

Create a `.env` file containing the following keys:

```
WEATHER_API_KEY="foo"
PLACES_API_KEY="bar"
FINANCE_API_KEY="foobar"
```