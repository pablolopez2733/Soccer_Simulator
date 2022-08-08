import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rcParams
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.ticker as ticker
from PIL import Image
import urllib
import matplotlib.patheffects as path_effects
import os
import matplotlib.font_manager as fm

wd ='C:/Users/USER/Documents/Github_Repos/Soccer_Simulator/'



# import fonts:
font_path = f"{wd}resources/fonts" #Set the path to where the fonts are located

for y in os.listdir(f"{font_path}"):
    if y.split(".")[-1] == "ttf":
        fm.fontManager.addfont(f"{font_path}/{y}")
        try:
            fm.FontProperties(weight=y.split("-")[-1].split(".")[0].lower(), fname=y)
        except Exception as e:
            print(f"Font {y} could not be added.")
            continue

rcParams['font.family'] = 'Karla'

################################################
################## READ DATA ###################
################################################

spi_ranks = pd.read_csv(f"{wd}Soccer_Sim_V2/data/spi_global_rankings.csv")
matches = pd.read_csv(f"{wd}Soccer_Sim_V2/data/spi_matches_latest.csv")
abb = pd.read_csv(f"{wd}Soccer_Sim_V2/data/abb.csv")

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

#jjoin rapido para abbreviations
teams = teams.merge(abb,left_on='name', right_on='name')


# -- Plot----------------------------------------------------------------------

fig = plt.figure(figsize = (7,5), dpi = 600, facecolor=("#EEE9E5"))
plt.rcParams["font.family"] = "Karla"
layout = [["logo"]* 2 + ["text"] * 8,
          ["edge"]+["bar"] * 9,
          ["edge"]+["bar"] * 9,
          ["edge"]+["bar"] * 9,
          ["edge"]+["bar"] *9 ] 

ax_dict = fig.subplot_mosaic(
    layout
)


# -- Add the logo
#fotmob_url = "https://images.fotmob.com/image_resources/logo/teamlogo/"
#club_icon = Image.open(urllib.request.urlopen(f"{fotmob_url}{8456:.0f}.png"))
#url = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/MX_logo.png/974px-MX_logo.png"
#icon = Image.open(urllib.request.urlopen(url))
icon = Image.open(f"{wd}resources/logomx.png")
ax_dict["logo"].imshow(icon)
ax_dict["logo"].axis("off")
ax_dict["edge"].axis("off")
ax_dict['logo'].autoscale_view('tight')
ax_dict["text"].axis("off")

# -- Add the title
ax_dict["text"].annotate(
    xy = (0, 0.8),
    text = "Los equipos más valiosos son los que mejor \njuegan en el Apertura 2022",
    ha = "left",
    va = "center",
    font = "Karla",
    #weight = 'bold',
    size = 14       
)

ax_dict["text"].annotate(
    xy = (0, 0.2),
    text = "Agrupando matemáticamente se forman 3 grupos donde el valor de mercado\ninfluye mucho en el desempeño.",
    va = "center",
    ha = "left",
 	fontsize = 8,
    color = "#4E616C",
    #font = "Karla"      
)


ax_dict["text"].axis("off")

# -- Add the bar chart

ax_dict["bar"].scatter(teams['transfermarkt'],teams['avg_spi'],c=teams['cluster_color'])
ax_dict["bar"].xaxis.set_major_locator(ticker.MultipleLocator(10))
ax_dict["bar"].yaxis.set_major_locator(ticker.MultipleLocator(5))
ax_dict["bar"].grid(True, ls = ":", color = "lightgray")
ax_dict["bar"].set_xlabel("Valor de mercado del equipo\n(millones de dls)")
ax_dict["bar"].set_ylabel("Soccer Power Index promedio")
ax_dict['bar'].xaxis.set_major_formatter('${x:1.0f}')


for x_,y_,abbrev in zip(teams['transfermarkt'],teams['avg_spi'],teams['abrev']):
    text_ = ax_dict["bar"].annotate(
        xy = (x_, y_),
        text = abbrev,
        ha = "center",
        va = "top",
        xytext = (x_, y_+ 2.5),
        #textcoords = "figure points",
        font = 'DejaVu Sans',
        arrowprops=dict(arrowstyle="->", color='black'),
        weight = "bold"
    )

    text_.set_path_effects(
                [path_effects.Stroke(linewidth=2.5, foreground="white"), 
                path_effects.Normal()]
            )
    


# -- Customize the "bar" ax
ax_dict["bar"].spines["top"].set_visible(False)
ax_dict["bar"].spines["right"].set_visible(False)
ax_dict["bar"].set_facecolor("#EFE9E6")
plt.figtext(0.9, 0.03,'Viz: @Landeros_p33\nCódigo original: @sonofacorner',
            fontsize=6,horizontalalignment='right',color = "#4E616C")

# import  matplotlib.font_manager
# flist = matplotlib.font_manager.get_fontconfig_fonts()
# names = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in flist]
# print (names)