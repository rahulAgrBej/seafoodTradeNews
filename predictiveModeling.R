
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

formulaR <- TRADE_SHOCK ~ NEWS_NO_SHIFT + NEWS_BACK_1 + NEWS_BACK_1 + NEWS_BACK_2 + NEWS_FORWARD_1 + NEWS_FORWARD_2 + NEWS_FORWARD_3
fit.allShifts <- glm(formulaR, data=trainSet, family=binomial)
probs.allShifts <- predict(fit.allShifts, newdata=testSet, type="response")
preds.allShifts <- ifelse(probs.allShifts > 0.1, 1, 0)
table(preds.allShifts, testSet$TRADE_SHOCK)
mean(preds.allShifts == testSet$TRADE_SHOCK)

#summaryTest <- table(summary(fit.shift_back_2))
#probs.shift_back_2 <- predict(fit.shift_back_2, newdata=testSet, type="response")


#print(summary(fit.noshift))
#print(summary(fit.shift_back_1))
#print(summary(fit.shift_back_2))
#print(summary(fit.allShifts))
#print(fit.allShifts)