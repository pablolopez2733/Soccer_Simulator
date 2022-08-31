library(devtools)
library(rethinking)
library(tidyverse)
library(gganimate)
library(reticulate)
library(factoextra)

# Get working directory
wd = getwd()

# Generate clusters from python script
py_run_file(paste0(wd,'/Soccer_Sim_V2/src/clusters.py'))


# Read data ====================================================================
tdy <- gsub('[-]', '_', Sys.Date())
cluster.22 = read.csv(paste0('Soccer_Sim_V2/outputs/team_clusters_2022.csv'),encoding="UTF-8")
games = read.csv(paste0(wd,'/Soccer_Sim_V2/data/soccer-spi/spi_matches_latest.csv'), encoding="latin-1")
games_total = read.csv(paste0(wd,'/Soccer_Sim_V2/data/soccer-spi/spi_matches.csv'),encoding="UTF-8")
val21 = read.csv(paste0(wd,'/Soccer_Sim_V2/data/val_merc_2021.csv'),encoding="latin-1")


# Cluster past season ==========================================================
# extract last years games
spi21 <- data.frame(matrix(ncol = 3, nrow = 0))
x <- c("name", "spi", "market_value")
colnames(spi21) <- x

liga21 <- games_total %>% 
  filter(league_id == 1975 & season == 2021) 

teams <- unique(liga21$team1)

for (t in teams) {
  aux <- liga21 %>% 
    filter(team1 == t | team2 == t) %>% 
    mutate(spi_f = ifelse(team1 == t, spi1, spi2))
  avg_spi <- mean(aux$spi_f)
  m_value <- val21[which(val21$name == t),2]
  spi21[nrow(spi21) + 1,] = c(t,avg_spi,m_value)
}
data <- spi21 %>% select(-c(name)) 
dat <- data.frame(lapply(data, function(x) as.numeric(as.character(x))))
scaled_data <- scale(dat)
# Elbow method for kmeans
fviz_nbclust(scaled_data, kmeans, method = "wss") 
# 3 clusters is optimal
set.seed(33)
km.res <- kmeans(scaled_data, 3, nstart = 25)
cluster.21 <- spi21
cluster.21$cluster_21 <- km.res$cluster
fviz_cluster(km.res, data = dat)


# Now we need to extract history for face to face
juegos <- games %>% 
  filter(league_id == 1952)

# A data de juegos le pegas los clusters y ya jala

