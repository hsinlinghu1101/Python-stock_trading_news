STOCK = "AMZN"

COMPANY_NAME = "Amazon.com Inc"

import config

stock_api = config.stock_api
news_api = config.news_api
account_sid = config.account_sid
auth_token = config.auth_token
twilio_phone = config.twilio_phone

import requests
import os

from twilio.rest import Client

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

response = requests.get(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&outputsize=compact&apikey={stock_api}")
data = response.json()

last_two = [date for date in data["Time Series (Daily)"]][:2]


last1_data = data["Time Series (Daily)"][last_two[0]]["4. close"]
last2_data = data["Time Series (Daily)"][last_two[1]]["4. close"]

diff_value = float(last1_data) - float(last2_data)
diff_percent = round(diff_value/float(last2_data)*100, 1)

client = Client(account_sid, auth_token)

increase = f"{STOCK}: 🔺{diff_percent}%"
decrease = f"{STOCK}: 🔻{abs(diff_percent)}%"

def send_msg(body_msg):
    message = client.messages \
        .create(
        body=body_msg,
        from_=twilio_phone,
        to='+13234048799'
    )
    print(message.sid)

if diff_percent < 0:
  send_msg(decrease)

else:
  send_msg(increase)

if diff_percent >= 5 or diff_percent <= -5:
    news = requests.get(url=f"http://newsapi.org/v2/everything?qInTitle={COMPANY_NAME}&apiKey={news_api}")
    news_data = news.json()
    for article in news_data["articles"][:3]:
      news_article = f"Headline: {article['title']}\nBrief: {article['description']}"
      send_msg(news_article)




## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 




