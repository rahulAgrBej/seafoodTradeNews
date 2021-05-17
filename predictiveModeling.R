
library(tidyverse)
library(ISLR)
library(caret)

dataPath = 'data/original/tradeNews.csv'
df <- read_csv(dataPath)

indexTrainTest <- caret::createDataPartition(df$TRADE_SHOCK, p=0.8, times=1, list=FALSE)
trainSet <- df[indexTrainTest,]
testSet <- df[-indexTrainTest,]

fit <- glm(TRADE_SHOCK ~ NEWS_NO_SHIFT, data=trainSet, family=binomial)
testing <- predict(fit, newdata=testSet, type = "response")
testing > 0.1
#summary(fit)
summary(testing)