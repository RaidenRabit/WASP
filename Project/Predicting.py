# -*- coding: utf-8 -*-
"""
This file represents the prediction part organized according to BigData3 lessons
"""

import os
import pandas as pd 
import numpy as np
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


##########################################################################
#shows how data was clustared
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.get_dummies(df, columns=['CANCELLATION_REASON'])

#Standardize
#removed: AIRLINE, FLIGHT_NUMBER, TAIL_NUMBER
#ORIGIN_AIRPORT DESTINATION_AIRPORT
clmns = ['MONTH', 'DAY',
         'DEPARTURE_TIME', 'ARRIVAL_TIME', 'DAY_OF_WEEK',
         'SCHEDULED_DEPARTURE', 'DEPARTURE_DELAY', 'TAXI_OUT', 
         'WHEELS_OFF', 'SCHEDULED_TIME', 'ELAPSED_TIME', 
         'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN',
         'SCHEDULED_ARRIVAL', 'ARRIVAL_DELAY', 'DIVERTED', 
         'CANCELLED', 'AIR_SYSTEM_DELAY', 
         'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 
         'WEATHER_DELAY', 'CRASHED', 
         'CANCELLATION_REASON_0', 'CANCELLATION_REASON_B', 'CANCELLATION_REASON_A', 
         'CANCELLATION_REASON_C', 'CANCELLATION_REASON_D']
df_tr_std = stats.zscore(df[clmns])

#Cluster the data
kmeans = KMeans(n_clusters=3, random_state=0).fit(df_tr_std)
labels = kmeans.labels_

#Glue back to originaal data
df['clusters'] = labels

#Add the column into our list
clmns.extend(['clusters'])

#Lets analyze the clusters
print(df[clmns].groupby(['clusters']).mean())

sns.lmplot('DEPARTURE_TIME', 'ARRIVAL_TIME', 
           data=df, 
           fit_reg=False, 
           hue="clusters",  
           scatter_kws={"marker": "D", 
                        "s": 100})
plt.title('Clusters')
plt.xlabel('DEPARTURE_TIME')
plt.ylabel('ARRIVAL_TIME')

'''
############################################################
#Supervised learning using the decision tree
#X- feature
#y- lable

from sklearn import tree
from sklearn import cross_validation
#df_tr = pd.get_dummies(df_tr, columns=['timeOfDay'])
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

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X[:-10], y[:-10], test_size=0.3, random_state=7)
model = tree.DecisionTreeClassifier()
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(accuracy)

print(model.predict(X[-10:]))#last 10
print(y[-10:])
'''
'''
#helpful
import matplotlib.pyplot as plt  
import numpy as np  
from sklearn.cluster import KMeans  

X = np.array([[5,3],  
     [10,15],
     [15,12],
     [24,10],
     [30,45],
     [85,70],
     [71,80],
     [60,78],
     [55,52],
     [80,91],])

kmeans = KMeans(n_clusters=2)  
kmeans.fit(X)  
print(kmeans.cluster_centers_)  
print(kmeans.labels_) 
plt.scatter(X[:,0],X[:,1], c=kmeans.labels_, cmap='rainbow')  
plt.scatter(kmeans.cluster_centers_[:,0] ,kmeans.cluster_centers_[:,1], color='black')  
'''
'''
#######################################################
#Shows unsupervised learning- k means
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

data = scale(df[['MONTH', 'DAY', 'DEPARTURE_TIME', 'ARRIVAL_TIME', 'DAY_OF_WEEK',
         'SCHEDULED_DEPARTURE', 'DEPARTURE_DELAY', 'TAXI_OUT', 
         'WHEELS_OFF', 'SCHEDULED_TIME', 'ELAPSED_TIME', 
         'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN',
         'SCHEDULED_ARRIVAL', 'ARRIVAL_DELAY', 'DIVERTED', 
         'CANCELLED', 'AIR_SYSTEM_DELAY', 'FLIGHT_NUMBER', 
         'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 
         'WEATHER_DELAY', 'CRASHED']])

# Visualize the results on PCA-reduced data
reduced_data = PCA(n_components=2).fit_transform(data)
kmeans = KMeans(init='k-means++', n_clusters=3, n_init=10)
kmeans.fit(reduced_data)

# Plot the decision boundary. For that, we will assign a color to each
x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, .02), np.arange(y_min, y_max, .02))

# Obtain labels for each point in mesh. Use last trained model.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

unique_elements, counts_elements = np.unique(Z, return_counts=True)

#print(np.asarray((unique_elements, counts_elements)))
#pd.DataFrame(Z).hist()

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')

plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)

# Plot the centroids as a white X
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)

plt.title('K-means clustering on the dataset')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.show()
'''

'''
##################################################################
#Deciding how many cluster are needed by using the Elbow Analysis
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

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
'''