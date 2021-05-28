
library(tidyverse)

sentimentDirPath <- './data/news/processed/original/positiveNegativeWrds/'
sentimentFiles <- list.files(sentimentDirPath)

df <- data.frame(
)

# read in the sentiment files
for (fileIdx in 1:1) {
  fullPath <- paste(sentimentDirPath,sentimentFiles[fileIdx], sep='')
  currDF <- read_csv(fullPath)
  
  # filter out blacklisted sites and remove duplicate rows
  currDF <- currDF %>%
    filter(!str_detect(domain, 'jewishtimes.com')) %>%
    filter(!str_detect(domain, 'thefloridastar.com')) %>%
    distinct()
  df <- rbind(df, currDF)
}

# calculating sentiment scores
# overall sentiment = posCount - negCount
# classify sentiment = +ve only positive words, -VE only negative words, neutral if no sentiment words
df <- df %>%
  mutate(overall_sentiment = posCount - negCount) %>%
  mutate(classify_sentiment = case_when(
    (posCount > 0) & (negCount == 0) ~ 1,
    (posCount == 0) & (negCount > 0) ~ -1,
    (posCount == 0) & (negCount == 0) ~ 0
  ))