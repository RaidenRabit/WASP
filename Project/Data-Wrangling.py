# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 19:57:09 2018

@author: RaidenRabit
This file represents the Data-wrangling part organized according to BigData3 lessons
"""
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer
pd.options.mode.chained_assignment = None  # default='warn'


######################################## LOAD FILES ##########################################
def loadFiles(): 
    #reading raw data
    df1990_1999 = pd.read_csv('STRIKE_REPORTS (1990-1999).csv', 
                     encoding = "ISO-8859-1",
                     dtype={'INDEX_NR': int, 'OPID': object, 'OPERATOR': object, 'ATYPE': object, 'AMA': object,
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
                            'NR_FATALITIES': float, 'LUPDATE': object, 'TRANSFER': bool, 'INDICATED_DAMAGE': bool})
    
    
    df2000_2009 = pd.read_csv('STRIKE_REPORTS (2000-2009).csv', 
                     encoding = "ISO-8859-1",
                     dtype={'INDEX_NR': int, 'OPID': object, 'OPERATOR': object, 'ATYPE': object, 'AMA': object,
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
                            'NR_FATALITIES': float, 'LUPDATE': object, 'TRANSFER': bool, 'INDICATED_DAMAGE': bool})
    
    df2010_Current = pd.read_csv('STRIKE_REPORTS (2010-Current).csv', 
                     encoding = "ISO-8859-1",
                     dtype={'INDEX_NR': int, 'OPID': object, 'OPERATOR': object, 'ATYPE': object, 'AMA': object,
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
                            'NR_FATALITIES': float, 'LUPDATE': object, 'TRANSFER': bool, 'INDICATED_DAMAGE': bool})
    
    dfMilitary = pd.read_csv('STRIKE_REPORTS_BASH (1990-Current).csv', 
                     encoding = "ISO-8859-1",
                     dtype={'INDEX_NR': int, 'OPID': object, 'OPERATOR': object, 'ATYPE': object, 'AMA': object,
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
                            'NR_FATALITIES': float, 'LUPDATE': object, 'TRANSFER': bool, 'INDICATED_DAMAGE': bool})
    #putting it into 1 single file
    frames = [df1990_1999, df2000_2009, df2010_Current, dfMilitary]
    df = pd.concat(frames)    
    df = df.set_index('INDEX_NR')
    return df

######################################## HANDLE NaN #########################################
    
def fillWithNa(df): 
    df = df.replace('', np.nan, regex=True)
    df = df.replace('UNKNOWN', np.nan, regex=True)
    df = df.replace('[Uu]nknown', np.nan, regex=True)
    df = df.replace('UNK', np.nan, regex=True)
    df = df.replace('CHANGE CODE', np.nan, regex=True)
    df = df.replace('ZZZZ', np.nan, regex=True)
    
    df.loc[df['OPID'] == "B-717IT", "OPERATOR"] = np.nan
    return df

def fillNaWithValues(df):
    #fill with specific values
    df['OPERATOR'].fillna('Unknown', inplace=True)
    df['NR_INJURIES'].fillna(0, inplace=True)
    df['NR_FATALITIES'].fillna(0, inplace=True)
    
    #Fills nan values using most popular
    df['SIZE'].fillna(df['SIZE'].value_counts().idxmax(), inplace=True)
    df['BIRDS_STRUCK'].fillna(df['BIRDS_STRUCK'].value_counts().idxmax(), inplace=True)
    df['SPECIES'].fillna(df['SPECIES'].value_counts().idxmax(), inplace=True)
    df['PRECIP'].fillna(df['PRECIP'].value_counts().idxmax(), inplace=True)
    df['EFFECT'].fillna(df['EFFECT'].value_counts().idxmax(), inplace=True)
    df['DAMAGE'].fillna(df['DAMAGE'].value_counts().idxmax(), inplace=True)
    df['AC_CLASS'].fillna(df['AC_CLASS'].value_counts().idxmax(), inplace=True)
    df['TYPE_ENG'].fillna(df['TYPE_ENG'].value_counts().idxmax(), inplace=True)
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
    
    
def handleNaNmain(df): #handling NAN values
    df=fillWithNa(df) #fill empty and wrong data with na values
    df=fillNaWithValues(df) #fill NaN values with some other types of values
    df=fillNaStrategicaly(df, ['SPEED'], 'mean')#Used only if outliners have small or no influence
    df=fillNaStrategicaly(df, ['AC_MASS', 'NUM_ENGS'], 'most_frequent')#When clear correlation can be seen
    df=fillNaStrategicaly(df, ['HEIGHT', 'DISTANCE', 'AOS', 'COST_OTHER', 'COST_REPAIRS'], 'median')#To resist the effects of outliers
    return df
########################################## DATA FORMATING ###################################
def dataFormating(df):
    df['INCIDENT_DATE'] = pd.to_datetime(df['INCIDENT_DATE']) #Converts object to datetime
    return df
########################################## DATA NORMALIZATION ####################################
def mergeFields(df): #Merge these fields to show state where the incident happened
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
    df.loc[df['OPID'] == "B-717IT", "OPERATOR"] = np.nan
    df.loc[df['AIRPORT_ID'] == "SPANISH PEAKS AIRFIELD", "AIRPORT"] = "SPANISH PEAKS AIRFIELD"
    df['AIRPORT_ID'].replace('SPANISH PEAKS AIRFIELD', "4V1")
    df.loc[df['AIRPORT_ID'] == "KLUK", "AIRPORT"] = "CINCINNATI MUNICIPAL"
    df.loc[df['AIRPORT_ID'] == "KDKK", "AIRPORT"] = "CHAUTAUQUA-DUNKIRK"
    return df

def normalizeGrammar(df):
    df['WARNED'] = df['WARNED'].map({'Y': 1, 'N': 0, 'y': 1, 'n': 0}) #Converts object values to int
    df['DAMAGE'] = df['DAMAGE'].replace('M?', "?")
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
    df = df.drop(['REG', 'FLT', 'INCIDENT_MONTH', 'INCIDENT_YEAR', 'COMMENTS',  #Information here is compleatly useless
                  'TRANSFER', 'LUPDATE', 'REPORTED_NAME', 'REPORTED_TITLE'], axis=1)
    df = df.drop(['OPID', 'AMO', 'EMO', 'ENG_1_POS', 'ENG_2_POS', 'ENG_3_POS', 'ENG_4_POS', #Information here could be used later if needed
                 'REMAINS_COLLECTED', 'REMAINS_SENT', 'AIRPORT_ID', 'FAAREGION', 'RUNWAY', 
                 'LOCATION', 'OTHER_SPECIFY', 'EFFECT_OTHER', 'SPECIES_ID', 'REMARKS', 
                 'COST_REPAIRS_INFL_ADJ', 'COST_OTHER_INFL_ADJ', 'REPORTED_DATE', 'SOURCE', 
                 'PERSON'], axis=1)
    return df
    

def dataNormalizationMain(df):
    df=mergeFields(df)
    df=normalizeIncidentDate(df)
    df=normalizeWrongValues(df)
    df=normalizeGrammar(df)
    df=dropValues(df)
    return df
########################################## MAIN FUNCTION ####################################
'''
    NOTE: if you dont want to wait the entire ~30 sec to rerun the entire program, you can just "pickle" the df (save it's current state in a file)
    using:
        df.to_pickle(filename)
    then you can load it by
        df=pd.read_pickle(filename)
'''
def main():
    os.chdir('dataset\\Extracted_dataset') #set working directory
    print('Files Found')
    
    df=loadFiles() #20-115; reading raw data and putting it into 1 single file
    print('Files Loaded')
    
    df=handleNaNmain(df) #117-; handling NAN values
    print('Handled NaN')
    
    df=dataFormating(df) #formating columns to appropriate data types
    print('Data Formated')
    
    df=dataNormalizationMain(df) #transforming values of several variables into a similar range
    print('Data Normalized')
    
    #TODO: df=dataBining(df) #transforming continuous numerical variables into discrete categorical 'bins'
    print('Data Binned')
    
    df = df.sort_values('INCIDENT_DATE')
    df = df.set_index('INCIDENT_DATE')
    print(df.dtypes)
    df.to_csv(path_or_buf='wildlife-collisions.csv', encoding = "utf-8")
    print('Data Saved to \'wildlife-collisions.csv\'')
    print('Done')
    
    
if __name__ == '__main__': #when program starts, start with main function
    main()
