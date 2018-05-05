# -*- coding: utf-8 -*-
"""
This file represents the Data-wrangling part organized according to BigData3 lessons
"""

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

df = df.merge(right=dfCollision,left_on=['DATE', 'ORIGIN_AIRPORT', 'TAIL_NUMBER'],
              right_on=['INCIDENT_DATE', 'airport', 'REG'], how='left')
df.loc[df['INCIDENT_DATE'].notnull(), 'CRASHED'] = 1
df = df[['DATE', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER', 'ORIGIN_AIRPORT',
         'DESTINATION_AIRPORT', 'DEPARTURE_TIME', 'ARRIVAL_TIME', 'CRASHED']]
print('1')

#A flight number, when combined with the name of the airline and the date, identifies a particular flight.
df = df.merge(right=dfCollision,left_on=['DATE', 'AIRLINE', 'FLIGHT_NUMBER'],
              right_on=['INCIDENT_DATE', 'airline', 'FLT'], how='left')
df.loc[df['INCIDENT_DATE'].notnull(), 'CRASHED'] = 1
df = df[['DATE', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER', 'ORIGIN_AIRPORT',
         'DESTINATION_AIRPORT', 'DEPARTURE_TIME', 'ARRIVAL_TIME', 'CRASHED']]
print('2')

df = df.merge(right=dfCollision,left_on=['DATE', 'DESTINATION_AIRPORT', 'TAIL_NUMBER'],
              right_on=['INCIDENT_DATE', 'airport', 'REG'], how='left')
df.loc[df['INCIDENT_DATE'].notnull(), 'CRASHED'] = 1
df = df[['DATE', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER', 'ORIGIN_AIRPORT',
         'DESTINATION_AIRPORT', 'DEPARTURE_TIME', 'ARRIVAL_TIME', 'CRASHED']]
print('3')

#A flight number, when combined with the name of the airline and the date, identifies a particular flight.
df = df.merge(right=dfCollision,left_on=['DATE', 'AIRLINE', 'FLIGHT_NUMBER'],
              right_on=['INCIDENT_DATE', 'airline', 'FLT'], how='left')
df.loc[df['INCIDENT_DATE'].notnull(), 'CRASHED'] = 1
df = df[['DATE', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER', 'ORIGIN_AIRPORT',
         'DESTINATION_AIRPORT', 'DEPARTURE_TIME', 'ARRIVAL_TIME', 'CRASHED']]
print('4')

print(df.shape)
print(df.isnull().sum())
print(df['CRASHED'].value_counts())

df = df.set_index('DATE')

df.to_csv(location+'wildlife-collisions_Joined2015.csv')

print('Done!')