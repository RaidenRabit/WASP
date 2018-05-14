# -*- coding: utf-8 -*-
"""
This file represents the prediction part organized according to BigData3 lessons
"""

import os
import pandas as pd 
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn import tree
from sklearn import cross_validation
pd.options.mode.chained_assignment = None  # default='warn'

os.chdir('dataset/Modified_dataset/') #set working directory

types = {'MONTH': int, 'DAY': int, 'DAY_OF_WEEK': int, 'AIRLINE': object,
         'FLIGHT_NUMBER': int, 'TAIL_NUMBER': object, 'ORIGIN_AIRPORT': object, 
         'DESTINATION_AIRPORT': object, 'DEPARTURE_TIME': float, 'ARRIVAL_TIME': float,
         'SCHEDULED_DEPARTURE': int, 'DEPARTURE_DELAY': float, 'TAXI_OUT': float, 
         'WHEELS_OFF': float, 'SCHEDULED_TIME': float, 'ELAPSED_TIME': float, 
         'AIR_TIME': float, 'DISTANCE': int, 'WHEELS_ON': float, 'TAXI_IN': float,
         'SCHEDULED_ARRIVAL': int, 'ARRIVAL_DELAY': float, 'DIVERTED': int, 
         'CANCELLED': int, 'CANCELLATION_REASON': object, 'AIR_SYSTEM_DELAY': float, 
         'SECURITY_DELAY': float, 'AIRLINE_DELAY': float, 'LATE_AIRCRAFT_DELAY': float, 
         'WEATHER_DELAY': float, 'CRASHED': int}
   
df = pd.read_csv('wildlife-collisions_Joined2015.csv',
                 dtype=types)

#Supervised learning using the decision tree
#X- feature
#y- lable

#'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'CANCELLATION_REASON'
X = df[['MONTH', 'DAY', 'DEPARTURE_TIME', 'ARRIVAL_TIME', 'DAY_OF_WEEK',
         'SCHEDULED_DEPARTURE', 'DEPARTURE_DELAY', 'TAXI_OUT', 
         'WHEELS_OFF', 'SCHEDULED_TIME', 'ELAPSED_TIME', 
         'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN',
         'SCHEDULED_ARRIVAL', 'ARRIVAL_DELAY', 'DIVERTED', 
         'CANCELLED', 'AIR_SYSTEM_DELAY', 'FLIGHT_NUMBER', 
         'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 
         'WEATHER_DELAY']]
y = df[['CRASHED']]

predict = 100

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X[:-predict], y[:-predict], test_size=0.3, random_state=7)
model = tree.DecisionTreeClassifier()
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(accuracy)

print(model.predict(X[-predict:]))
print(y[-predict:])

#############################################################################################
types = {'INCIDENT_DATE': object, 'OPERATOR': object, 'ATYPE': object, 
         'AC_CLASS': object, 'AC_MASS': int, 'NUM_ENGS': int, 
         'TYPE_ENG': object, 'AIRPORT': object, 'STATE': object, 
         'HEIGHT': float, 'SPEED': float, 'DISTANCE': float, 'PHASE_OF_FLT': object, 
         'STR_RAD	DAM_RAD': int, 'STR_WINDSHLD': int, 'DAM_WINDSHLD': int,
         'STR_NOSE': int, 'DAM_NOSE': int, 'STR_ENG1': int, 'DAM_ENG1': int, 'STR_ENG2': int,
         'DAM_ENG2': int, 'STR_ENG3': int, 'DAM_ENG3': int, 'STR_ENG4': int,
         'DAM_ENG4': int, 'INGESTED': int, 'STR_PROP': int, 'DAM_PROP': int, 'STR_WING_ROT': int,	
         'DAM_WING_ROT': int, 'STR_FUSE': int, 'DAM_FUSE': int, 'STR_LG': int, 'DAM_LG': int,
         'STR_TAIL': int, 'DAM_TAIL': int, 'STR_LGHTS': int, 
         'DAM_LGHTS': int, 'STR_OTHER': int, 'DAM_OTHER': int,
         'EFFECT': object, 'SKY': object, 'PRECIP': object, 'SPECIES': object, 'BIRDS_STRUCK': object,
         'SIZE': object, 'AOS': float, 'NR_INJURIES': int, 'NR_FATALITIES': int, 'INDICATED_DAMAGE': int,	'COSTS': float}

df = pd.read_csv('wildlife-collisions.csv',
                 dtype=types)

df['INCIDENT_DATE'] = df['INCIDENT_DATE'].astype(str).str.extract('(....-..-..)', expand=True)
df['Year'], df['Month'], df['Day'] = df['INCIDENT_DATE'].str.split('-').str
df = df.drop(['INCIDENT_DATE'], axis=1)

df = pd.get_dummies(df, columns=['AC_CLASS'])
df = pd.get_dummies(df, columns=['STATE'])
df = pd.get_dummies(df, columns=['TYPE_ENG'])
df = pd.get_dummies(df, columns=['PHASE_OF_FLT'])
df = pd.get_dummies(df, columns=['EFFECT'])
df = pd.get_dummies(df, columns=['SKY'])
df = pd.get_dummies(df, columns=['PRECIP'])
df = pd.get_dummies(df, columns=['BIRDS_STRUCK'])
df = pd.get_dummies(df, columns=['SIZE'])

df = df.drop(['OPERATOR', 'ATYPE', 'AIRPORT', 'SPECIES'], axis=1)

#Deciding how many cluster are needed by using the Elbow Analysis

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

cluster_range  = range( 1, 10 )
cluster_errors = []

for num_clusters in cluster_range:
    print(num_clusters)
    clusters = KMeans( num_clusters )
    clusters.fit( X_scaled )
    cluster_errors.append( clusters.inertia_ )
    
clusters_df = pd.DataFrame( { "num_clusters":cluster_range, "cluster_errors": cluster_errors } )

print(clusters_df)

plt.figure(figsize=(12,6))
plt.plot( clusters_df.num_clusters, clusters_df.cluster_errors, marker = "o" )
plt.show()

#Unsupervised learning using k means
predict = 100

reduced_data = PCA(n_components=2).fit_transform(df[:-predict])
kmeans = KMeans(init='k-means++', n_clusters=5, n_init=10).fit(reduced_data)
df['clusters'] = np.nan
df['clusters'][:-predict] = kmeans.labels_

#Analyze the clusters
print(df.groupby(['clusters']).mean())
unique_elements, counts_elements = np.unique(kmeans.labels_, return_counts=True)
print(np.asarray((unique_elements, counts_elements)))

#Visualization of actual data
plt.scatter(reduced_data[:,0], reduced_data[:,1], c=kmeans.labels_, cmap='rainbow')  
plt.scatter(kmeans.cluster_centers_[:,0] ,kmeans.cluster_centers_[:,1], marker='x', color='w')   
plt.title('K-means clustering on the wildlife-collisions dataset')
plt.xticks(())
plt.yticks(())
plt.show()

#Prediction
reduced_data = PCA(n_components=2).fit_transform(df.loc[:, df.columns != 'clusters'][-predict:])
Z = kmeans.predict(reduced_data)
df['clusters'][-predict:] = Z
unique_elements, counts_elements = np.unique(Z, return_counts=True)
print(np.asarray((unique_elements, counts_elements)))