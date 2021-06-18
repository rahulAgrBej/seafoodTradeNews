library(tidyverse)
library(ggplot2)

newsPath <- 'data/news/processed/original/GeneralNewsShocks.csv'
newsData <- read_csv(newsPath) %>%
  mutate(shock.event = replace_na(shock.event, 0))

importsPath <- 'data/trade/processed/original/level_hs_10/imports.csv'
exportsPath <- 'data/trade/processed/original/level_hs_10/exports.csv'

importsData <- read_csv(importsPath)
exportsData <- read_csv(exportsPath )

# cleaning out country names - eliminating parentheses in datasets
newsData$CTY_NAME <- gsub('\\(', '', newsData$CTY_NAME)
newsData$CTY_NAME <- gsub('\\)', '', newsData$CTY_NAME)
importsData$CTY_NAME <- gsub('\\(', '', importsData$CTY_NAME)
importsData$CTY_NAME <- gsub('\\)', '', importsData$CTY_NAME)
exportsData$CTY_NAME <- gsub('\\(', '', importsData$CTY_NAME)
exportsData$CTY_NAME <- gsub('\\)', '', importsData$CTY_NAME)

# aggregating imports + exports = trade
tradeData <- importsData
tradeData$TOTAL <- tradeData$TOTAL + exportsData$TOTAL

# list of countries that do not trade in seafood with the US
tradingCountryData  <- tradeData %>%
  group_by(CTY_NAME) %>%
  summarize(TOTAL_TRADE = sum(TOTAL)) %>%
  filter(TOTAL_TRADE > 0)

tradeData <- tradeData %>%
  filter(CTY_NAME %in% unique(tradingCountryData$CTY_NAME))

avgTrades <- tradeData %>%
  group_by(CTY_NAME) %>%
  summarize(AVG_TRADE = sum(TOTAL) / 4) %>%
  ungroup()# %>%
  #group_by(CTY_NAME) %>%
  #summarize(AVG_TRADE = TOTAL_TRADE / n())

# Histogram to determine a cut off of high trade vs low trade partners
histo <- ggplot(avgTrades, aes(AVG_TRADE)) + 
  geom_histogram(binwidth=500000)

avgNewsShocks <- newsData %>%
  group_by(CTY_NAME) %>%
  summarize(AVG_NEWS_SHOCKS = (sum(shock.event) / 4), AVG_NEWS = (sum(TOTAL) / 4)) %>%
  ungroup()
#plot(histo)

newsTradeData <- avgNewsShocks %>%
  right_join(avgTrades)

p <- ggplot(newsTradeData, aes(x=AVG_TRADE, y=AVG_NEWS_SHOCKS)) +
  geom_point()

plot(p)

p1 <- ggplot(newsTradeData, aes(x=AVG_TRADE, y=AVG_NEWS)) +
  geom_point()

plot(p1)

bigTradeNews <- newsTradeData %>%
  filter(AVG_TRADE > 500000)

avgBigTradeNewsShocks <- sum(bigTradeNews$AVG_NEWS_SHOCKS) / nrow(bigTradeNews)

smallTradeNews <- newsTradeData %>%
  filter(AVG_TRADE < 500000)

avgSmallTradeNewsShocks <- sum(smallTradeNews$AVG_NEWS_SHOCKS) / nrow(smallTradeNews)

p3 <- ggplot(bigTradeNews, aes(x=AVG_TRADE, y=AVG_NEWS_SHOCKS)) + geom_point() +
  labs(title='Big Trade Partners')
p4 <- ggplot(bigTradeNews, aes(x=AVG_TRADE, y=AVG_NEWS)) + geom_point() +
  labs(title='Big Trade Partners')

p5 <- ggplot(smallTradeNews, aes(x=AVG_TRADE, y=AVG_NEWS_SHOCKS)) + geom_point() +
  labs(title='Small Trade Partners')
p6 <- ggplot(smallTradeNews, aes(x=AVG_TRADE, y=AVG_NEWS)) + geom_point() +
  labs(title='Small Trade Partners')

plot(p3)
plot(p4)
plot(p5)
plot(p6)