# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 11:47:16 2016

@author: AbreuLastra_Work
"""

import pandas as pd
import sqlite3 as lite
import collections
import datetime
import requests


url = "https://api.forecast.io/forecast/"
apikey = "ad90e19efd02c37d39053e7481891792/"


end_date = datetime.datetime.now()
query_date = datetime.datetime.now() - datetime.timedelta(days = 30)

cities = { "Atlanta": '33.762909,-84.422675',
            "Austin": '30.303936,-97.754355',
            "Boston": '42.331960,-71.020173',
            "Chicago": '41.837551,-87.681844',
            "Cleveland": '41.478462,-81.679435'
        }
        

con = lite.connect('weather.db')
cur = con.cursor()


#First we instantiate our table
#Here we name the colummns, for time and the five cities
with con:
    cur.execute('DROP TABLE IF EXISTS daily_temp')    
    cur.execute('CREATE TABLE daily_temp (day_of_reading INT, Atlanta TEXT , Austin TEXT, Boston TEXT, Chicago TEXT, Cleveland TEXT);')

#Here, ther rows, for 30 days of observations
with con:
    while query_date < end_date:
        cur.execute('INSERT INTO daily_temp(day_of_reading) VALUES (?)', (int(query_date.strftime('%s')),))
        query_date += datetime.timedelta(days=1)
        
#Second, we populate the table

for k,v in cities.iteritems():
    query_date = end_date - datetime.timedelta(days=30)
    while query_date < end_date:
        r = requests.get(url + apikey + v + "," + query_date.strftime('%Y-%m-%dT%H:%M:%S'))                
    
        with con:
            cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))
        query_date += datetime.timedelta(days=1)
        print(v)
        print(query_date)
con.close()