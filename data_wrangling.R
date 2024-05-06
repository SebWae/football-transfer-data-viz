library(tidyverse)
options(scipen=999)

path <- "/Users/krusand/Documents/GitHub/football-data-viz/"

leagues <- c("Premier League", "Serie A", "LaLiga", "Bundesliga", "Ligue 1")

transfers <- read.csv(paste0(path, "data/all_transfers.csv"))

transfers %>% View()

transfer_paths <- read.csv(paste0(path,"data/transfer_paths.csv")) %>% 
  mutate(Season = paste0(substr(Year, 3,4),"/", as.numeric(substr(Year, 3,4))+1))
  

league_transfers <- transfers %>% 
  filter(From_League != To_League) %>% 
  filter(grepl("^Premier League|^Bundesliga|^Ligue 1|^LaLiga|^Serie A", From_League)) %>% 
  filter(grepl("^Premier League|^Bundesliga|^Ligue 1|^LaLiga|^Serie A", To_League)) %>% 
  group_by(Season, From_League, To_League) %>% 
  summarise(Fee_total = sum(Fee))



transfer_paths_with_fee <- transfer_paths %>% 
  left_join(league_transfers, by=c("Season", "From_League", "To_League")) %>% 
  replace(is.na(.), 0) %>%
  mutate(From_To = paste0(From_League, To_League)) %>% 
  mutate(country = case_when(
    grepl("^Premier League", From_League) ~ "United Kingdom",
    grepl("^Serie A", From_League) ~ "Italy",
    grepl("^Bundesliga", From_League) ~ "Germany",
    grepl("^Ligue 1", From_League) ~ "France",
    grepl("^LaLiga", From_League) ~ "Spain"
    
  ))

transfer_paths_with_fee

transfer_paths_with_fee %>% 
  write.csv(paste0(path, "data/transfer_paths_with_fee.csv"), row.names = F)




  

