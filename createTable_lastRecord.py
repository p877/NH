# 387.2997028827667 s for oneRecord_5_new.csv
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

filepath = '../Shayan'
lenTable = 5

try:
    df = pd.read_csv(os.path.join(filepath,'table-D_MemberId_JourneyId.csv'))
except:
    df = pd.read_csv(os.path.join(filepath,'table-D_MemberId_JourneyId.csv'),  compression='zip')

if os.path.isfile(os.path.join(filepath,'oneRecord_{}_new.csv'.format(lenTable))):
   os.remove(os.path.join(filepath,'oneRecord_{}_new.csv'.format(lenTable)))
with open(os.path.join(filepath,'oneRecord_{}_new.csv'.format(lenTable)), "w") as my_empty_csv: pass #create an empty .csv file

newDF2 = pd.DataFrame(data = list(), columns=df.columns)

chunksize = 200000
k = 0
firstTime = time.time()
for key, table in df.groupby(['MemberId', 'JourneyId']):
    table.index = range(len(table))
    firstDate = datetime.datetime.strptime(table.loc[0, 'D'], '%Y-%m-%d')
    firstRow = table[table['D'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d')-firstDate > datetime.timedelta(days=lenTable))].head(1)
    secondDate = 0
    delta = 0
    if firstRow.__len__() == 0:
        subTable = table
        secondDate = datetime.datetime.strptime(table.loc[len(table)-1, 'D'], '%Y-%m-%d')
        delta = (secondDate - firstDate).days + 1
    else:
        indexFirst = firstRow.index.values[0]
        subTable = table.loc[0:indexFirst - 1]
        secondDate = datetime.datetime.strptime(table.loc[indexFirst-1, 'D'], '%Y-%m-%d')
        delta = lenTable

    actionsKeep = pd.Series(np.zeros(shape=delta), dtype='int')
    for i in range(len(subTable)):
        tempDate = datetime.datetime.strptime(subTable.loc[i, 'D'], '%Y-%m-%d')
        index = (tempDate-firstDate).days
        actionsKeep[index] = subTable.loc[i, 'DaillyActions']

    span = 0
    daily = 0
    daily = 0 if (len(firstRow) != 0) else subTable.loc[len(subTable)-1, 'DaillyActions']
    span = 0 if(len(firstRow) == 0) else lenTable - (secondDate-firstDate).days + 1
    newDF2 = newDF2.append(subTable.loc[0], ignore_index=True)  # insert the last row of table to newDf2
    newDF2.loc[len(newDF2) - 1, 'JourneyStarted':] = subTable.loc[0:len(subTable)-1,'JourneyStarted':].sum()  # change Event and ElementType for this new record to total Event and total ElementType
    newDF2.loc[len(newDF2) - 1, 'Event'] = subTable.loc[0:len(subTable)-1, 'Event'].sum()
    newDF2.loc[len(newDF2) - 1, 'ElementType'] = subTable.loc[0:len(subTable)-1, 'ElementType'].sum()
    newDF2.loc[len(newDF2) - 1, 'D'] = ((secondDate + datetime.timedelta(days=span)).__str__().split(' '))[0]
    newDF2.loc[len(newDF2) - 1, 'TotalNumberOfActions'] = subTable.loc[0:len(subTable)-1, 'DaillyActions'].sum()
    newDF2.loc[len(newDF2) - 1, 'DaillyActions'] = daily
    newDF2.loc[len(newDF2) - 1, 'AvgNumberOfActions'] = actionsKeep.mean()
    newDF2.loc[len(newDF2) - 1, 'StdDevNumberOfActions'] = actionsKeep.std()
    print()
newDF2 = newDF2.fillna(0)
newDF2[newDF2.columns].to_csv(os.path.join(filepath, 'oneRecord_{}_new.csv'.format(lenTable)), mode='a', index=False,header=(os.path.getsize(os.path.join(filepath, 'oneRecord_{}_new.csv'.format(lenTable))) == 0))
lasttime = time.time()
print(lasttime-firstTime)

