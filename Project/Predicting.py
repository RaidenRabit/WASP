# -*- coding: utf-8 -*-
"""
This file represents the prediction part organized according to BigData3 lessons
"""

import os
import pandas as pd 
import numpy as np

os.chdir('dataset/Modified_dataset/') #set working directory

types = {'DATE': object, 'AIRLINE': object, 'FLIGHT_NUMBER': int, 
         'TAIL_NUMBER': object, 'ORIGIN_AIRPORT': object, 'DESTINATION_AIRPORT': object, 
         'DEPARTURE_TIME': object, 'ARRIVAL_TIME': object, 'CRASHED': int}
   
df = pd.read_csv('wildlife-collisions_Joined2015.csv',
                 dtype=types)

#print(df.corr())
#df['STATE'].hist()
#df['lable'] = df['STATE'].shift(10)
#import matplotlib.pyplot as plt
#df.plot();

#X- features
#y- lable

from sklearn import tree
from sklearn import cross_validation

X = df[['FLIGHT_NUMBER']]
y = df[['CRASHED']]

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3, random_state=7)
model = tree.DecisionTreeClassifier()
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(accuracy)

'''
from mpl_toolkits.mplot3d import Axes3D 
from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt

X = np.array(df[['FLIGHT_NUMBER', 'CRASHED', 'COSTS']])

est = KMeans(n_clusters=7)
est.fit(X)

ax = Axes3D(plt.figure(1, figsize=(4, 3)), rect=[0, 0, .95, 1], elev=48, azim=134)
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=est.labels_.astype(np.float))

ax.set_xlabel('AC_MASS')
ax.set_ylabel('NUM_ENGS')
ax.set_zlabel('COSTS')
plt.show()
'''
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
'''