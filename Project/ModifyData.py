import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

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

#drops not needed columns
df = df.drop(['INDEX_NR', 'REG', 'FLT', 'INCIDENT_MONTH', 'INCIDENT_YEAR', 'COMMENTS',
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

#replaces bad values with nan
df = df.replace(r'', np.nan, regex=True)
df = df.replace(r'UNKNOWN', np.nan, regex=True)
df = df.replace(r'CHANGE CODE', np.nan, regex=True)
df = df.replace(r'ZZZZ', np.nan, regex=True)

#replaces names so they represent Airline operator code
df.loc[df['OPID'] == "ASY", "OPERATOR"] = "Royal Australian Air Force"
df.loc[df['OPID'] == "FDY", "OPERATOR"] = "Sun Air International"
df.loc[df['OPID'] == "LTD", "OPERATOR"] = "Executive Express Aviation/JA Air Charter"
df.loc[df['OPID'] == "SOI", "OPERATOR"] = "Southern Aviation"
df.loc[df['OPID'] == "B-717IT", "OPERATOR"] = np.nan
df.reset_index(drop=False)

#fix airport id and name
df.loc[df['AIRPORT_ID'] == "SPANISH PEAKS AIRFIELD", "AIRPORT"] = "SPANISH PEAKS AIRFIELD"
df['AIRPORT_ID']['SPANISH PEAKS AIRFIELD'] = "4V1"

#Converts object to datetime
df['INCIDENT_DATE'] = pd.to_datetime(df['INCIDENT_DATE'])
df['REPORTED_DATE'] = pd.to_datetime(df['REPORTED_DATE'], errors='coerce')
df['LUPDATE'] = pd.to_datetime(df['LUPDATE'], errors='coerce')

#drop nan values in INCIDENT_DATE
df.dropna(subset=['INCIDENT_DATE'], inplace=True)

#replaces names of TIME_OF_DAY with respective times and adds it to INCIDENT_DATE
times = {'Night': '23:59', 'Dusk': '18:00', 'Day': '12:00', 'Dawn': '6:00', np.nan: '0:00', '': '0:00'}
df['TIME_OF_DAY'] = df['TIME_OF_DAY'].apply(times.get)
df['INCIDENT_DATE'] = pd.to_datetime(df['INCIDENT_DATE'].apply(str)+' '+df['TIME_OF_DAY'])
df = df.drop(['TIME_OF_DAY'], axis=1)

print(df['TIME'].abs() * 0.6)########################################################

#Sorts values based on date and sets INCIDENT_DATE as index
df = df.sort_values('INCIDENT_DATE')
df = df.set_index('INCIDENT_DATE')

#Writes to new file
#df.to_csv(location+'wildlife-collisionsTest.csv', encoding = "utf-8")

'''
set values based on previous
combine both tables
DAMAGE: M? just replace with ?

Unknown:
    AIRPORT, RUNWAY, LOCATION, PHASE_OF_FLT, OTHER_SPECIFY,SPECIES
missing values
    ama, amo, ema, emo, AC_CLASS, AC_MASS, NUM_ENGS, TYPE_ENG, ENG_1_POS, ENG_2_POS,
    ENG_3_POS, ENG_4_POS, REG, FLT,
    TIME, AIRPORT, STATE, FAAREGION, ENROUTE, RUNWAY, LOCATION, HEIGHT, SPEED, DISTANCE, PHASE_OF_FLT,
    DAMAGE, OTHER_SPECIFY, EFFECT, EFFECT_OTHER, SKY, PRECIP, SPECIES, SIZE, WARNED, REMARKS, AOS, COST_REPAIRS
    COST_OTHER, COST_REPAIRS_INFL_ADJ, COST_OTHER_INFL_ADJ, REPORTED_DATE, SOURCE, PERSON, NR_INJURIES,
    NR_FATALITIES, LUPDATE
TIME: has minus values
FLT, LOCATION, OTHER_SPECIFY: search- unk
RUNWAY, EFFECT_OTHER: random values contains dates and so much more
SPECIES_ID, SPECIES: UNKB-m,s,l
BIRDS_SEEN, BIRDS_STRUCK: random date and over 100
'''

#df[1].fillna(0, inplace=True)




#df = df.drop(['OPID', 'AIRPORT_ID', 'SPECIES_ID'], axis=1)
'''
removed:
OPID- Airline operator code
AIRPORT_ID- International Civil Aviation Organization airport identifier for location of strike whether it was on or off airport
SPECIES_ID- International Civil Aviation Organization code for type of bird or other wildlife
'''