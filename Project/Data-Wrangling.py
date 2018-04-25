# -*- coding: utf-8 -*-
"""
This file represents the Data-wrangling part organized according to BigData3 lessons
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer
pd.options.mode.chained_assignment = None  # default='warn'


######################################## LOAD FILES ##########################################
def loadFiles(): 
    location = "Extracted_dataset/"
    encoding = "ISO-8859-1"
    types = {'INDEX_NR': int, 'OPID': object, 'OPERATOR': object, 'ATYPE': object, 'AMA': object,
                            'AMO': object, 'EMA': object, 'EMO': object, 'AC_CLASS': object, 'AC_MASS': float, 
                            'NUM_ENGS': float, 'TYPE_ENG': object, 'ENG_1_POS': object, 'ENG_2_POS': float, 'ENG_3_POS': object, 
                            'ENG_4_POS': float, 'REG': object, 'FLT': object, 'REMAINS_COLLECTED': bool, 'REMAINS_SENT': bool, 
                            'INCIDENT_DATE': object, 'INCIDENT_MONTH': float, 'INCIDENT_YEAR': float, 'TIME_OF_DAY': object, 'TIME': float, 
                            'AIRPORT_ID': object, 'AIRPORT': object, 'STATE': object, 'FAAREGION': object, 'ENROUTE': object, 
                            'RUNWAY': object, 'LOCATION': object, 'HEIGHT': float, 'SPEED': float, 'DISTANCE': float, 
                            'PHASE_OF_FLT': object, 'DAMAGE': object, 'STR_RAD': bool, 'DAM_RAD': bool, 'STR_WINDSHLD': bool, 
                            'DAM_WINDSHLD': bool, 'STR_NOSE': bool, 'DAM_NOSE': bool, 'STR_ENG1': bool, 'DAM_ENG1': bool, 
                            'STR_ENG2': bool, 'DAM_ENG2': bool, 'STR_ENG3': bool, 'DAM_ENG3': bool, 'STR_ENG4': bool, 
                            'DAM_ENG4': bool, 'INGESTED': bool, 'STR_PROP': bool, 'DAM_PROP': bool, 'STR_WING_ROT': bool, 
                            'DAM_WING_ROT': bool, 'STR_FUSE': bool, 'DAM_FUSE': bool, 'STR_LG': bool, 'DAM_LG': bool,
                            'STR_TAIL': bool, 'DAM_TAIL': bool, 'STR_LGHTS': bool, 'DAM_LGHTS': bool, 'STR_OTHER': bool,
                            'DAM_OTHER': bool, 'OTHER_SPECIFY': object, 'EFFECT': object, 'EFFECT_OTHER': object, 'SKY': object,
                            'PRECIP': object, 'SPECIES_ID': object, 'SPECIES': object, 'BIRDS_SEEN': object, 'BIRDS_STRUCK': object,
                            'SIZE': object, 'WARNED': object, 'COMMENTS': object, 'REMARKS': object, 'AOS': float,
                            'COST_REPAIRS': float, 'COST_OTHER': float, 'COST_REPAIRS_INFL_ADJ': float, 'COST_OTHER_INFL_ADJ': float, 'REPORTED_NAME': object,
                            'REPORTED_TITLE': object, 'REPORTED_DATE': object, 'SOURCE': object, 'PERSON': object, 'NR_INJURIES': float,
                            'NR_FATALITIES': float, 'LUPDATE': object, 'TRANSFER': bool, 'INDICATED_DAMAGE': bool}
   
    df1990_1999 = pd.read_csv(location+'STRIKE_REPORTS (1990-1999).csv', 
                     encoding = encoding,
                     dtype=types)
    
    
    df2000_2009 = pd.read_csv(location+'STRIKE_REPORTS (2000-2009).csv', 
                     encoding = encoding,
                     dtype=types)
    
    df2010_Current = pd.read_csv(location+'STRIKE_REPORTS (2010-Current).csv', 
                     encoding = encoding,
                     dtype=types)
    
    dfMilitary = pd.read_csv(location+'STRIKE_REPORTS_BASH (1990-Current).csv', 
                     encoding = encoding,
                     dtype=types)
    
    #putting it into 1 single file
    frames = [df1990_1999, df2000_2009, df2010_Current, dfMilitary]
    df = pd.concat(frames)    
    return df

######################################## HANDLE NaN #########################################
    
def fillWithNa(df):
    df = df.replace('', np.nan, regex=True)
    df = df.replace('UNKNOWN', np.nan, regex=True)
    df = df.replace('[Uu]nknown', np.nan, regex=True)
    df = df.replace('UNK', np.nan, regex=True)
    df = df.replace('CHANGE CODE', np.nan, regex=True)
    df = df.replace('ZZZZ', np.nan, regex=True)
    df['OPID'] = df['OPID'].replace('B-717IT', np.nan, regex=True)
    
    return df

def fillNaWithValues(df):
    #fill nan with some coaralation
    df.loc[df['PRECIP'] != "None", "SKY"].fillna("Overcast")
    df.loc[df['SKY'] == "No Clouds", "PRECIP"].fillna("None")
    
    #fill with specific values
    nanRepresenter = '-'
    df['NR_INJURIES'].fillna(0, inplace=True)
    df['NR_FATALITIES'].fillna(0, inplace=True)
    df['SKY'].fillna('Some Clouds', inplace=True)
    df['ATYPE'].fillna(nanRepresenter, inplace=True)
    df['OPERATOR'].fillna(nanRepresenter, inplace=True)
    df['STATE'].fillna(nanRepresenter, inplace=True)
    df['AIRPORT'].fillna(nanRepresenter, inplace=True)
    
    #Fills nan values using most popular
    df['SIZE'].fillna(df['SIZE'].value_counts().idxmax(), inplace=True)
    df['BIRDS_STRUCK'].fillna(df['BIRDS_STRUCK'].value_counts().idxmax(), inplace=True)
    df['SPECIES'].fillna(df['SPECIES'].value_counts().idxmax(), inplace=True)
    df['PRECIP'].fillna(df['PRECIP'].value_counts().idxmax(), inplace=True)
    df['EFFECT'].fillna(df['EFFECT'].value_counts().idxmax(), inplace=True)
    df['DAMAGE'].fillna(df['DAMAGE'].value_counts().idxmax(), inplace=True)
    df['AC_CLASS'].fillna(df['AC_CLASS'].value_counts().idxmax(), inplace=True)
    df['TYPE_ENG'].fillna(df['TYPE_ENG'].value_counts().idxmax(), inplace=True)
    df['PHASE_OF_FLT'].fillna(df['PHASE_OF_FLT'].value_counts().idxmax(), inplace=True)
    
    df=fillNaStrategicaly(df, ['SPEED'], 'mean')#Used only if outliners have small or no influence
    df=fillNaStrategicaly(df, ['AC_MASS', 'NUM_ENGS'], 'most_frequent')#When clear correlation can be seen
    df=fillNaStrategicaly(df, ['HEIGHT', 'DISTANCE', 'AOS', 'COST_REPAIRS_INFL_ADJ', 'COST_OTHER_INFL_ADJ'], 'median')#To resist the effects of outliers
    
    return df

def fillNaStrategicaly(df, columns, strategy):
    change = df[columns]#Columns to change
    impute = Imputer(missing_values='NaN',#Change NaN values
                   strategy=strategy,#Use established strategy
                   axis=0)#Along the rows
    imputed = impute.fit_transform(change)# Use imputation model to get values
    imputed = pd.DataFrame(imputed,# Remake the DataFrame
                           index=change.index,#Get rows
                           columns=change.columns)#Get columns
    df[columns] = imputed[columns]#Replaces existing columns and all information in them with new
    return df
    
    
def handleNaN(df): #handling NAN values
    df=fillWithNa(df) #fill empty and wrong data with na values
    df=fillNaWithValues(df) #fill NaN values with some other types of values
    return df

########################################## DATA FORMATING ###################################
def dataFormating(df):
    df['INCIDENT_DATE'] = pd.to_datetime(df['INCIDENT_DATE']) #Converts object to datetime
    return df

########################################## DATA NORMALIZATION ####################################
def mergeFields(df): #Merge these fields to show state where the incident happened
    #Location?
    df['ENROUTE'].fillna(df['STATE'], inplace=True)
    df = df.drop(['STATE'], axis=1)
    df = df.rename(columns={'ENROUTE': 'STATE'})
    
    return df

def normalizeIncidentDate(df): #fixes INCIDENT_DATE based on given info
    times = {'Night': '23:59', 'Dusk': '18:00', 'Day': '12:00', 'Dawn': '6:00'}
    df['TIME_OF_DAY'] = df['TIME_OF_DAY'].apply(times.get)
    df['TIME'] = pd.to_datetime((df['TIME'].abs() // 100 * 60) + (df['TIME'].abs() % 100), unit='m')
    df['TIME'] = df['TIME'].astype(str).str.extract('(..:..)', expand=True)
    df['TIME'].fillna(df['TIME_OF_DAY'], inplace=True)
    df['TIME'] = df['TIME'].replace(np.nan, '0:00', regex=True)
    df['INCIDENT_DATE'] = pd.to_datetime(df['INCIDENT_DATE'].apply(np.str)+' '+df['TIME'], errors='coerce')
    return df

def normalizeWrongValues(df):
    df.loc[df['OPID'] == "ASY", "OPERATOR"] = "Royal Australian Air Force"
    df.loc[df['OPID'] == "FDY", "OPERATOR"] = "Sun Air International"
    df.loc[df['OPID'] == "LTD", "OPERATOR"] = "Executive Express Aviation/JA Air Charter"
    df.loc[df['OPID'] == "SOI", "OPERATOR"] = "Southern Aviation"
    
    df.loc[df['AIRPORT_ID'] == "SPANISH PEAKS AIRFIELD", "AIRPORT"] = "SPANISH PEAKS AIRFIELD"
    df['AIRPORT_ID'].replace('SPANISH PEAKS AIRFIELD', "4V1")
    df.loc[df['AIRPORT_ID'] == "KLUK", "AIRPORT"] = "CINCINNATI MUNICIPAL"
    df.loc[df['AIRPORT_ID'] == "KDKK", "AIRPORT"] = "CHAUTAUQUA-DUNKIRK"
    
    return df

def normalizeGrammar(df):
    df['WARNED'] = df['WARNED'].map({'Y': 1, 'N': 0, 'y': 1, 'n': 0}) #Converts object values to int
    '''
    df['AC_CLASS'] = df['AC_CLASS'].map({'A': 'Airplane', 'B': 'Helicopter', 'C': 'Glider', 
                                          'D': 'Balloon', 'F': 'Dirigible', 'I': 'Gyroplane', 
                                          'J': 'Ultralight', 'Y': 'Other', 'Z': 'Unknown'})#Aircrafts class
        
    df['AC_MASS'] = df['AC_MASS'].map({1: '2,250 kg or less', 2: '2251-5700 kg', 
                                          3: '5,701-27,000 kg', 4: '27,001-272,000 kg',
                                          5: 'above 272,000 kg'})#Mass of aircraft
    
    df['TYPE_ENG'] = df['TYPE_ENG'].map({'A': 'Reciprocating engine (piston)', 'B': 'Turbojet', 
                                          'C': 'Turboprop', 'D': 'Turbofan', 'E': 'None (glider)',
                                          'F': 'Turboshaft (helicopter)', 'Y': 'Other'})#Type of power
    
    df['DAMAGE'] = df['DAMAGE'].map({'M': 'Minor', 'M?': 'Uncertain level', 
                                          'S': 'Substantial', 'D': 'Destroyed'})#Type of damage
    '''
    df['SIZE'] = df['SIZE'].str.lower().replace(r'small', "Small")
    df['SIZE'] = df['SIZE'].str.lower().replace(r'medium', "Medium")
    df['SIZE'] = df['SIZE'].str.lower().replace(r'large', "Large")
    df['SPECIES'] = (df['SPECIES'].str.lower()).str.title()
    df['EFFECT'] = (df['EFFECT'].str.lower()).str.title()
    df['SKY'] = df['SKY'].str.replace(r'S[Oo]me Clouds?', "Some Clouds")
    df['SKY'] = df['SKY'].str.replace(r'N[Oo] C[Ll]ouds?s?', "No Clouds")
    df['PRECIP'] = df['PRECIP'].replace('NoNe', "None")
    df['EFFECT'] = df['EFFECT'].replace('NONE', "None")
    df['PHASE_OF_FLT'] = df['PHASE_OF_FLT'].replace('take-off run', "Take-off run")
    df['PHASE_OF_FLT'] = df['PHASE_OF_FLT'].str.replace('landing roll', "Landing roll")
    df['PHASE_OF_FLT'] = df['PHASE_OF_FLT'].replace('approach', "Approach")
    df['PHASE_OF_FLT'] = df['PHASE_OF_FLT'].replace('climb', "Climb")
    df['PHASE_OF_FLT'] = df['PHASE_OF_FLT'].replace('descent', "Descent")
    return df

def dropValues(df):
    df = df.drop(['TIME'], axis=1)
    df = df.drop(['TIME_OF_DAY'], axis=1)
    df.dropna(subset=['INCIDENT_DATE'], inplace=True) #drop nan rows in INCIDENT_DATE
    df = df.drop(['INDEX_NR', 'REG', 'FLT', 'INCIDENT_MONTH', 'INCIDENT_YEAR', 'COMMENTS',  #Information here is compleatly useless
                  'TRANSFER', 'LUPDATE', 'REPORTED_NAME', 'REPORTED_TITLE'], axis=1)
    df = df.drop(['OPID', 'AMA', 'AMO', 'EMA', 'EMO', 'ENG_1_POS', 'ENG_2_POS', 'ENG_3_POS', 'ENG_4_POS', #Information here could be used later if needed
                 'REMAINS_COLLECTED', 'REMAINS_SENT', 'AIRPORT_ID', 'FAAREGION', 'RUNWAY', 
                 'LOCATION', 'OTHER_SPECIFY', 'EFFECT_OTHER', 'SPECIES_ID', 'REMARKS', 
                 'COST_REPAIRS', 'COST_OTHER', 'REPORTED_DATE', 'SOURCE', 'WARNED', 'BIRDS_SEEN',
                 'PERSON', 'DAMAGE'], axis=1)
    #WARNED,BIRDS_SEEN,DAMAGE- usefull but contains too litle info
    return df
    

def dataNormalization(df):
    df=mergeFields(df)
    sys.stdout.write('.')
    df=normalizeIncidentDate(df)
    sys.stdout.write('.')
    df=normalizeWrongValues(df)
    sys.stdout.write('.')
    df=normalizeGrammar(df)
    sys.stdout.write('.')
    df=dropValues(df)
    sys.stdout.write('.')
    return df

########################################## MAIN FUNCTION ####################################
def main():
    sys.stdout.write('Looking for files...')
    sys.stdout.flush()
    os.chdir('dataset') #set working directory
    print(' Files Found')
    
    sys.stdout.write('Loading files...')
    df=loadFiles() #20-115; reading raw data and putting it into 1 single file
    print(' Files Loaded')
    
    sys.stdout.write('Handaling NaN values...')
    df=handleNaN(df) #117-; handling NAN values
    print(' Handled NaN')
    
    sys.stdout.write('Formating data...')
    df=dataFormating(df) #formating columns to appropriate data types
    print(' Data Formated')
    
    sys.stdout.write('Normalizing data')
    df=dataNormalization(df) #transforming values of several variables into a similar range
    print(' Data Normalized')
    
    df = df.sort_values('INCIDENT_DATE')
    df = df.set_index('INCIDENT_DATE')
    
    #if indicate damage is false than price 0 or lower
    #if rain than has clouds
    #coaralation between strike all false and no known aircraft type?
    
    #removes all info out side of usa and could deal with nan values better maybe drop columns
    print(df.isnull().sum())
    '''
    test = df['DAMAGE']
    print(test.value_counts())
    print(test.isnull().sum())
    test.hist()
    '''
    df.to_csv('Modified_dataset/wildlife-collisions.csv', encoding = "utf-8")
    
    print('Done')
    
    
if __name__ == '__main__': #when program starts, start with main function
    main()
