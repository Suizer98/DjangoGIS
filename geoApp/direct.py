import numpy as np
import pandas as pd
file_url = "latlng2.csv"

data = pd.read_csv(file_url)
features = data[['lat', 'lng']]
print(features)

from sklearn.cluster import KMeans
# create kmeans model/object
kmeans = KMeans(
    init="random",
    n_clusters=11,
    n_init=10,
    max_iter=300,
    random_state=42
)

# do clustering
kmeans.fit(features)
# save results
labels = kmeans.labels_

# send back into dataframe and display it
data['cluster'] = labels
print(labels)

# display the number of mamber each clustering
_clusters = data.groupby('cluster')['lat'].count()
print(_clusters)

# force same no of cluster amount

data = pd.read_csv("latlng2.csv")
features = data[['lat', 'lng']]
X = np.array(features)
print(X[:10])

from k_means_constrained import KMeansConstrained
clf = KMeansConstrained(
    n_clusters=20,
    size_min=15,
    size_max=16,
    random_state=0
)


clf.fit_predict(X)
# save results
labels = clf.labels_
# send back into dataframe and display it
data['cluster'] = labels
# display the number of mamber each clustering
_clusters = data.groupby('cluster')['lat'].count()
print(_clusters)

import folium
colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', \
     'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', \
     'darkpurple', 'pink', 'lightblue', 'lightgreen', 'gray', \
     'black', 'lightgray', 'red', 'blue', 'green', 'purple', \
     'orange', 'darkred', 'lightred', 'beige', 'darkblue', \
     'darkgreen', 'cadetblue', 'darkpurple','pink', 'lightblue', \
     'lightgreen', 'gray', 'black', 'lightgray' ]
lat = data.iloc[0]['lat']
lng = data.iloc[0]['lng']


map = folium.Map(location=[lng, lat], zoom_start=12)
for _, row in data.iterrows():
    folium.CircleMarker(
        location=[row["lng"], row["lat"]],
        radius=12,
        weight=2,
        fill=True,
        fill_color=colors[int(row["cluster"])],
        color=colors[int(row["cluster"])]
    ).add_to(map)

# map

