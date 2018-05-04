# -*- coding: utf-8 -*-
"""
This file represents the Data joining
"""

import pandas as pd
import os

os.chdir('dataset/Modified_dataset') #set working directory

types = {'DATE': object, 'AIRLINE': object, 'FLIGHT_NUMBER': object, 'TAIL_NUMBER': object, 'ORIGIN_AIRPORT': object, 
         'DESTINATION_AIRPORT': object, 'DEPARTURE_TIME': object, 'ARRIVAL_TIME': object}

df = pd.read_csv('2015.csv',
     dtype=types)

########################################################################################

types = {'REG': object, 'FLT': object, 'OPID': object, 'AIRPORT_ID': object}

dfCollision = pd.read_csv('wildlife-collisions2015.csv',
                 parse_dates=['INCIDENT_DATE'],
                 dtype=types)

dfCollision['INCIDENT_DATE'] = dfCollision['INCIDENT_DATE'].astype(str).str.extract('(....-..-..)', expand=True)

dfCollisionFix = pd.read_csv('airlines.csv')
dfCollisionFix = dfCollisionFix[['IATA', 'ICAO']]
dfCollisionFix.dropna(subset=['ICAO'], inplace=True)

dfCollision = pd.merge(left = dfCollision, right = dfCollisionFix,  how='left', left_on=['OPID'], right_on = ['ICAO'])
dfCollision = dfCollision.drop(['OPID', 'ICAO'], axis=1)
dfCollision = dfCollision.rename(columns={'IATA': 'airline'})

dfCollisionFix = pd.read_csv('airports.csv')
dfCollisionFix = dfCollisionFix[['IATA', 'ICAO']]
dfCollisionFix.dropna(subset=['ICAO'], inplace=True)

dfCollision = pd.merge(left = dfCollision, right = dfCollisionFix,  how='left', left_on=['AIRPORT_ID'], right_on = ['ICAO'])
dfCollisionFix = 1;
dfCollision = dfCollision.drop(['AIRPORT_ID', 'ICAO'], axis=1)
dfCollision = dfCollision.rename(columns={'IATA': 'airport'})

########################################################################################
print('here')
df['CRASHED'] = 0

df = df.merge(right=dfCollision,left_on=['DATE', 'AIRLINE', 'ORIGIN_AIRPORT', 'TAIL_NUMBER'],right_on=['INCIDENT_DATE', 'airline', 'airport', 'REG'], how='left')
df.loc[df['INCIDENT_DATE'].notnull(), 'CRASHED'] = 1
df = df[['DATE', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER', 'ORIGIN_AIRPORT',
         'DESTINATION_AIRPORT', 'DEPARTURE_TIME', 'ARRIVAL_TIME', 'CRASHED']]
print('1')

df = df.merge(right=dfCollision,left_on=['DATE', 'AIRLINE', 'ORIGIN_AIRPORT', 'FLIGHT_NUMBER'],right_on=['INCIDENT_DATE', 'airline', 'airport', 'FLT'], how='left')
df.loc[df['INCIDENT_DATE'].notnull(), 'CRASHED'] = 1
df = df[['DATE', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER', 'ORIGIN_AIRPORT',
         'DESTINATION_AIRPORT', 'DEPARTURE_TIME', 'ARRIVAL_TIME', 'CRASHED']]
print('2')

df = df.merge(right=dfCollision,left_on=['DATE', 'AIRLINE', 'DESTINATION_AIRPORT', 'TAIL_NUMBER'],right_on=['INCIDENT_DATE', 'airline', 'airport', 'REG'], how='left')
df.loc[df['INCIDENT_DATE'].notnull(), 'CRASHED'] = 1
df = df[['DATE', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER', 'ORIGIN_AIRPORT',
         'DESTINATION_AIRPORT', 'DEPARTURE_TIME', 'ARRIVAL_TIME', 'CRASHED']]
print('3')

df = df.merge(right=dfCollision,left_on=['DATE', 'AIRLINE', 'DESTINATION_AIRPORT', 'FLIGHT_NUMBER'],right_on=['INCIDENT_DATE', 'airline', 'airport', 'FLT'], how='left')
df.loc[df['INCIDENT_DATE'].notnull(), 'CRASHED'] = 1
df = df[['DATE', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER', 'ORIGIN_AIRPORT',
         'DESTINATION_AIRPORT', 'DEPARTURE_TIME', 'ARRIVAL_TIME', 'CRASHED']]
print('4')

print(df.shape)
print(df.isnull().sum())
print(df['CRASHED'].value_counts())

df = df.set_index('DATE')

df.to_csv('Joined2015.csv')

print('Done!')