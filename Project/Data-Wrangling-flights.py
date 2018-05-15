# -*- coding: utf-8 -*-
"""
This file represents the Data-wrangling part organized according to BigData3 lessons
"""

import pandas as pd
import os

os.chdir('dataset') #set working directory
location = 'Extracted_dataset/'

def LoadDataframe():
    types = {'YEAR': int, 'MONTH': int, 'DAY': int, 'DAY_OF_WEEK': int, 'AIRLINE': object,
         'FLIGHT_NUMBER': object, 'TAIL_NUMBER': object, 'ORIGIN_AIRPORT': object, 
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
    print('flights loaded')
    return df

def CleanCollisions():
    types = {'REG': object, 'FLT': object, 'OPID': object, 'AIRPORT_ID': object}

    dfCollision = pd.read_csv('Modified_dataset/wildlife-collisions2015.csv',
                 parse_dates=['INCIDENT_DATE'],
                 dtype=types)

    dfCollision['INCIDENT_DATE'] = dfCollision['INCIDENT_DATE'].astype(str).str.extract('(....-..-..)', expand=True)
    dfCollision['Year'], dfCollision['Month'], dfCollision['Day'] = dfCollision['INCIDENT_DATE'].str.split('-').str
    dfCollision = dfCollision.drop(['INCIDENT_DATE', 'Year'], axis=1)
    dfCollision[['Month','Day']] = dfCollision[['Month','Day']].apply(pd.to_numeric)

    dfFix = pd.read_csv(location+'airlines.csv')
    dfFix = dfFix[['IATA', 'ICAO']]
    dfFix.dropna(subset=['ICAO'], inplace=True)

    dfCollision = pd.merge(left = dfCollision, right = dfFix,  how='left', left_on=['OPID'], right_on = ['ICAO'])
    dfCollision = dfCollision.drop(['OPID', 'ICAO'], axis=1)
    dfCollision = dfCollision.rename(columns={'IATA': 'airline'})

    dfFix = pd.read_csv(location+'airports.csv')
    dfFix = dfFix[['IATA', 'ICAO']]
    dfFix.dropna(subset=['ICAO'], inplace=True)

    dfCollision = pd.merge(left = dfCollision, right = dfFix,  how='left', left_on=['AIRPORT_ID'], right_on = ['ICAO'])
    dfFix = 1
    dfCollision = dfCollision.drop(['AIRPORT_ID', 'ICAO'], axis=1)
    dfCollision = dfCollision.rename(columns={'IATA': 'airport'})
    print('wildlife-collisions2015 dataset loaded')
    return dfCollision

def merge(left,right,df,dfCollision):
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

def mergeDatasets(df,dfCollision):
    df['CRASHED'] = 0

    df = merge(['MONTH', 'DAY', 'ORIGIN_AIRPORT', 'TAIL_NUMBER'],['Month', 'Day', 'airport', 'REG'],df,dfCollision)
    print('1')

    df = merge(['MONTH', 'DAY', 'DESTINATION_AIRPORT', 'TAIL_NUMBER'],['Month', 'Day', 'airport', 'REG'],df,dfCollision)
    print('2')

    #A flight number, when combined with the name of the airline and the date, identifies a particular flight.
    df = merge(['MONTH', 'DAY', 'AIRLINE', 'FLIGHT_NUMBER'],['Month', 'Day', 'airline', 'FLT'],df,dfCollision)
    print('3')

    return df

#used to show where the airports are located in
def addStates(df):
    dfFix = pd.read_csv(location+'us-airports.csv')
    dfFix = dfFix[['iata_code', 'iso_region']]
    dfFix.dropna(subset=['iata_code'], inplace=True)

    df = pd.merge(left = df, right = dfFix,  how='left', left_on=['ORIGIN_AIRPORT'], right_on = ['iata_code'])
    df = df.drop(['iata_code'], axis=1)

    df = pd.merge(left = df, right = dfFix,  how='left', left_on=['DESTINATION_AIRPORT'], right_on = ['iata_code'])
    df = df.drop(['iata_code'], axis=1)

    df = df.rename(columns={'iso_region_x': 'ORIGIN_STATE'})
    df = df.rename(columns={'iso_region_y': 'DESTINATION_STATE'})
    return df
    print('States added')

#check months with crashes
def finish(df):
    print(df.groupby('MONTH')['CRASHED'].value_counts())

    df.fillna(0, inplace=True)

    print(df.shape)
    print(df.isnull().sum())
    print(df['CRASHED'].value_counts())

    df = df.set_index('MONTH', 'DAY')

    df.to_csv('Modified_dataset/wildlife-collisions_Joined2015.csv')
    print('Done!')


if __name__ == '__main__': #when program starts, start with main function
    df = mergeDatasets(LoadDataframe(),CleanCollisions())
    df = addStates(df)
    finish(df)