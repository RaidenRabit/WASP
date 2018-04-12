'''
    Data in this file is being finalized by dealing with nan values
'''

import pandas as pd
from sklearn.preprocessing import Imputer
import matplotlib.pyplot as plt
import os

os.chdir('C:/Users/bubri/Desktop/Project/dataset/Modified_dataset/') # Set working directory

df = pd.read_csv('wildlife-collisions-Modified.csv',
                 dtype={'INCIDENT_DATE': object, 'OPERATOR': object, 'ATYPE': object, 'AMA': object,
                        'EMA': object, 'AC_CLASS': object, 'AC_MASS': float, 'NUM_ENGS': float, 
                        'TYPE_ENG': object, 'AIRPORT': object, 'STATE': object, 'ENROUTE': object, 
                        'HEIGHT': float, 'SPEED': float, 'DISTANCE': float, 'PHASE_OF_FLT': object, 
                        'DAMAGE': object, 'STR_RAD': int, 'DAM_RAD': int, 'STR_WINDSHLD': int, 
                        'DAM_WINDSHLD': int, 'STR_NOSE': int, 'DAM_NOSE': int, 'STR_ENG1': int, 
                        'DAM_ENG1': int, 'STR_ENG2': int, 'DAM_ENG2': int, 'STR_ENG3': int, 'DAM_ENG3': int, 
                        'STR_ENG4': int, 'DAM_ENG4': int, 'INGESTED': int, 'STR_PROP': int, 'DAM_PROP': int, 
                        'STR_WING_ROT': int, 'DAM_WING_ROT': int, 'STR_FUSE': int, 'DAM_FUSE': int, 
                        'STR_LG': int, 'DAM_LG': int, 'STR_TAIL': int, 'DAM_TAIL': int, 'STR_LGHTS': int,
                        'DAM_LGHTS': int, 'STR_OTHER': int, 'DAM_OTHER': int, 'EFFECT': object, 
                        'SKY': object, 'PRECIP': object, 'SPECIES': object, 'BIRDS_SEEN': object, 
                        'BIRDS_STRUCK': object, 'SIZE': object, 'WARNED': float, 'AOS': float, 
                        'COST_REPAIRS': float, 'COST_OTHER': float, 'NR_INJURIES': float, 
                        'NR_FATALITIES': float, 'INDICATED_DAMAGE': int},
                parse_dates=['INCIDENT_DATE'])

df = df.set_index('INCIDENT_DATE')

'''dont delete was used for deciding how to fill nan values
test = df['WARNED']
#No ATYPE EMA AIRPORT STATE
#Maybe remove BIRDS_SEEN WARNED
#Maybe AMA PHASE_OF_FLT SKY
print(test.value_counts())

print(test.isnull().sum())
#test.plot()
test.hist()

print(test.skew())
print(test.kurt())

test.plot(kind="density",
              figsize=(10,10))


plt.vlines(test.mean(),     # Plot black line at mean
           ymin=0, 
           ymax=0.4,
           linewidth=5.0)

plt.vlines(test.median(),   # Plot red line at median
           ymin=0, 
           ymax=0.4, 
           linewidth=2.0,
           color="red")
'''
#Merge these fields to show state where the incident happened
df['ENROUTE'].fillna(df['STATE'], inplace=True)
df = df.drop(['STATE'], axis=1)
df = df.rename(columns={'ENROUTE': 'STATE'})

#Fills nan values with value
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

def fillNaNValues(columns, strategy):
    change = df[columns]#Columns to change
    
    impute = Imputer(missing_values='NaN',#Change NaN values
                   strategy=strategy,#Use established strategy
                   axis=0)#Along the rows
    
    imputed = impute.fit_transform(change)# Use imputation model to get values
    
    imputed = pd.DataFrame(imputed,# Remake the DataFrame
                           index=change.index,#Get rows
                           columns=change.columns)#Get columns
    
    df[columns] = imputed[columns]#Replaces existing columns and all information in them with new

fillNaNValues(['SPEED'], 'mean')#Used only if outliners have small or no influence
fillNaNValues(['AC_MASS', 'NUM_ENGS'], 'most_frequent')#When clear correlation can be seen
fillNaNValues(['HEIGHT', 'DISTANCE', 'AOS', 'COST_OTHER', 'COST_REPAIRS'], 'median')#To resist the effects of outliers

print(df.isnull().sum())
print(df.shape)

#Writes to new file
df.to_csv('wildlife-collisions-Finished.csv', encoding = "utf-8")
print('Done!')
