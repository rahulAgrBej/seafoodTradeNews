
import os
import pandas as pd
import concurrent.futures
import threading
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer

snowStemmer = SnowballStemmer(language='english')

OUT_FILE_LOCK = threading.Lock()

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

positiveSet = getWordSet(positivePath)
negativeSet = getWordSet(negativePath)

retrievedStopWords = stopwords.words()

# Returns number of positive and negative words in a given sentence
def getSentimentWordCount(inRow, outPath, positiveWords, negativeWords, stopwordsMine):

    # grabs article title
    sentence = str(inRow['title'])
    country = ''
    if inRow['country1'] != 'US':
        country = inRow['country1']
    else:
        country = inRow['country2']

    positiveCount = 0
    negativeCount = 0

    # lower case the whole line
    sentence = sentence.lower()

    # tokenize sentences
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(sentence)

    # remove stop words
    tokensNoSw = [word for word in words if not (word in stopwordsMine)]
    stemmedTokens = [snowStemmer.stem(word) for word in tokensNoSw]

    # count positive and negative words in line
    positiveCount = 0
    negativeCount = 0
    for stemmedWrd in stemmedTokens:
        if stemmedWrd in positiveWords:
            positiveCount += 1
        if stemmedWrd in negativeWords:
            negativeCount += 1

    outRecord = [country, inRow['sourceCountry'], str(inRow['year']), str(inRow['month']), str(inRow['day']), inRow['domain'], str(inRow['title']), inRow['url'], str(positiveCount), str(negativeCount)]
    outLine = ','.join(outRecord) + '\n'
    OUT_FILE_LOCK.acquire()
    f = open(outPath, 'a+')
    f.write(outLine)
    f.close()
    print(f'done with {sentence}\nposCount: {positiveCount}, negCount: {negativeCount}\n========================================')
    OUT_FILE_LOCK.release()

    return [positiveCount, negativeCount]

inFolderPath = 'data/news/processed/original/GDELT_Combined_Files/english/'
inFileNames = os.listdir(inFolderPath)


outFolderPath = 'data/news/processed/original/positiveNegativeWrds/'
#inFileNames = ['testing.csv']
for fileName in inFileNames:
    outFilePath = os.path.join(outFolderPath, fileName)
    outHeader = 'country,sourceCountry,year,month,day,domain,title,url,posCount,negCount\n'
    outF = open(outFilePath, 'a+')
    outF.write(outHeader)
    outF.close()

    fullPath = os.path.join(inFolderPath, fileName)
    df = pd.read_csv(fullPath)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for index, row in df.iterrows():
            #print(row)
            futures.append(executor.submit(getSentimentWordCount, inRow=row, outPath=outFilePath, positiveWords=positiveSet, negativeWords=negativeSet, stopwordsMine=retrievedStopWords))
        
        for future in concurrent.futures.as_completed(futures):
            print(future.result())
    
    print(f'*******************************DONE {fileName}**************************')