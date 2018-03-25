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

#replaces bad values with nan
df = df.replace(r'', np.nan, regex=True)
df = df.replace(r'UNKNOWN', np.nan, regex=True)
df = df.replace(r'UNK', np.nan, regex=True)
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
df['AIRPORT_ID'].replace('SPANISH PEAKS AIRFIELD', "4V1")
df.loc[df['AIRPORT_ID'] == "KLUK", "AIRPORT"] = "CINCINNATI MUNICIPAL"
df.loc[df['AIRPORT_ID'] == "KDKK", "AIRPORT"] = "CHAUTAUQUA-DUNKIRK"

#replace values so it is easyer to understand
df['DAMAGE'].replace('M?', "?")
df['NR_INJURIES'].fillna(0, inplace=True)
df['NR_FATALITIES'].fillna(0, inplace=True)
df['PERSON'].fillna('Other', inplace=True)

df['SKY'].replace('Some Cloud', "Some Clouds")
df['SKY'].replace('No Cloud', "No Clouds")

#Converts object to datetime
df['INCIDENT_DATE'] = pd.to_datetime(df['INCIDENT_DATE'])
'''df['REPORTED_DATE'] = pd.to_datetime(df['REPORTED_DATE'], errors='coerce')
df['LUPDATE'] = pd.to_datetime(df['LUPDATE'], errors='coerce')'''

#drop nan rows in INCIDENT_DATE
df.dropna(subset=['INCIDENT_DATE'], inplace=True)

#fixes INCIDENT_DATE based on given info
times = {'Night': '23:59', 'Dusk': '18:00', 'Day': '12:00', 'Dawn': '6:00'}
df['TIME_OF_DAY'] = df['TIME_OF_DAY'].apply(times.get)
df['TIME'] = pd.to_datetime((df['TIME'].abs() // 100 * 60) + (df['TIME'].abs() % 100), unit='m')
df['TIME'] = df['TIME'].astype(str).str.extract('(..:..)', expand=True)
df['TIME'].fillna(df['TIME_OF_DAY'], inplace=True)
df['TIME'] = df['TIME'].replace(np.nan, '0:00', regex=True)
df['INCIDENT_DATE'] = pd.to_datetime(df['INCIDENT_DATE'].apply(str)+' '+df['TIME'])
df = df.drop(['TIME'], axis=1)
df = df.drop(['TIME_OF_DAY'], axis=1)

#Sorts values based on date and sets INCIDENT_DATE as index
df = df.sort_values('INCIDENT_DATE')
df = df.set_index('INCIDENT_DATE')

#drops not needed columns
df = df.drop(['INDEX_NR', 'REG', 'FLT', 'INCIDENT_MONTH', 'INCIDENT_YEAR', 'COMMENTS', 
              'TRANSFER', 'COST_REPAIRS_INFL_ADJ', 'COST_OTHER_INFL_ADJ', 
              'REPORTED_NAME', 'REPORTED_TITLE'], axis=1)

'''
removed:
    Unnamed: 0- unnecessary field
    INDEX_NR- Individual record number
    REG- Aircraft registration
    FLT- Flight number
    INCIDENT_MONTH- already provided in INCIDENT_DATE
    INCIDENT_YEAR- already provided in INCIDENT_DATE
    COMMENTS- As entered by database manager. Can include name of aircraft owner, types of reports received, updates, etc.
    TRANSFER- Unused field at this time
    COST_REPAIRS_INFL_ADJ- Costs adjusted for inflation (can be self calculated)
    COST_OTHER_INFL_ADJ- Other cost adjusted for inflation (can be self calculated)
    REPORTED_NAME- always empty
    REPORTED_TITLE- always empty
'''

df = df.drop(['OPID', 'AMO', 'EMO', 'ENG_1_POS', 'ENG_2_POS', 'ENG_3_POS', 'ENG_4_POS',
              'REMAINS_COLLECTED', 'REMAINS_SENT', 'AIRPORT_ID', 'FAAREGION', 'RUNWAY', 
              'LOCATION', 'OTHER_SPECIFY', 'EFFECT_OTHER', 'SPECIES_ID', 'REMARKS', 'REPORTED_DATE',
              'SOURCE', 'PERSON', 'LUPDATE'], axis=1)
'''
removed:
    OPID- Airline operator code
    AMO- International Civil Aviation Organization code for Aircraft Model 
    EMO- Engine Model Code
    ENG_1-4_POS- Where engine is mounted  on aircraft
    REMAINS_COLLECTED- Indicates if bird or wildlife remains were found and collected
    REMAINS_SENT- Indicates if remains were sent to the Smithsonian Institution for identifcation
    AIRPORT_ID- International Civil Aviation Organization airport identifier for location of strike whether it was on or off airport
    FAAREGION- FAA Region where airport is located
    RUNWAY- Runway
    LOCATION- Various information about aircraft location if enroute or airport where strike evidence was found. Some locations show the two airports for the flight departure and arrival if pilot was unaware of the strike.
    OTHER_SPECIFY- What part was struck other than those listed above
    EFFECT_OTHER- Effect on flight other than those listed on the form
    SPECIES_ID- International Civil Aviation Organization code for type of bird or other wildlife
    REMARKS- Most of remarks are from the form but some are data entry notes and are usually in parentheses.
    REPORTED_DATE- Date report was written
    SOURCE- Type of report. Note: for multiple types of reports this will be indicated as Multiple.  See "Comments" field for details
    PERSON- Only one selection allowed. For multiple reports, see field "Reported Title"
    LUPDATE- Last time record was updated
'''

#Writes to new file
df.to_csv(location+'wildlife-collisions-Modified.csv', encoding = "utf-8")

print('Done!')