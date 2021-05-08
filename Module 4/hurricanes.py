import requests
import sqlite3
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

#Get the html page from wikipedia
r = requests.get('https://en.wikipedia.org/wiki/Atlantic_hurricane_season')
soup = BeautifulSoup(r.text, 'html.parser')
with open("hurricane.html", "w", encoding='utf-8') as file:
    file.write(str(soup))
	
#Create a place to store the data
data = []

#Get the tables that have this class
my_table = soup.find_all('table',{'class':'wikitable sortable'})

#Read through each row in the table and take the value of each element
for table in my_table:
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
		
#The tables have different column sizes. I can't figure out what to do about them
#This different column sizes is causing all of my subsequent results to be wrong.
#
pd.set_option('display.max_rows',300)
df = pd.DataFrame(data)

df.dropna(how = 'all',inplace = True)
df.drop(range(190,242),axis = 0,inplace = True)
df = df.loc[df[0] != 'Total',:]
df.columns = ['year','num_tropical_cyclones','num_tropical_storms','num_hurricanes','num_major_hurricanes','deaths','damage_usd','strongest_storm','retired_names','notes']

#Creating sqlalchemy connection and writing the dataframe to the database
engine = create_engine('sqlite:///hurricanes.db', echo=False)

#Creating a table with the dataframe data
df.to_sql('atlantic_hurricanes', con=engine, if_exists='replace')