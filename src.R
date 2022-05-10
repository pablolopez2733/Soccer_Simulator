# Cargar funciones
source("utils.R")

# Leer data
df <- read.csv("clausura_2022.csv")

# Equipo visitante
away <- ""
# Equipo local
home <- ""

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
prob_matrix <- match_matrix(lambdas)