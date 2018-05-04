# -*- coding: utf-8 -*-
"""
This file represents the Data-wrangling part organized according to BigData3 lessons
"""
#https://github.com/jpatokal/openflights/blob/master/data/airlines.dat

import pandas as pd
import os

os.chdir('dataset') #set working directory

location = 'Extracted_dataset/'
types = {'YEAR': object, 'MONTH': object, 'DAY': object, 'DAY_OF_WEEK': int, 'AIRLINE': object,
         'FLIGHT_NUMBER': int, 'TAIL_NUMBER': object, 'ORIGIN_AIRPORT': object, 
         'DESTINATION_AIRPORT': object, 'SCHEDULED_DEPARTURE': int, 'DEPARTURE_TIME': float,
         'DEPARTURE_DELAY': float, 'TAXI_OUT': float, 'WHEELS_OFF': float,
         'SCHEDULED_TIME': float, 'ELAPSED_TIME': float, 'AIR_TIME': float,
         'DISTANCE': int, 'WHEELS_ON': float, 'TAXI_IN': float,
         'SCHEDULED_ARRIVAL': int, 'ARRIVAL_TIME': float, 'ARRIVAL_DELAY': float,
         'DIVERTED': int, 'CANCELLED': int, 'CANCELLATION_REASON': object,
         'AIR_SYSTEM_DELAY': float, 'SECURITY_DELAY': float, 'AIRLINE_DELAY': float,
         'LATE_AIRCRAFT_DELAY': float, 'WEATHER_DELAY': float}
   
df = pd.read_csv(location+'flights.csv',
     dtype=types)

df['DATE'] = df['YEAR'] + "-" + df['MONTH'] + "-" + df['DAY']

df = df[['DATE', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER', 'ORIGIN_AIRPORT',
         'DESTINATION_AIRPORT', 'DEPARTURE_TIME', 'ARRIVAL_TIME']]

df['DEPARTURE_TIME'] = pd.to_datetime((df['DEPARTURE_TIME'].abs() // 100 * 60) + (df['DEPARTURE_TIME'].abs() % 100), unit='m')
df['DEPARTURE_TIME'] = df['DEPARTURE_TIME'].astype(str).str.extract('(..:..:..)', expand=True)
df['ARRIVAL_TIME'] = pd.to_datetime((df['ARRIVAL_TIME'].abs() // 100 * 60) + (df['ARRIVAL_TIME'].abs() % 100), unit='m')
df['ARRIVAL_TIME'] = df['ARRIVAL_TIME'].astype(str).str.extract('(..:..:..)', expand=True)

df = df.set_index('DATE')

df.to_csv('Modified_dataset/2015.csv')

print('Done!')