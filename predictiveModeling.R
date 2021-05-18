
library(tidyverse)
library(ISLR)
library(caret)

dataPath = 'data/original/tradeNewsShifts.csv'
df <- read_csv(dataPath)

indexTrainTest <- caret::createDataPartition(df$TRADE_SHOCK, p=0.8, times=1, list=FALSE)
trainSet <- df[indexTrainTest,]
testSet <- df[-indexTrainTest,]

fit.noshift <- glm(TRADE_SHOCK ~ NEWS_NO_SHIFT, data=trainSet, family=binomial)
fit.shift_back_1 <- glm(TRADE_SHOCK ~ NEWS_BACK_1, data=trainSet, family=binomial)
fit.shift_back_2 <- glm(TRADE_SHOCK ~ NEWS_BACK_2, data=trainSet, family=binomial)
fit.shift_back_3 <- glm(TRADE_SHOCK ~ NEWS_BACK_3, data=trainSet, family=binomial)
fit.shift_forward_1 <- glm(TRADE_SHOCK ~ NEWS_FORWARD_1, data=trainSet, family=binomial)
fit.shift_forward_2 <- glm(TRADE_SHOCK ~ NEWS_FORWARD_2, data=trainSet, family=binomial)
fit.shift_forward_3 <- glm(TRADE_SHOCK ~ NEWS_FORWARD_3, data=trainSet, family=binomial)

print(summary(fit.noshift))