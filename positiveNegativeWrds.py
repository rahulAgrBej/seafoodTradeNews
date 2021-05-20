
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer

snowStemmer = SnowballStemmer(language='english')

# Returns number of positive and negative words in a given sentence
def getSentimentWordCount(sentence, positiveWords, negativeWords):

    positiveCount = 0
    negativeCount = 0

    # lower case the whole line
    sentence = sentence.lower()

    # tokenize sentences
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(sentence)

    # remove stop words
    tokensNoSw = [word for word in words if not word in stopwords.words()]
    stemmedTokens = [snowStemmer.stem(word) for word in tokensNoSw]

    # count positive and negative words in line
    positiveCount = 0
    negativeCount = 0
    for stemmedWrd in stemmedTokens:
        if stemmedWrd in positiveWords:
            positiveCount += 1
        if stemmedWrd in negativeWords:
            negativeCount += 1

    return positiveCount, negativeCount

def countSentimentWords(df, positiveWords, negativeWords):

    df = df.sort_index()
    sentimentCounts = {
        'posCounts': [],
        'negCounts': []
    }

    # get the article titles
    for index, row in df.iterrows():
        articleTitle = row['title']
        articleTitle = str(articleTitle)
        posCount, negCount = getSentimentWordCount(articleTitle, positiveWords, negativeWords)
        sentimentCounts['posCounts'].append(posCount)
        sentimentCounts['negCounts'].append(negCount)

        print(f'Article Title: {articleTitle}')
        print(f'Positive Count: {posCount}, Negative Count: {negCount}')
        print('====================================================================')
    
    return sentimentCounts

def getWordSet(path):

    f = open(path, 'r')
    words = f.readlines()
    f.close()

    wordList = [snowStemmer.stem(word.rstrip('\n')) for word in words]
    wordSet = set(wordList)
    return wordSet

wordFolderPath = 'data/original/opinion-lexicon-English/'
positiveName = 'positive-words.txt'
negativeName = 'negative-words.txt'

positivePath = os.path.join(wordFolderPath, positiveName)
negativePath = os.path.join(wordFolderPath, negativeName)

positiveWords = getWordSet(positivePath)
negativeWords = getWordSet(negativePath)

newsDataFolder = 'data/news/processed/original/GDELT_Combined_Files/'
newsFiles = os.listdir(newsDataFolder)


outFolder = 'data/news/processed/original/positiveNegativeWrds/'

for newsFileName in newsFiles:
    fullPath = os.path.join(newsDataFolder, newsFileName)
    print(f'Starting {newsFileName}')
    newsDF = pd.read_csv(fullPath)

    # filter down to only include articles written in English
    englishNewsDF = (newsDF['language'] == 'English')
    df = newsDF[englishNewsDF]

    print(f'number of english articles {len(df.index)}')
    sentimentCounts = countSentimentWords(df, positiveWords, negativeWords)
    df = sort_index()
    sentimentFreq = pd.DataFrame(sentimentCounts)
    df['Positive_Words'] = sentimentFreq['posCounts']
    df['Negative_Words'] = sentimentFreq['negCounts']

    outPath = os.path.join(outFolder, newsFileName)
    df.to_csv(outPath)
    print(f'DONE WITH {newsFileName}')
    print('======================================================')