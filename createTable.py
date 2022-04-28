import pandas as pd
import numpy as np

# import gc
# gc.collect()
import numpy as np
import pandas as pd

# ['D', 'MemberId', 'JourneyId', 'Event', 'Time_JourneyStarted',
# 'Time_JourneyCompleted','ElementType', 'Duration', 'days',
# 'target', 'Time_JourneyStarted_week', 'Time_JourneyStarted_dayofweek',
# 'Time_JourneyStarted_weekend']

df = pd.read_csv('features2.csv')
sizeDF = len(df.groupby(['D', 'MemberId', 'JourneyId'])['Event'].groups.keys())
df = df.reindex(columns = df.columns.tolist() +
                          ["DaillyActions", "TotalActions" , "mean", "std"] +
                          [x for x in df['Event'].unique()]  +
                          [x for x in df['ElementType'].unique()])
colls = df.columns.tolist()
zero_data = np.zeros(shape=(sizeDF, len(colls)), dtype='int64')
newDF = pd.DataFrame(columns=colls, data=zero_data)

groups = list()
keys = list()
dic = {}
for key, data in df.groupby(['D', 'MemberId', 'JourneyId']):
    # print(key, data)
    groups.append(data)
    keys.append(key)
    dic.update({key:data})

for i in range(len(keys)):
    # print('iiii:', i)
    table = groups[i]
    index = keys[i]
    sElement = table['ElementType'].value_counts()
    sEvent = table['Event'].value_counts()
    actions = sElement.sum() + sEvent.sum()
    D = index[0]
    MemberId = index[1]
    JourneyId = index[2]
    newDF.loc[i, 'D'] = D
    newDF.loc[i, 'DaillyActions'] = actions
    newDF.loc[i, 'ElementType'] = sElement.sum()
    newDF.loc[i, 'Event'] = sEvent.sum()
    newDF.loc[i, 'JourneyId'] = JourneyId
    newDF.loc[i, 'MemberId'] = MemberId
    newDF.loc[i, 'Duration'] = table['Duration'].unique()[0]
    newDF.loc[i, 'Time_JourneyStarted'] = table['Time_JourneyStarted'].unique()[0]
    newDF.loc[i, 'Time_JourneyCompleted'] = table['Time_JourneyCompleted'].unique()[0]
    newDF.loc[i, 'Time_JourneyStarted_dayofweek'] = table['Time_JourneyStarted_dayofweek'].unique()[0]
    newDF.loc[i, 'Time_JourneyStarted_weekend'] = table['Time_JourneyStarted_weekend'].unique()[0]
    newDF.loc[i, 'days'] = table['days'].unique()[0]
    newDF.loc[i, 'target'] = table['target'].unique()[0]
    newDF.loc[i, 'Time_JourneyStarted_week'] = table['Time_JourneyStarted_week'].unique()[0]
    for name in sElement.index.values:
        newDF.loc[i, name] = sElement[name]
    for name in sEvent.index.values:
        newDF.loc[i, name] = sEvent[name]

# gs = newDF.groupby(['D'])['Actions'].describe()
# indx = gs.index.values
# actionMean = gs['mean']
# actionSTD = gs['std']
# s1 = pd.Series()
# s2 = pd.Series()
# for i in range(len(indx)):
#     rep = newDF[newDF['D']==indx[i]]['D'].count()
#     s1 = pd.concat([s1, pd.Series(actionMean[i]).repeat(rep)], ignore_index=True)
#     s2 = pd.concat([s2, pd.Series(actionSTD[i]).repeat(rep)], ignore_index=True)
# newDF['mean'] = s1
# newDF['std'] = s2
newDF = newDF.fillna(0)
newDF.to_csv('table_3.csv')
