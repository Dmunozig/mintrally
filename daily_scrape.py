import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from sqlalchemy import create_engine

url = 'https://rally.io/creator/'

# Making a request to the URL
response = requests.get(url)
# PARSE the response with BS
soup = BeautifulSoup(response.content, "html.parser")

# Scraping creator content from json
data = soup.find(id='__NEXT_DATA__').contents[0]
import json
data_dict = json.loads(data)

# Total creators
total_creators = data_dict['props']['pageProps']['data']['getDetailedCreatorInformation']['totalCreators']

# Going deeper into creator dictionary
dict_summary = data_dict['props']['pageProps']['data']['getDetailedCreatorInformation']['detailedCreatorInformation']

# Lists to take in data
tot_coins = []
creators = []
prices = []
support_volume = []
supporters = []
rly_backing = []
tot_transactions = []
symbols = []
start_price = []
user_id = []

for creator in range(0,total_creators-1):
    tot_coins.append(dict_summary[creator]['coinSummary']['totalCoins'])
    tot_transactions.append(dict_summary[creator]['coinSummary']['totalTransaction'])
    supporters.append(dict_summary[creator]['coinSummary']['totalSupporters'])
    support_volume.append(dict_summary[creator]['coinSummary']['totalSupportVolume'])
    rly_backing.append(dict_summary[creator]['coinSummary']['totalRLYBacking'])
    symbols.append(dict_summary[creator]['coinSummary']['symbol'])
    prices.append(dict_summary[creator]['coinSummary']['price'])
    creators.append(dict_summary[creator]['data']['creatorPreferredName'])
    start_price.append(dict_summary[creator]['data']['startingPrice'])
    user_id.append(dict_summary[creator]['data']['rnbUserId'])

# Add a Date to log date of scrape
from datetime import date
today = date.today()

# Create dataframe with scraped information
df = pd.DataFrame({"Day":today,"Price":prices, "Support Volume": support_volume, "Supporters":supporters, "$RLY Backing": rly_backing,"Total Coins":tot_coins, "Total Transactions": tot_transactions, "Symbol" :symbols,"Starting Price":start_price, "User ID":user_id}, index = creators)

#import the relevant sql library 
from sqlalchemy import create_engine
# link to your database
terminal_command  = os.popen('heroku config').readlines()
print(terminal_command)
# DATABASE_URL = terminal_command[1].split()[1]
# engine = create_engine(DATABASE_URL, echo = False)

# attach the data frame (df) to the database with a name of the table; the name can be whatever you like
# df.to_sql('daily_creators', con = engine, if_exists='append') 