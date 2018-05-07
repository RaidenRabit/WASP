# -*- coding: utf-8 -*-
"""
This file represents the prediction part organized according to BigData3 lessons
"""

import os
import pandas as pd 
import numpy as np

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

#X- feature
#y- lable

from sklearn import tree
from sklearn import cross_validation

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

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3, random_state=7)
model = tree.DecisionTreeClassifier()
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(accuracy)

#takes long time and shows how the values group up
from sklearn.cluster import KMeans
'''
X_train, X_test = cross_validation.train_test_split(X, test_size=0.3, random_state=7)

model = KMeans(n_clusters=10, random_state=7)
model.fit(X_train)

predicted= model.predict(X_test)

unique_elements, counts_elements = np.unique(predicted, return_counts=True)
print("Frequency of unique values of the said array:")
print(np.asarray((unique_elements, counts_elements)))

pd.DataFrame(predicted).hist()
'''

#Show corolations
from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.pyplot as plt

X = np.array(df[['MONTH', 'CRASHED', 'DAY_OF_WEEK']])

est = KMeans(n_clusters=7)
est.fit(X)

ax = Axes3D(plt.figure(1, figsize=(4, 3)), rect=[0, 0, .95, 1], elev=48, azim=134)
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=est.labels_.astype(np.float))

ax.set_xlabel('MONTH')
ax.set_ylabel('CRASHED')
ax.set_zlabel('DAY_OF_WEEK')
plt.show()
