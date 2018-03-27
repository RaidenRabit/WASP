import pandas as pd
#from pandas.tools.plotting import scatter_matrix
from sklearn.preprocessing import Imputer
#import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt
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
                        'BIRDS_STRUCK': object, 'SIZE': object, 'WARNED': object, 'AOS': float, 
                        'COST_REPAIRS': float, 'COST_OTHER': float, 'NR_INJURIES': float, 
                        'NR_FATALITIES': float, 'INDICATED_DAMAGE': int})

df = df.set_index('INCIDENT_DATE')

df['WARNED'] = df['WARNED'].map({'Y': 1, 'N': 0})

df['SIZE'].fillna(df['SIZE'].value_counts().idxmax(), inplace=True)
df['BIRDS_STRUCK'].fillna(df['BIRDS_STRUCK'].value_counts().idxmax(), inplace=True)
df['BIRDS_SEEN'].fillna(df['BIRDS_SEEN'].value_counts().idxmax(), inplace=True)
df['SPECIES'].fillna(df['SPECIES'].value_counts().idxmax(), inplace=True)
df['PRECIP'].fillna(df['PRECIP'].value_counts().idxmax(), inplace=True)
df['SKY'].fillna(df['SKY'].value_counts().idxmax(), inplace=True)
df['EFFECT'].fillna(df['EFFECT'].value_counts().idxmax(), inplace=True)
df['DAMAGE'].fillna(df['DAMAGE'].value_counts().idxmax(), inplace=True)
df['PHASE_OF_FLT'].fillna(df['PHASE_OF_FLT'].value_counts().idxmax(), inplace=True)
df['AC_CLASS'].fillna(df['AC_CLASS'].value_counts().idxmax(), inplace=True)
df['TYPE_ENG'].fillna(df['TYPE_ENG'].value_counts().idxmax(), inplace=True)
#print(df['STATE'].value_counts())
#maybe remove or join: ENROUTE
#cant choose: OPERATOR, ATYPE, EMA, AIRPORT, STATE
#maybe: AMA

###########################################################################################

change_mean = df[['HEIGHT', 'SPEED', 'DISTANCE']] #Average

mean = Imputer(missing_values='NaN',  # Create imputation model
              strategy='mean',       # Use mean imputation
              axis=0)                # Impute by column

imputed_mean = mean.fit_transform(change_mean) # Use imputation model to get values

imputed_mean = pd.DataFrame(imputed_mean,    # Remake the DataFrame
                           index=change_mean.index,
                           columns=change_mean.columns)

df[['HEIGHT', 'SPEED', 'DISTANCE']] = imputed_mean[['HEIGHT', 'SPEED', 'DISTANCE']]

###########################################################################################

change_most_frequent = df[['AC_MASS', 'NUM_ENGS', 'WARNED']] #Variable with highest frequency

most_frequent = Imputer(missing_values='NaN',
              strategy='most_frequent',
              axis=0)

imputed_most_frequent = most_frequent.fit_transform(change_most_frequent)

imputed_most_frequent = pd.DataFrame(imputed_most_frequent,
                           index=change_most_frequent.index,
                           columns=change_most_frequent.columns)

df[['AC_MASS', 'NUM_ENGS', 'WARNED']] = imputed_most_frequent[['AC_MASS', 'NUM_ENGS', 'WARNED']]

###########################################################################################

change_median = df[['AOS', 'COST_REPAIRS', 'COST_OTHER']] #Middle number of set

median = Imputer(missing_values='NaN',
              strategy='median',
              axis=0)

imputed_median = median.fit_transform(change_median)

imputed_median = pd.DataFrame(imputed_median,
                           index=change_median.index,
                           columns=change_median.columns)

df[['AOS', 'COST_REPAIRS', 'COST_OTHER']] = imputed_median[['AOS', 'COST_REPAIRS', 'COST_OTHER']]

###########################################################################################

print(df.isnull().sum())
print(df.shape)

#Writes to new file
df.to_csv('wildlife-collisions-Finished.csv', encoding = "utf-8")
print('Done!')

'''
colmeans = df._get_numeric_data().sum()/df.shape[0]
print(colmeans)

centered = df._get_numeric_data()-colmeans
print(centered.describe())

column_deviations = df._get_numeric_data().std(axis=0)   # Get column standard deviations
centered_and_scaled = centered/column_deviations 
print(centered_and_scaled.describe())

#df['AOS'].hist(figsize=(8,8), bins=30)

print(df.corr())

scatter_matrix(df._get_numeric_data().ix[:,0:6],   # Make a scatter matrix of 6 columns
               figsize=(10, 10),   # Set plot size
               diagonal='kde')     # Show distribution estimates on diagonal
'''
'''
print(df['OPERATOR'].value_counts().to_frame())

#print(df['PHASE_OF_FLT'].value_counts().plot(kind="bar"))

print(df['OPERATOR'].isnull().sum())
corr = df.corr()
_, ax = plt.subplots(figsize=(13,10))
_ = sns.heatmap(corr, ax=ax,xticklabels=corr.columns.values,yticklabels=corr.columns.values)
'''