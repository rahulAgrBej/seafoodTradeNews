
import os
import pandas as pd

folderPath = 'data/news/raw/original/GDELT_results_unaltered'
fileNames = os.listdir(folderPath)


outLines = ''

for fileName in fileNames:
    fullPath = os.path.join(folderPath, fileName)
    print(fileName)
    if fileName[-4:] != '.csv':
        print(f'here {fileName} {fileName[-3:]}')
        continue
    f = open(fullPath, 'r')
    lines = f.readlines()
    header = lines[0]

    lines = lines[1:]
    for line in lines:
        line = line.rstrip('\n')
        cells = line.split(',')

        if ((cells[0] == 'US') or (cells[1] == 'US')):
            if len(cells) == 12:
                line = line + '\n'
            else:
                line = ','.join(cells[:8]) + ',MALFORMED.com,' + ','.join(cells[-3:]) + '\n'
            
            outLines = outLines + line
        #print(line)
    
    outFolderPath = 'data/news/processed/original/GDELT_results_cleaned'
    outFileName = fileName
    outFilePath = os.path.join(outFolderPath, outFileName)
    outF = open(outFilePath, 'w')
    outF.write(header)
    outF.write(outLines)
    outF.close()