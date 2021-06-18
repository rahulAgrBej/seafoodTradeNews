library(tidyverse)

# Shock Detection Function
shock.id <- function(dat, thresh=0.25){
  # dat is your time series data and threshold is the threshold you want for Cook's D (defaulted to 0.35)
  outt <- array(dim=c(length(dat), 3))
  x <- 1:length(dat)
  ll <- lowess(x, dat, f=(2/3)) # Fits lowess curve (can specify other options for how the curve is estimated and can change the span)
  rr <- as.numeric(dat[order(x)]-ll$y) #residuals off lowess
  rrp1 <- rr[2:length(rr)] # Residuals at time t
  rrm1 <- rr[1:(length(rr)-1)] # Residuals at time t-1
  ll2 <- lm(rrp1~rrm1) # Linear fit of the residuals
  cd <- cooks.distance(ll2) # Calculate the Cook's D
  outt[2:length(rr),1] <- as.numeric(cd) # Output the Cook's D
  outt[,2] <- rr # Output the residuals
  outt[2:length(rr),3] <- ifelse(as.numeric(cd) >= thresh,1,0) # Logical of whether point is a shock
  outt <- as.data.frame(outt)
  colnames(outt) <- c("cooks.d", "residual", "shock.event")
  return(outt)
}

dirPath <- 'data/news/processed/original/GDELT_General_cleaned_no_query'
fileNames <- list.files(dirPath)

df <- data.frame()

for (fName in fileNames) {
  fullPath <- paste(dirPath, '/', fName, sep='')
  currDF <- read_csv(fullPath)
  currDF <- currDF %>%
    filter(!str_detect(domain, 'jewishtimes.com')) %>%
    filter(!str_detect(domain, 'thefloridastar.com')) %>%
    distinct() %>%
    select(-c(country1)) %>%
    rename(CTY_NAME=country2)
  
  df <- rbind(df, currDF)
}

countryCodeNameLookupPath <- 'data/relevantCountries.csv'
countryCodeNameLookup <- read_csv(countryCodeNameLookupPath) %>%
  rename(CTY_NAME=name)

countryFillerPath <- 'data/countryFiller.csv'
countryFiller <- read_csv(countryFillerPath)


newsCounts <- df %>%
  rename(YEAR=year,MONTH=month) %>%
  group_by(CTY_NAME, YEAR, MONTH) %>%
  summarize(TOTAL = n()) %>%
  ungroup() %>%
  rename(code=CTY_NAME) %>%
  left_join(countryCodeNameLookup) %>%
  select(-c(code)) %>%
  right_join(countryFiller) %>%
  mutate(TOTAL = replace_na(TOTAL, 0)) %>%
  arrange(CTY_NAME, YEAR, MONTH)

write_csv(newsCounts, 'data/news/processed/original/GeneralNewsCounts.csv')

newsCounts$CTY_NAME <- gsub('\\(', '', newsCounts$CTY_NAME) # eliminate all (
newsCounts$CTY_NAME <- gsub('\\)', '', newsCounts$CTY_NAME) # eliminate all )

countryCodeNameLookup$CTY_NAME <- gsub('\\(', '', countryCodeNameLookup$CTY_NAME)
countryCodeNameLookup$CTY_NAME <- gsub('\\)', '', countryCodeNameLookup$CTY_NAME)


newsShocks <- data.frame(
  CTY_NAME=character(),
  cooks.d=numeric(),
  residual=numeric(),
  shock.event=numeric(),
  TOTAL=numeric(),
  YEAR=numeric(),
  MONTH=numeric()
)

countryNames <- unique(newsCounts$CTY_NAME)

for (country in countryNames) {
  
  countryNews <- newsCounts %>%
    filter(str_detect(CTY_NAME, country)) %>%
    filter(str_length(CTY_NAME) == str_length(country))
  
  countryNewsShocks <- shock.id(countryNews$TOTAL)
  countryNewsShocks <- countryNewsShocks %>%
    cbind(countryNews)
  
  newsShocks <- newsShocks %>%
    rbind(countryNewsShocks)
}

outShockPath <- 'data/news/processed/original/GeneralNewsShocks.csv'
write_csv(newsShocks, outShockPath)
