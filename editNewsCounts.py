
import pandas as pd
import pprint as pp

def zeroShifts(keylist, data):
    for k in keylist:
        data[k] = [0] * len(data)
    return data

def shiftData(originalKeyList, forwardKeyList, backKeyList, countryData, newsShiftData):
    print(originalKeyList)
    print(forwardKeyList)
    print(backKeyList)
    for originalKey in originalKeyList:
        #print(originalKey)
        it = 0
        for forwardKey in forwardKeyList:
            forwardIt = (it % 3) + 1
            #print(f'{forwardKey} , {forwardIt}')
            forwardInsert = ([0] * forwardIt) + list(countryData[originalKey][:-forwardIt])
            newsShiftData[forwardKey].extend(forwardInsert)
            it += 1

        it = 0
        for backKey in backKeyList:
            backIt = (it % 3) + 1
            #print(f'{backKey} , {backIt}')
            backInsert = list(countryData[originalKey][backIt:]) + ([0] * backIt)
            newsShiftData[backKey].extend(backInsert)
            it += 1
        
        newsShiftData[originalKey].extend(countryData[originalKey])

    return newsShiftData

path = 'data/original/tradeNewsSentiment.csv'
data = pd.read_csv(path)
keylist = [
    'NEWS_FORWARD_1',
    'NEWS_FORWARD_2',
    'NEWS_FORWARD_3',
    'NEWS_BACK_1',
    'NEWS_BACK_2',
    'NEWS_BACK_3',
    'POS_OVERALL_FORWARD_1',
    'POS_OVERALL_FORWARD_2',
    'POS_OVERALL_FORWARD_3',
    'NEG_OVERALL_FORWARD_1',
    'NEG_OVERALL_FORWARD_2',
    'NEG_OVERALL_FORWARD_3',
    'POS_OVERALL_BACK_1',
    'POS_OVERALL_BACK_2',
    'POS_OVERALL_BACK_3',
    'NEG_OVERALL_BACK_1',
    'NEG_OVERALL_BACK_2',
    'NEG_OVERALL_BACK_3',
    'POS_CLASS_FORWARD_1',
    'POS_CLASS_FORWARD_2',
    'POS_CLASS_FORWARD_3',
    'NEG_CLASS_FORWARD_1',
    'NEG_CLASS_FORWARD_2',
    'NEG_CLASS_FORWARD_3',
    'POS_CLASS_BACK_1',
    'POS_CLASS_BACK_2',
    'POS_CLASS_BACK_3',
    'NEG_CLASS_BACK_1',
    'NEG_CLASS_BACK_2',
    'NEG_CLASS_BACK_3'
]

originalKeyList = [
    'NEWS_NO_SHIFT',
    'POS_OVERALL',
    'POS_CLASS',
    'NEG_OVERALL',
    'NEG_CLASS'
]

forwardKeyList = [
    'NEWS_FORWARD_1',
    'NEWS_FORWARD_2',
    'NEWS_FORWARD_3',
    'POS_OVERALL_FORWARD_1',
    'POS_OVERALL_FORWARD_2',
    'POS_OVERALL_FORWARD_3',
    'POS_CLASS_FORWARD_1',
    'POS_CLASS_FORWARD_2',
    'POS_CLASS_FORWARD_3',
    'NEG_OVERALL_FORWARD_1',
    'NEG_OVERALL_FORWARD_2',
    'NEG_OVERALL_FORWARD_3',
    'NEG_CLASS_FORWARD_1',
    'NEG_CLASS_FORWARD_2',
    'NEG_CLASS_FORWARD_3'
]

backKeyList = [
    'NEWS_BACK_1',
    'NEWS_BACK_2',
    'NEWS_BACK_3',
    'POS_OVERALL_BACK_1',
    'POS_OVERALL_BACK_2',
    'POS_OVERALL_BACK_3',
    'POS_CLASS_BACK_1',
    'POS_CLASS_BACK_2',
    'POS_CLASS_BACK_3',
    'NEG_OVERALL_BACK_1',
    'NEG_OVERALL_BACK_2',
    'NEG_OVERALL_BACK_3',
    'NEG_CLASS_BACK_1',
    'NEG_CLASS_BACK_2',
    'NEG_CLASS_BACK_3'
]

data = zeroShifts(keylist, data)
print(data)
print(len(data))

# Get all countries
countries = data['CTY_NAME'].unique()

newsShiftData = {
        'YEAR': [],
        'MONTH': [],
        'NEWS_NO_SHIFT': [],
        'POS_OVERALL': [],
        'POS_CLASS': [],
        'NEG_OVERALL': [],
        'NEG_CLASS': [],
        'CTY_NAME': [],
        'MONTH_IDX': [],
        'TRADE_SHOCK': [],
        'NEWS_FORWARD_1': [],
        'NEWS_FORWARD_2': [],
        'NEWS_FORWARD_3': [],
        'NEWS_BACK_1': [],
        'NEWS_BACK_2': [],
        'NEWS_BACK_3': [],
        'POS_OVERALL_FORWARD_1': [],
        'POS_OVERALL_FORWARD_2': [],
        'POS_OVERALL_FORWARD_3': [],
        'NEG_OVERALL_FORWARD_1': [],
        'NEG_OVERALL_FORWARD_2': [],
        'NEG_OVERALL_FORWARD_3': [],
        'POS_OVERALL_BACK_1': [],
        'POS_OVERALL_BACK_2': [],
        'POS_OVERALL_BACK_3': [],
        'NEG_OVERALL_BACK_1': [],
        'NEG_OVERALL_BACK_2': [],
        'NEG_OVERALL_BACK_3': [],
        'POS_CLASS_FORWARD_1': [],
        'POS_CLASS_FORWARD_2': [],
        'POS_CLASS_FORWARD_3': [],
        'NEG_CLASS_FORWARD_1': [],
        'NEG_CLASS_FORWARD_2': [],
        'NEG_CLASS_FORWARD_3': [],
        'POS_CLASS_BACK_1': [],
        'POS_CLASS_BACK_2': [],
        'POS_CLASS_BACK_3': [],
        'NEG_CLASS_BACK_1': [],
        'NEG_CLASS_BACK_2': [],
        'NEG_CLASS_BACK_3': []
    }


for country in countries[:1]:
    countryIdx = (data['CTY_NAME'] == country)
    countryData = data[countryIdx]
    itStart = 0
    for originalKey in originalKeyList:
        newsShiftData = shiftData([originalKey], forwardKeyList[itStart:itStart+3], backKeyList[itStart:itStart+3], countryData, newsShiftData)
        itStart += 3
    

    newsShiftData['CTY_NAME'].extend(countryData['CTY_NAME'])
    newsShiftData['YEAR'].extend(countryData['YEAR'])
    newsShiftData['MONTH'].extend(countryData['MONTH'])
    newsShiftData['MONTH_IDX'].extend(countryData['MONTH_IDX'])
    newsShiftData['TRADE_SHOCK'].extend(countryData['TRADE_SHOCK'])

print('HERE')
print(len(newsShiftData['CTY_NAME']))
#print(newsShiftData.keys())
print('asdkfjaskldfjlkasdjfkla')
for k in newsShiftData.keys():
    print(f'{k} : {len(newsShiftData[k])}')

#print(newsShiftData)
newDataWithShifts = pd.DataFrame(data=newsShiftData)


dataWithShiftsPath = 'data/original/tradeNewsShiftsSentiment.csv'
newDataWithShifts.to_csv(dataWithShiftsPath, index=False)