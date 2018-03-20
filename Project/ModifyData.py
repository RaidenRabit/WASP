import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt 

location = 'dataset/Modified_dataset/'

df = pd.read_csv(location+'wildlife-collisions.csv',
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

df = df.drop(['INDEX_NR', 'REG', 'FLT', 'INCIDENT_MONTH', 'INCIDENT_YEAR',
              'COST_REPAIRS_INFL_ADJ', 'COST_OTHER_INFL_ADJ', 'REPORTED_NAME', 'REPORTED_TITLE'], axis=1)

'''
removed:
Unnamed: 0- unnecessary field
INDEX_NR- Individual record number
REG- Aircraft registration
FLT- Flight number
INCIDENT_MONTH- already provided in INCIDENT_DATE
INCIDENT_YEAR- already provided in INCIDENT_DATE
COST_REPAIRS_INFL_ADJ- Costs adjusted for inflation (can be self calculated)
COST_OTHER_INFL_ADJ- Other cost adjusted for inflation (can be self calculated)
REPORTED_NAME- always empty
REPORTED_TITLE- always empty
'''

df = df.drop(['OPID', 'AIRPORT_ID', 'SPECIES_ID'], axis=1)
'''
removed:
OPID- Airline operator code
AIRPORT_ID- International Civil Aviation Organization airport identifier for location of strike whether it was on or off airport
SPECIES_ID- International Civil Aviation Organization code for type of bird or other wildlife
'''

df = df.replace(r'UNKNOWN', np.nan, regex=True)
#ENG_3_POS CHANGE CODE
#BIRDS_SEEN, BIRDS_STRUCK over 100
#in some places some random #name?
#location - and '


#print(df[173601:173620])
#print('////////////////////////////////////////////////////////////////////')
#print(df.describe(include=['object']))
corr = df.corr()
_, ax = plt.subplots(figsize=(8,6))
sns.heatmap(corr, ax=ax,xticklabels=corr.columns.values,yticklabels=corr.columns.values)
#del df[1]
#df = df.sort_values('Unnamed: 0')