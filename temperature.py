# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 14:01:55 2016

@author: AbreuLastra_Work
"""


import pandas as pd
import sqlite3 as lite
import collections
import datetime


con = lite.connect('weather.db')
cur = con.cursor()

df = pd.read_sql_query('SELECT * FROM daily_temp ORDER BY day_of_reading', con, index_col='day_of_reading')

temp_change = collections.defaultdict(int)
for col in df.columns:    
    city_values = df[col].tolist()
    city_values = [float(i) for i in city_values]
    city = col
    max_temp_delta = 0
    for k, v in enumerate(city_values):
        if k < len(city_values) - 1:
            max_temp_delta += abs(city_values[k] - city_values[k+1])
    temp_change[city] = max_temp_delta


def citywithmaxval(d):
    """Find the city with the biggest with the greatest change"""
    return max(d, key=lambda k: d[k])
    
max_city = citywithmaxval(temp_change)

print(max_city)

