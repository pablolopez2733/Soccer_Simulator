library(tidyverse)

# Funcion para calular las lambdas de cada equipo ==============================
calc_lambda <- function(league,h_team,a_team){
  
   # Goles anotados por liga de visita
   league_avg_away <- mean(league$A_GF/league$A_JJ)
   league_total_away <- sum(league$A_GF)
   
   # Goles anotados por liga de local
   league_avg_home <- mean(league$H_GF/league$H_JJ)
   league_total_home <- sum(league$H_GF)
   
   # Home data
   home_df = league[league['Club']== h_team,]
   h_total = home_df$H_GF
   h_average = home_df$H_GF/home_df$H_JJ
   h_conceed_total = home_df$H_GC
   h_conceed_avg = home_df$H_GC/home_df$H_JJ
   
   # Away data:
   away_df = league[league['Club']== a_team,]
   a_total = away_df$A_GF
   a_average = away_df$A_GF/away_df$A_JJ
   a_conceed_total = away_df$A_GC
   a_conceed_avg = away_df$A_GC/away_df$A_JJ
   
   # Attack Strenghts:
   h_attack_str = h_average / league_avg_home
   a_attack_str = a_average / league_avg_away
   
   # Defense Strengths
   h_defence_str = h_conceed_avg / league_avg_away
   a_defence_str = a_conceed_avg / league_avg_home
   
   # Avg goals scored against each other
   h_expect = h_attack_str * a_defence_str * league_avg_home
   a_expect = a_attack_str * h_defence_str * league_avg_away
   
   # Lambdas:
   equipos <- c(h_team,a_team)
   xgs <- c(h_expect,a_expect)
   
   lambdas <- data.frame(h_lambda = h_expect, a_lambda = a_expect)
   return(lambdas)
  
}

# Funcion Poisson:
prob_poisson <- function(l,x){
  probability = ((l**x) * math.exp(-l)) / math.factorial(x)
  return(probability*100)
}

# Funcion para simular el partido n veces ======================================
sim_match <- function(lambs,n){
  # vars:
  goles <- seq(0,6)
  a <- NULL
  h <- NULL
  h_wins <- NULL
  a_wins <- NULL
  tie <- NULL
  iteracion <- NULL
  # prob vectors for each goal:
  h_goals <- dpois(goles, lambs$h_lambda)
  a_goals <- dpois(goles, lambs$a_lambda)
  
  
  for (i in 1:n) {
    h[i] <- sample(goles,1,prob=h_goals,replace = TRUE)
    a[i] <- sample(goles,1,prob=a_goals,replace = TRUE)
    iteracion[i] <- i
  }
  sim <- as.data.frame(cbind(iteracion,h,a))
  sim <- sim %>% 
    mutate(res = case_when(h>a ~ "h",
                           a>h ~ "a",
                           h==a ~ "t"))
  return(sim)
  
}

# Sacar la matriz de probabilidades de resultado:
match_matrix <- function(rates){
  goals <- seq(0,6)
  home_probs <- dpois(goals, rates$h_lambda)
  away_probs <- dpois(goals, rates$a_lambda)
  
  rown <- as.character(goals)
  coln <- as.character(goals)
  
  res_matrix = matrix((home_probs) %*% t(away_probs),
                      dimnames = list(rown, coln))
}