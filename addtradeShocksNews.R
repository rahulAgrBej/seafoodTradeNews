
library(tidyverse)

newsCountsPath <- 'data/news/processed/original/newsCounts.csv'
newsCounts <- read_csv(newsCountsPath)

exportShocksPath <- 'data/trade/processed/original/exportShocks.csv'
importShocksPath <- 'data/trade/processed/original/importShocks.csv'

exportShocks <- read_csv(exportShocksPath)
importShocks <- read_csv(importShocksPath)

exportShockCol <- exportShocks %>%
  select(shock.event)

importShockCol <- importShocks %>%
  select(shock.event)

# adds all export and import shocks together
allTradeShocks <- exportShockCol + importShockCol
allTradeShocks <- allTradeShocks %>%
  mutate(shock.event = case_when(shock.event > 1 ~ 1,
                                 TRUE ~ shock.event)) %>%
  rename(TRADE_SHOCK = shock.event)

tradeNews <- newsCounts %>%
  cbind(allTradeShocks) %>%
  rename(NEWS_NO_SHIFT = TOTAL)

write_csv(allTradeShocks, 'data/original/tradeNews.csv')

