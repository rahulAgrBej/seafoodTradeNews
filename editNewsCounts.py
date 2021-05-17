
import pandas as pd
import pprint as pp

path = 'data/original/tradeNews.csv'
data = pd.read_csv(path)
data['NEWS_FORWARD_1'] = [0] * len(data)
data['NEWS_FORWARD_2'] = [0] * len(data)
data['NEWS_FORWARD_3'] = [0] * len(data)
data['NEWS_BACK_1'] = [0] * len(data)
data['NEWS_BACK_2'] = [0] * len(data)
data['NEWS_BACK_3'] = [0] * len(data)
print(data)
print(len(data))

# Get all countries
countries = data['CTY_NAME'].unique()

newsShiftData = {
        'YEAR': [],
        'MONTH': [],
        'NEWS_NO_SHIFT': [],
        'CTY_NAME': [],
        'MONTH_IDX': [],
        'TRADE_SHOCK': [],
        'NEWS_FORWARD_1': [],
        'NEWS_FORWARD_2': [],
        'NEWS_FORWARD_3': [],
        'NEWS_BACK_1': [],
        'NEWS_BACK_2': [],
        'NEWS_BACK_3': []
    }


for country in countries:
    countryIdx = (data['CTY_NAME'] == country)
    countryData = data[countryIdx]
    newsForward1 = ([0] * 1) + list(countryData['NEWS_NO_SHIFT'][:-1])
    newsForward2 = ([0] * 2) + list(countryData['NEWS_NO_SHIFT'][:-2])
    newsForward3 = ([0] * 3) + list(countryData['NEWS_NO_SHIFT'][:-3])
    newsBack1 = list(countryData['NEWS_NO_SHIFT'][1:]) + ([0] * 1)
    newsBack2 = list(countryData['NEWS_NO_SHIFT'][2:]) + ([0] * 2)
    newsBack3 = list(countryData['NEWS_NO_SHIFT'][3:]) + ([0] * 3)
    
    newsShiftData['YEAR'].extend(countryData['YEAR'])
    newsShiftData['MONTH'].extend(countryData['MONTH'])
    newsShiftData['NEWS_NO_SHIFT'].extend(countryData['NEWS_NO_SHIFT'])
    newsShiftData['CTY_NAME'].extend(countryData['CTY_NAME'])
    newsShiftData['MONTH_IDX'].extend(countryData['MONTH_IDX'])
    newsShiftData['TRADE_SHOCK'].extend(countryData['TRADE_SHOCK'])
    newsShiftData['NEWS_FORWARD_1'].extend(newsForward1)
    newsShiftData['NEWS_FORWARD_2'].extend(newsForward2)
    newsShiftData['NEWS_FORWARD_3'].extend(newsForward3)
    newsShiftData['NEWS_BACK_1'].extend(newsBack1)
    newsShiftData['NEWS_BACK_2'].extend(newsBack2)
    newsShiftData['NEWS_BACK_3'].extend(newsBack3)

print('HERE')
print(len(newsShiftData['CTY_NAME']))
print(newsShiftData.keys())
newDataWithShifts = pd.DataFrame(data=newsShiftData)

dataWithShiftsPath = 'data/original/tradeNewsShifts.csv'
newDataWithShifts.to_csv(dataWithShiftsPath, index=False)