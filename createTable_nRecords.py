# 1:  1527.8373394012451
# 2: 0.029996156692504883

# 1291.8778989315033

# import gc
# gc.collect()
import numpy as np
import pandas as pd
import datetime
import time
import os
import warnings
warnings.filterwarnings('ignore')

# ['D', 'MemberId', 'JourneyId', 'Event', 'Time_JourneyStarted',
# 'Time_JourneyCompleted','ElementType', 'Duration', 'days',
# 'target', 'Time_JourneyStarted_week', 'Time_JourneyStarted_dayofweek',
# 'Time_JourneyStarted_weekend']

filepath = './'
lenTable = 5

try:
    df = pd.read_csv(os.path.join(filepath,'table-D_MemberId_JourneyId.csv'))
except:
    df = pd.read_csv(os.path.join(filepath,'table-D_MemberId_JourneyId.csv'),  compression='zip')

if os.path.isfile(os.path.join(filepath,'finalTable.h5')):
   os.remove(os.path.join(filepath,'finalTable.h5'))
with open(os.path.join(filepath,'finalTable.h5'), "w") as my_empty_csv: pass #create an empty .csv file

newDF = pd.DataFrame(data = list(), columns=df.columns)
chunksize = df.__len__()/2

firstTime = time.time()
for key, table in df.groupby(['MemberId', 'JourneyId']):
    # table.index = range(len(table))
    first_date = 0
    leeen = len(table)
    i = 0
    while (i in range(len(table))) & (i < lenTable):
        table.index = range(len(table))
        nxtD = table.loc[i, 'D']
        second_date = datetime.datetime.strptime(nxtD, '%Y-%m-%d')
        if i != 0:
            table.loc[i, 'TotalNumberOfActions'] = table.loc[i, 'DaillyActions'] + table.loc[i-1, 'TotalNumberOfActions']
            f = int(((second_date-first_date).__str__().split(','))[0].split(' ')[0]) - 1
            line = pd.Series(np.zeros(shape=(len(table.columns))), dtype='int64')
        else:
            f = 0
            table.loc[i, 'TotalNumberOfActions'] = table.loc[i, 'DaillyActions']

        for j in range(f):
            table.loc[float((i - 1) + 0.00000001 * (j + 1))] = line
            table.loc[float((i - 1) + 0.00000001 * (j + 1)), :'TotalNumberOfActions'] = table.loc[i - 1, :'TotalNumberOfActions']
            table.loc[float((i - 1) + 0.00000001 * (j + 1)), 'DaillyActions'] = 0
            table.loc[float((i - 1) + 0.00000001 * (j + 1)), 'Event'] = 0
            table.loc[float((i - 1) + 0.00000001 * (j + 1)), 'ElementType'] = 0
            table.loc[float((i - 1) + 0.00000001 * (j + 1)), 'D'] = \
            ((first_date + datetime.timedelta(days=j + 1)).__str__().split(' '))[0]
        table = table.sort_index().reset_index(drop=True)
        i = (i + f) + 1
        first_date = second_date

    for j in range(table.head(lenTable).shape[0]): #calculate mean and std for each uniqe memberId and journeyId in each day
        table.loc[j, 'AvgNumberOfActions'] = table.loc[:j, 'DaillyActions'].mean()
        table.loc[j, 'StdDevNumberOfActions'] = table.loc[:j, 'DaillyActions'].std()

    if newDF.__len__() < chunksize:
        newDF = newDF.append(table.head(lenTable))
    else:
        newDF[newDF.columns].to_csv(os.path.join(filepath, 'finalTable.csv'), mode='a', index=False,header=(os.path.getsize(os.path.join(filepath, 'finalTable.csv')) == 0))
        newDF = pd.DataFrame(data=list(), columns=df.columns)

if newDF.empty != True:
    newDF[newDF.columns].to_csv(os.path.join(filepath, 'finalTable.csv'), mode='a', index=False, header=(os.path.getsize(os.path.join(filepath, 'finalTable.csv')) == 0))

lasttime = time.time()
print(lasttime-firstTime)

