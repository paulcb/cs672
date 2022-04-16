from sklearn.cluster import KMeans
import numpy as np
from collections import Counter

X = np.array([[1, 2], [1, 4], [1, 0],
              [10, 2], [10, 4], [10, 0]])
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
kmeans.labels_
kmeans.predict([[0, 0], [12, 3]])
print(kmeans.cluster_centers_)
import pandas as pd
values = pd.read_csv('~/Documents/stuff.csv', header=None).values
kmeans = KMeans(n_clusters=5, random_state=0).fit(values)
print(kmeans.labels_)
print(kmeans.cluster_centers_)
print(Counter(kmeans.labels_))
for label in kmeans.labels_:
  print(label)