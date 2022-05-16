# Cargar funciones
source("utils.R")

# Leer data
df <- read.csv("data/clausura_2022.csv")

# Equipo visitante
away <- "America"
# Equipo local
home <- "Puebla"

################################################################################
############################### SIMULACIÓN #####################################
################################################################################
# Numero de simulaciones:
n <- 10000
# Calculamos los lambdas de cada equipo:
lambdas <- calc_lambda(df, home, away)
# Simulamos el partido n veces:
resultado <- sim_match(lambdas, n)
# Matriz de calor
prob_matrix <- match_matrix(lambdas, home, away)
