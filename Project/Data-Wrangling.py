# -*- coding: utf-8 -*-
"""
This file represents the Data-wrangling part organized according to BigData3 lessons
"""

import os
import sys
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'


######################################## LOAD FILES ##########################################
def loadFiles(): 
    location = 'Extracted_dataset/'
    encoding = 'ISO-8859-1'
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
    df = df.replace({'' : np.nan, 'UNKNOWN': np.nan, '[Uu]nknown': np.nan, 
                     'UNK': np.nan, 'CHANGE CODE': np.nan, 'ZZZZ': np.nan}, regex=True)
    df['OPID'] = df['OPID'].replace('B-717IT', np.nan, regex=True)
    
    return df

def fillNaWithValues(df):
    #Fills nan values using different strategies
        #fill with specific values
    df[['NR_INJURIES', 'NR_FATALITIES']] = df[['NR_INJURIES', 'NR_FATALITIES']].fillna(0)
    df['OPERATOR'].fillna('Unknown', inplace=True)
        #Used only if outliners have small or no influence (average):
    df['SPEED'].fillna(df['SPEED'].mean(), inplace=True)
        #When clear correlation can be seen (most common value also used as most_frequent):
            #Nummerich values
    df['AC_MASS'].fillna(df['AC_MASS'].mode()[0], inplace=True)
    df['NUM_ENGS'].fillna(df['NUM_ENGS'].mode()[0], inplace=True)
            #Object/categorical values
    df['SIZE'].fillna(df['SIZE'].mode()[0], inplace=True)
    df['BIRDS_STRUCK'].fillna(df['BIRDS_STRUCK'].mode()[0], inplace=True)
    df['SPECIES'].fillna(df['SPECIES'].mode()[0], inplace=True)
    df['SKY'].fillna(df['SKY'].mode()[0], inplace=True)
    df['EFFECT'].fillna(df['EFFECT'].mode()[0], inplace=True)
    df['DAMAGE'].fillna(df['DAMAGE'].mode()[0], inplace=True)
    df['AC_CLASS'].fillna(df['AC_CLASS'].mode()[0], inplace=True)
    df['TYPE_ENG'].fillna(df['TYPE_ENG'].mode()[0], inplace=True)
    df['PHASE_OF_FLT'].fillna(df['PHASE_OF_FLT'].mode()[0], inplace=True)
        #Used to resist the effects of outliers (value in the middle):
    df['HEIGHT'].fillna(df['HEIGHT'].median(), inplace=True)
    df['DISTANCE'].fillna(df['DISTANCE'].median(), inplace=True)
    df['AOS'].fillna(df['AOS'].median(), inplace=True)
    
    df['COSTS'] = df['COST_REPAIRS_INFL_ADJ'] + df['COST_OTHER_INFL_ADJ']
    
    #Fills nan values strategies based on groups
        #All strategies (except mode)
    df = fillNaNBasedOnGroup('INDICATED_DAMAGE', 'COSTS', df, 'median')
        #mode
    df = fillNaNwithGroupsMode(df, 'SKY', 'PRECIP')
    df = fillNaNwithGroupsMode(df, 'AC_CLASS', 'ATYPE')
    
    df['ENROUTE'].fillna(df['STATE'], inplace=True)
    df = df.drop(['STATE'], axis=1)
    df = df.rename(columns={'ENROUTE': 'STATE'})
    df = fillNaNwithGroupsMode(df, 'STATE', 'AIRPORT')
    
    return df

def fillNaNwithGroupsMode(df, groupedBy, filled):#fills nan values base on theyr group, supports only mode
    def top_value_count(x):
        return x.value_counts()

    gb = df[[groupedBy, filled]].groupby([groupedBy])[filled]
    df_top_freq = gb.apply(top_value_count).reset_index()
    df_top_freq = df_top_freq.sort_values(by=filled, ascending=False)
    df_top_freq = df_top_freq.drop_duplicates([groupedBy], keep='first')
    
    for i in df_top_freq.iterrows():
        df.loc[df[groupedBy] == i[1][0], filled] = df.loc[df[groupedBy] == i[1][0], filled].fillna(i[1][1])
        
    return df

def fillNaNBasedOnGroup(groupedBy, column, df, strategy):#fills nan values base on theyr group, but doesnt support mode
    df[column] = df[column].fillna(df.groupby(groupedBy)[column].transform(strategy))
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
    df.loc[df['OPID'] == 'ASY', 'OPERATOR'] = 'Royal Australian Air Force'
    df.loc[df['OPID'] == 'FDY', 'OPERATOR'] = 'Sun Air International'
    df.loc[df['OPID'] == 'LTD', 'OPERATOR'] = 'Executive Express Aviation/JA Air Charter'
    df.loc[df['OPID'] == 'SOI', 'OPERATOR'] = 'Southern Aviation'
    
    df.loc[df['AIRPORT_ID'] == 'SPANISH PEAKS AIRFIELD', 'AIRPORT'] = 'SPANISH PEAKS AIRFIELD'
    df['AIRPORT_ID'].replace('SPANISH PEAKS AIRFIELD', '4V1')
    df.loc[df['AIRPORT_ID'] == 'KLUK', 'AIRPORT'] = 'CINCINNATI MUNICIPAL'
    df.loc[df['AIRPORT_ID'] == 'KDKK', 'AIRPORT'] = 'CHAUTAUQUA-DUNKIRK'
    
    return df

def normalizeGrammar(df):
    df['WARNED'] = df['WARNED'].map({'Y': 1, 'N': 0, 'y': 1, 'n': 0}) #Converts object values to int
    
    df['SIZE'] = df['SIZE'].str.lower().replace(r'small', 'Small')
    df['SIZE'] = df['SIZE'].str.lower().replace(r'medium', 'Medium')
    df['SIZE'] = df['SIZE'].str.lower().replace(r'large', 'Large')
    df['SPECIES'] = (df['SPECIES'].str.lower()).str.title()
    df['EFFECT'] = (df['EFFECT'].str.lower()).str.title()
    df['SKY'] = df['SKY'].str.replace(r'S[Oo]me Clouds?', 'Some Clouds')
    df['SKY'] = df['SKY'].str.replace(r'N[Oo] C[Ll]ouds?s?', 'No Clouds')
    df['PRECIP'] = df['PRECIP'].replace('NoNe', 'None')
    df['EFFECT'] = df['EFFECT'].replace('NONE', 'None')
    df['PHASE_OF_FLT'] = df['PHASE_OF_FLT'].replace('take-off run', 'Take-off run')
    df['PHASE_OF_FLT'] = df['PHASE_OF_FLT'].str.replace('landing roll', 'Landing roll')
    df['PHASE_OF_FLT'] = df['PHASE_OF_FLT'].replace('approach', 'Approach')
    df['PHASE_OF_FLT'] = df['PHASE_OF_FLT'].replace('climb', 'Climb')
    df['PHASE_OF_FLT'] = df['PHASE_OF_FLT'].replace('descent', 'Descent')
    
    return df

def dropValues(df):
    df = df.drop(['TIME_OF_DAY', 'TIME'], axis=1)
    df.dropna(subset=['INCIDENT_DATE'], inplace=True) #drop nan rows in INCIDENT_DATE
    df = df.drop(['INDEX_NR', 'INCIDENT_MONTH', 'INCIDENT_YEAR', 'COMMENTS',  #Information here is compleatly useless
                  'TRANSFER', 'LUPDATE', 'REPORTED_NAME', 'REPORTED_TITLE'], axis=1)
    df = df.drop(['AMA', 'AMO', 'EMA', 'EMO', 'ENG_1_POS', 'ENG_2_POS', 'ENG_3_POS', 'ENG_4_POS', #Information here could be used later if needed
                 'REMAINS_COLLECTED', 'REMAINS_SENT', 'FAAREGION', 'RUNWAY', 
                 'LOCATION', 'OTHER_SPECIFY', 'EFFECT_OTHER', 'SPECIES_ID', 'REMARKS', 
                 'COST_REPAIRS', 'COST_OTHER', 'REPORTED_DATE', 'SOURCE', 'WARNED', 'BIRDS_SEEN',
                 'PERSON', 'DAMAGE', 'COST_OTHER_INFL_ADJ', 'COST_REPAIRS_INFL_ADJ'], axis=1)
    #WARNED,BIRDS_SEEN,DAMAGE- usefull but contains too litle info
    
    states=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
       'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
       'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
       'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
       'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', #States till here
       'DC', #Federal district till here
       'PR', 'VI', 'PI']#Inhabited territories till here
    df = df[df['STATE'].isin(states)]#drops all from outside USA
    
    return df
    

def dataNormalization(df):
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
    
    '''
    #used to determin how to fill in nan values
    test = df['DAMAGE']
    print(test.value_counts())
    print(test.isnull().sum())
    test.hist()
    '''
    
    df2015 = df.loc['2015-01-01 00:00:00':'2015-12-31 23:59:59']
    df2015 = df2015[['REG', 'FLT', 'OPID', 'AIRPORT_ID']]
    df2015.to_csv('Modified_dataset/wildlife-collisions2015.csv', encoding = 'utf-8')
    
    df = df.drop(['REG', 'FLT', 'OPID', 'AIRPORT_ID'], axis=1)
    print(df.isnull().sum())
    df.to_csv('Modified_dataset/wildlife-collisions.csv', encoding = 'utf-8')
    
    print('Done!')

    
if __name__ == '__main__': #when program starts, start with main function
    main()
