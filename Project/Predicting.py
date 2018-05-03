# -*- coding: utf-8 -*-
"""
This file represents the prediction part organized according to BigData3 lessons
"""

import os
import pandas as pd 
import numpy as np

os.chdir('dataset/Modified_dataset/') #set working directory

encoding = 'utf-8'
parse_dates = ['INCIDENT_DATE']
types = {'OPERATOR': object, 'AC_CLASS': object, 'AC_MASS': int, 
         'NUM_ENGS': int, 'TYPE_ENG': object, 'AIRPORT': object, 
         'STATE': object, 'HEIGHT': int, 'SPEED': float, 
         'DISTANCE': float, 'PHASE_OF_FLT': object, 'STR_RAD': bool, 
         'DAM_RAD': bool, 'STR_WINDSHLD': bool, 'DAM_WINDSHLD': bool, 
         'STR_NOSE': bool, 'DAM_NOSE': bool, 'STR_ENG1': bool, 
         'DAM_ENG1': bool, 'STR_ENG2': bool, 'DAM_ENG2': bool, 
         'STR_ENG3': bool, 'DAM_ENG3': bool, 'STR_ENG4': bool, 
         'DAM_ENG4': bool, 'INGESTED': bool, 'STR_PROP': bool, 
         'DAM_PROP': bool, 'STR_WING_ROT': bool, 'DAM_WING_ROT': bool, 
         'STR_FUSE': bool, 'DAM_FUSE': bool, 'STR_LG': bool, 
         'DAM_LG': bool, 'STR_TAIL': bool, 'DAM_TAIL': bool, 
         'STR_LGHTS': bool, 'DAM_LGHTS': bool, 'STR_OTHER': bool,
         'DAM_OTHER': bool, 'EFFECT': object, 'SKY': object, 
         'PRECIP': object, 'SPECIES': object, 'BIRDS_STRUCK': object, 
         'SIZE': object, 'AOS': float, 'COSTS': float, 
         'NR_INJURIES': int, 'NR_FATALITIES': int, 'INDICATED_DAMAGE': bool}
   
df = pd.read_csv('wildlife-collisions.csv', 
                 encoding = encoding,
                 parse_dates=parse_dates,
                 dtype=types)

#print(df.corr())
#df['STATE'].hist()
#df['lable'] = df['STATE'].shift(10)
#import matplotlib.pyplot as plt
#df.plot();

#X- features
#y- lable

'''
from sklearn import cross_validation
#from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression

predict = 'COSTS'
#X = df.drop([predict], axis=1)#Everything but predict column
X = df[['STR_RAD', 'DAM_RAD', 'STR_WINDSHLD', 'DAM_WINDSHLD', 
         'STR_NOSE', 'DAM_NOSE', 'STR_ENG1', 
         'DAM_ENG1', 'STR_ENG2', 'DAM_ENG2', 
         'STR_ENG3', 'DAM_ENG3', 'STR_ENG4', 
         'DAM_ENG4', 'INGESTED', 'STR_PROP', 
         'DAM_PROP', 'STR_WING_ROT', 'DAM_WING_ROT', 
         'STR_FUSE', 'DAM_FUSE', 'STR_LG', 
         'DAM_LG', 'STR_TAIL', 'DAM_TAIL', 
         'STR_LGHTS', 'DAM_LGHTS', 'STR_OTHER']]
y = df[predict]
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3, random_state=7)

#model = GaussianNB()
model = LinearRegression(n_jobs=-1)#n_jobs how many threads to use
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(accuracy)
'''
'''
from mpl_toolkits.mplot3d import Axes3D 
from sklearn.cluster import KMeans 
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

#iris = load_iris()
#X = iris.data
X = np.array(df[['AC_MASS', 'NUM_ENGS', 'COSTS']])

est = KMeans(n_clusters=7)
est.fit(X)

ax = Axes3D(plt.figure(1, figsize=(4, 3)), rect=[0, 0, .95, 1], elev=48, azim=134)
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=est.labels_.astype(np.float))

ax.set_xlabel('AC_MASS')
ax.set_ylabel('NUM_ENGS')
ax.set_zlabel('COSTS')
plt.show()
'''
from sklearn import cross_validation
from sklearn.cluster import KMeans

X_train, X_test = cross_validation.train_test_split(df[['STR_RAD', 'DAM_RAD', 'STR_WINDSHLD', 'DAM_WINDSHLD', 
         'STR_NOSE', 'DAM_NOSE', 'STR_ENG1', 
         'DAM_ENG1', 'STR_ENG2', 'DAM_ENG2', 
         'STR_ENG3', 'DAM_ENG3', 'STR_ENG4', 
         'DAM_ENG4', 'INGESTED', 'STR_PROP', 
         'DAM_PROP', 'STR_WING_ROT', 'DAM_WING_ROT', 
         'STR_FUSE', 'DAM_FUSE', 'STR_LG', 
         'DAM_LG', 'STR_TAIL', 'DAM_TAIL', 
         'STR_LGHTS', 'DAM_LGHTS', 'STR_OTHER']], test_size=0.3, random_state=7)

model = KMeans(n_clusters=10, random_state=7)
model.fit(X_train)

predicted= model.predict(X_test)

unique_elements, counts_elements = np.unique(predicted, return_counts=True)
print("Frequency of unique values of the said array:")
print(np.asarray((unique_elements, counts_elements)))

pd.DataFrame(predicted).hist()