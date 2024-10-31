import requests
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
STOCKS_API_KEY = os.environ.get('STOCKS_API_KEY')
TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

news_params = {
    "q": STOCK,
    "apiKey": NEWS_API_KEY,
    "pageSize": 3,
}

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCKS_API_KEY,
}

stock_response = requests.get("https://www.alphavantage.co/query", params=stock_params)
stock_response.raise_for_status()
response = requests.get("https://newsapi.org/v2/everything", params = news_params)
response.raise_for_status()

stock_data = stock_response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]
yesterday_price = float(stock_data_list[1]["4. close"])
yesterday_yesterday_price = float(stock_data_list[2]["4. close"])
difference = abs(yesterday_yesterday_price - yesterday_price)

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# if 5% change in difference
if difference / yesterday_price >= 5:
    print(f" {STOCK}: {difference:.2f}")
    print(F" {STOCK}: {yesterday_yesterday_price:.2f} to {yesterday_price:.2f}")
    for i in range(news_params["pageSize"]):
        title = response.json()["articles"][i]["title"]
        description = response.json()["articles"][i]["description"]
        message = client.messages.create(
            body=[title, description],
            from_="18333629439",
            to='your phone number'
        )
        print(f"Headline: {title}")
        print(f"Description: {description}")