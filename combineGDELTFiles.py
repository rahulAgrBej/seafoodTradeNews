
import os

folderPath = 'data/news/processed/original/GDELT_results_cleaned/'
fileNames = os.listdir(folderPath)

years = [2017, 2018, 2019, 2020]
fileNamesbyYear = []

for year in years:
    currFileNames = [fileName for fileName in fileNames if (fileName[:4] != '.DS_') and (int(fileName[:4]) == year)]
    fileNamesbyYear.append(currFileNames)

header = 'country1,country2,sourceCountry,year,month,day,domain,title,url,social_image,language,query\n'

year = 2017
for fileNames in fileNamesbyYear:
    print(f'starting files for {str(year)}')
    outLines = header

    for fileName in fileNames:
        print(fileName)
        fullPath = os.path.join(folderPath, fileName)
        f = open(fullPath, 'r')
        lines = f.readlines()
        f.close()

        lines = lines[1:]
        for line in lines:
            outLines = outLines + line
    
    outPath = f'data/news/processed/original/GDELT_FullResults_{str(year)}.csv'
    outF = open(outPath, 'w')
    outF.write(outLines)
    outF.close()
    year += 1
