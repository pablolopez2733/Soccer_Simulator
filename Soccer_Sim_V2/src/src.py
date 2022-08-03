import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

################################################
################## READ DATA ###################
################################################
wd ='C:/Users/USER/Documents/Github_Repos/Soccer_Simulator/'
spi_ranks = pd.read_csv(f"{wd}Soccer_Sim_V2/data/spi_global_rankings.csv")
matches = pd.read_csv(f"{wd}Soccer_Sim_V2/data/spi_matches_latest.csv")

# Filtrar juegos de este torneo:
ligamx = matches[matches['league_id']== 1952]
teams = spi_ranks[spi_ranks['league']== 'Mexican Primera Division Torneo Apertura']


################################################
################## CLUSTERS ####################
################################################

# Calcular spi promedio este torneo
for team in teams['name']:
  aux = ligamx[(ligamx['team1']==team)|(ligamx['team2']==team)]
  aux.loc[aux['team1']==team,'spi_f'] = aux['spi1']
  aux.loc[aux['team2']==team,'spi_f'] = aux['spi2']
  avg_spi = aux['spi_f'].mean()
  teams.loc[teams['name']==team,'avg_spi']=avg_spi


# Cluster teams by spi and transfrmarket value (with standarization)
wcss = []
cols_to_standardize = ['avg_spi','transfermarkt']
data_to_standardize =teams[cols_to_standardize] 
scaler = StandardScaler().fit(data_to_standardize)
standardized_data = teams.copy()
standardized_columns = scaler.transform(data_to_standardize)
standardized_data[cols_to_standardize] = standardized_columns
x=standardized_data[cols_to_standardize]

for i in range(1, 8):
  kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
  kmeans.fit(x)
  wcss.append(kmeans.inertia_)
plt.plot(range(1, 8), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()
# 3 clusters

kmeans = KMeans(n_clusters=3, init='k-means++', max_iter=100, n_init=10, random_state=0)
teams['cluster'] = kmeans.fit_predict(x)

# Grafica de clusters:
LABEL_COLOR_MAP = {0 : '#c92851',
                   1 : '#eba771',
                   2 : '#2b9b8f'}
teams['cluster_color'] = [LABEL_COLOR_MAP[l] for l in teams['cluster']]
plt.scatter(teams['transfermarkt'],teams['avg_spi'],c=teams['cluster_color'])
plt.show()
