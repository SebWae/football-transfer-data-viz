library(tidyverse)
# Data from: https://www.kaggle.com/datasets/davidcariboo/player-scores?select=player_valuations.csv
# https://github.com/ewenme/transfers/tree/master


path <- "/Users/krusand/Documents/GitHub/football-data-viz/"

player_valuations <- read.csv(paste0(path,"data/kaggle/player_valuations.csv"))
appearances <- read.csv(paste0(path,"data/kaggle/appearances.csv"))
club_games <- read.csv(paste0(path,"data/kaggle/club_games.csv"))
clubs <- read.csv(paste0(path,"data/kaggle/clubs.csv"))
competitions <- read.csv(paste0(path,"data/kaggle/competitions.csv"))
game_events <- read.csv(paste0(path,"data/kaggle/game_events.csv"))
game_lineups <- read.csv(paste0(path,"data/kaggle/game_lineups.csv"))
players <- read.csv(paste0(path,"data/kaggle/players.csv"))
games <- read.csv(paste0(path,"data/kaggle/games.csv"))



player_valuations %>% 
  left_join(players, by = 'player_id') %>% 
  group_by(date) %>% 
  summarise(gns = mean(market_value_in_eur.y)) %>% 
  ungroup() %>% 
  arrange(date)




bundesliga <- read.csv(paste0(path,"data/kaggle/transfers/bundesliga.csv"))
la_liga <- read.csv(paste0(path,"data/kaggle/transfers/laliga.csv"))
premier_league <- read.csv(paste0(path,"data/kaggle/transfers/premier-league.csv"))
ligue_1 <- read.csv(paste0(path,"data/kaggle/transfers/ligue1.csv"))
serie_a <- read.csv(paste0(path,"data/kaggle/transfers/serie-a.csv"))


transfer_data <- rbind(bundesliga, la_liga, premier_league, ligue_1, serie_a) %>% 
  filter(!is.na(fee_cleaned)) %>% 
  group_by(league_name, year,transfer_movement) %>% 
  summarise(fee_total = sum(fee_cleaned)) %>% 
  ungroup()



transfer_data %>% 
  pivot_wider(names_from = 'transfer_movement', values_from = 'fee_total') %>% 
  mutate(net_fee = )


ggplot(data = transfer_data, aes(x=year, y = fee_total, col=transfer_movement)) + 
  geom_point()




rbind(
games %>% 
  filter(competition_type == 'domestic_league') %>% 
  select(season, club_id = home_club_id, competition_id)  
,
games %>% 
  filter(competition_type == 'domestic_league') %>% 
  select(season, club_id = away_club_id, competition_id) 
) %>% 
  distinct(season, club_id, competition_id)




clubs %>% View()







