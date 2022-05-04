import warnings
warnings.filterwarnings('ignore')

# import gc
# gc.collect()
import numpy as np
import pandas as pd
import os
# ['D', 'MemberId', 'JourneyId', 'Event', 'Time_JourneyStarted',
# 'Time_JourneyCompleted','ElementType', 'Duration', 'days',
# 'target', 'Time_JourneyStarted_week', 'Time_JourneyStarted_dayofweek',
# 'Time_JourneyStarted_weekend']

filepath = './'
df = pd.read_csv(os.path.join(filepath,'featureprocess.csv'))

colls = df.columns.tolist() + ["DaillyActions", "TotalActions" , "mean", "std"] +[x for x in df['Event'].unique()]  +[x for x in df['ElementType'].unique()] # df['Event'].unique().tolist()
newDF = pd.DataFrame(columns=colls, data=list())

if os.path.isfile(os.path.join(filepath,'table-D_MemberId_JourneyId.csv')):
   os.remove(os.path.join(filepath,'table-D_MemberId_JourneyId.csv'))
with open(os.path.join(filepath,'table-D_MemberId_JourneyId.csv'), "w") as my_empty_csv: pass #create an empty .csv file


inx = 0
for index, table in df.groupby(['D', 'MemberId', 'JourneyId']):
    table.index = range(len(table)) # update indexes
    sElement = table['ElementType'].value_counts()
    sEvent = table['Event'].value_counts()
    actions = sElement.sum() + sEvent.sum()
    newDF = newDF.append(table.loc[0], ignore_index=True) # add a new line like previous table to newDF
    newDF.loc[inx, 'DaillyActions'] = actions
    newDF.loc[inx, 'ElementType'] = sElement.sum()
    newDF.loc[inx, 'Event'] = sEvent.sum()
    newDF.loc[inx, sElement.index.values] = sElement[sElement.index.values]
    newDF.loc[inx, sEvent.index.values] = sEvent[sEvent.index.values]
    inx = inx + 1

newDF = newDF.fillna(0)
newDF[colls].to_csv(os.path.join(filepath,'table-D_MemberId_JourneyId.csv'))
# newDF.to_csv('test.csv', chunksize=200000, compression='zip')

