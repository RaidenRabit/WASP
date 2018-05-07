# -*- coding: utf-8 -*-
"""
This file represents the Data-wrangling part organized according to BigData3 lessons
"""

import pandas as pd
import os

os.chdir('dataset') #set working directory

location = 'Extracted_dataset/'
types = {'YEAR': int, 'MONTH': int, 'DAY': int, 'DAY_OF_WEEK': int, 'AIRLINE': object,
         'FLIGHT_NUMBER': int, 'TAIL_NUMBER': object, 'ORIGIN_AIRPORT': object, 
         'DESTINATION_AIRPORT': object, 'DEPARTURE_TIME': float, 'ARRIVAL_TIME': float,
         'SCHEDULED_DEPARTURE': int, 'DEPARTURE_DELAY': float, 'TAXI_OUT': float, 
         'WHEELS_OFF': float, 'SCHEDULED_TIME': float, 'ELAPSED_TIME': float, 
         'AIR_TIME': float, 'DISTANCE': int, 'WHEELS_ON': float, 'TAXI_IN': float,
         'SCHEDULED_ARRIVAL': int, 'ARRIVAL_DELAY': float, 'DIVERTED': int, 
         'CANCELLED': int, 'CANCELLATION_REASON': object, 'AIR_SYSTEM_DELAY': float, 
         'SECURITY_DELAY': float, 'AIRLINE_DELAY': float, 'LATE_AIRCRAFT_DELAY': float, 
         'WEATHER_DELAY': float}
   
df = pd.read_csv(location+'flights.csv',
     dtype=types)

df = df[['MONTH', 'DAY', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER', 
         'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 
         
         'DEPARTURE_TIME', 'ARRIVAL_TIME', 'DAY_OF_WEEK',
         'SCHEDULED_DEPARTURE', 'DEPARTURE_DELAY', 'TAXI_OUT', 
         'WHEELS_OFF', 'SCHEDULED_TIME', 'ELAPSED_TIME', 
         'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN',
         'SCHEDULED_ARRIVAL', 'ARRIVAL_DELAY', 'DIVERTED', 
         'CANCELLED', 'CANCELLATION_REASON', 'AIR_SYSTEM_DELAY', 
         'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 
         'WEATHER_DELAY']]

'''
#used to show where the airports are located in
#########################################
location = 'Modified_dataset/'
dfCollisionFix = pd.read_csv(location+'airports.csv')
dfCollisionFix = dfCollisionFix[['IATA', 'Country']]
dfCollisionFix.dropna(subset=['IATA'], inplace=True)

df = pd.merge(left = df, right = dfCollisionFix,  how='left', left_on=['ORIGIN_AIRPORT'], right_on = ['IATA'])
dfCollisionFix = 1;
df = df.drop(['ORIGIN_AIRPORT', 'IATA'], axis=1)
#########################################

df.to_csv('Modified_dataset/USA2015.csv')

print('Done!')
'''
########################################################################################
print('flights dataset cleaned')
location = 'Modified_dataset/'
types = {'REG': object, 'FLT': object, 'OPID': object, 'AIRPORT_ID': object}

dfCollision = pd.read_csv(location+'wildlife-collisions2015.csv',
                 parse_dates=['INCIDENT_DATE'],
                 dtype=types)

dfCollision['INCIDENT_DATE'] = dfCollision['INCIDENT_DATE'].astype(str).str.extract('(....-..-..)', expand=True)
dfCollision['Year'], dfCollision['Month'], dfCollision['Day'] = dfCollision['INCIDENT_DATE'].str.split('-').str
dfCollision = dfCollision.drop(['INCIDENT_DATE', 'Year'], axis=1)
dfCollision[['Month','Day']] = dfCollision[['Month','Day']].apply(pd.to_numeric)

dfCollisionFix = pd.read_csv(location+'airlines.csv')
dfCollisionFix = dfCollisionFix[['IATA', 'ICAO']]
dfCollisionFix.dropna(subset=['ICAO'], inplace=True)

dfCollision = pd.merge(left = dfCollision, right = dfCollisionFix,  how='left', left_on=['OPID'], right_on = ['ICAO'])
dfCollision = dfCollision.drop(['OPID', 'ICAO'], axis=1)
dfCollision = dfCollision.rename(columns={'IATA': 'airline'})

dfCollisionFix = pd.read_csv(location+'airports.csv')
dfCollisionFix = dfCollisionFix[['IATA', 'ICAO']]
dfCollisionFix.dropna(subset=['ICAO'], inplace=True)

dfCollision = pd.merge(left = dfCollision, right = dfCollisionFix,  how='left', left_on=['AIRPORT_ID'], right_on = ['ICAO'])
dfCollisionFix = 1;
dfCollision = dfCollision.drop(['AIRPORT_ID', 'ICAO'], axis=1)
dfCollision = dfCollision.rename(columns={'IATA': 'airport'})

########################################################################################
print('wildlife-collisions2015 dataset cleaned')
df['CRASHED'] = 0

def merge(left,right,df):
    df = df.merge(right=dfCollision,left_on=left,
              right_on=right, how='left')
    df.loc[df['Month'].notnull(), 'CRASHED'] = 1
    return df[['MONTH', 'DAY', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER', 
         'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 
         'DEPARTURE_TIME', 'ARRIVAL_TIME', 'DAY_OF_WEEK',
         'SCHEDULED_DEPARTURE', 'DEPARTURE_DELAY', 'TAXI_OUT', 
         'WHEELS_OFF', 'SCHEDULED_TIME', 'ELAPSED_TIME', 
         'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN',
         'SCHEDULED_ARRIVAL', 'ARRIVAL_DELAY', 'DIVERTED', 
         'CANCELLED', 'CANCELLATION_REASON', 'AIR_SYSTEM_DELAY', 
         'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 
         'WEATHER_DELAY', 'CRASHED']]

df = merge(['MONTH', 'DAY', 'ORIGIN_AIRPORT', 'TAIL_NUMBER'],['Month', 'Day', 'airport', 'REG'],df)
print('1')

#A flight number, when combined with the name of the airline and the date, identifies a particular flight.
df = merge(['MONTH', 'DAY', 'AIRLINE', 'FLIGHT_NUMBER'],['Month', 'Day', 'airline', 'FLT'],df)
print('2')

df = merge(['MONTH', 'DAY', 'DESTINATION_AIRPORT', 'TAIL_NUMBER'],['Month', 'Day', 'airport', 'REG'],df)
print('3')

#A flight number, when combined with the name of the airline and the date, identifies a particular flight.
df = merge(['MONTH', 'DAY', 'AIRLINE', 'FLIGHT_NUMBER'],['Month', 'Day', 'airline', 'FLT'],df)
print('4')

#check months with crashes
print(df.groupby('MONTH')['CRASHED'].value_counts())

df.fillna(0, inplace=True)

print(df.shape)
print(df.isnull().sum())
print(df['CRASHED'].value_counts())

df = df.set_index('MONTH', 'DAY')

df.to_csv(location+'wildlife-collisions_Joined2015.csv')

print('Done!')