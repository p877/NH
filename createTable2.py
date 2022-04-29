import pandas as pd
import numpy as np

# import gc
# gc.collect()
import numpy as np
import pandas as pd
import datetime
import csv
import os

# ['D', 'MemberId', 'JourneyId', 'Event', 'Time_JourneyStarted',
# 'Time_JourneyCompleted','ElementType', 'Duration', 'days',
# 'target', 'Time_JourneyStarted_week', 'Time_JourneyStarted_dayofweek',
# 'Time_JourneyStarted_weekend']

filepath = 'finalTable.csv'
df = pd.read_csv('table_3.csv')
lenTable = 5
with open(filepath, "w") as my_empty_csv: pass #create an empty .csv file

for key, table in df.groupby(['MemberId', 'JourneyId']):
    table.index = range(len(table))
    i = 0
    first_date = 0
    leeen = len(table)
    while i in range(len(table)):
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

        for j in range(i, i + f + 1):
            table.loc[j, 'AvgNumberOfActions'] = table.loc[:j, 'DaillyActions'].mean()
            table.loc[j, 'StdDevNumberOfActions'] = table.loc[:j, 'DaillyActions'].std()

        i = (i + f) + 1
        first_date = second_date
    table = table.fillna(0)

    table.to_csv(filepath, mode='a', index=False, header=(os.path.getsize(filepath) == 0))

    print()