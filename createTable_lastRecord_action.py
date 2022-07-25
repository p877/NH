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

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

filepath = '.'
lenTable = 200



try:
    # df = pd.read_csv(os.path.join(filepath, 'featureprocess.csv'), nrows=1000)
    df = pd.read_csv(os.path.join(filepath,'featureprocess.csv'))
except:
    # df = pd.read_csv(os.path.join(filepath,'featureprocess.csv'), nrows=1000,  compression='zip')
    df = pd.read_csv(os.path.join(filepath, 'featureprocess.csv'), compression='zip')

if os.path.isfile(os.path.join(filepath,'oneRecord_{}_new.csv'.format(lenTable))):
   os.remove(os.path.join(filepath,'oneRecord_{}_new.csv'.format(lenTable)))
with open(os.path.join(filepath,'oneRecord_{}_new.csv'.format(lenTable)), "w") as my_empty_csv: pass #create an empty .csv file

newDF2 = pd.DataFrame(data = list(), columns=df.columns)

chunksize = 200000
k = 0
D = []
Event_Element = df['Event'].unique().tolist() + [str(col) for col in df['Element'].unique()]
Event_Element = [col for col in Event_Element if col!= 'nan']
for key, table in df.groupby(['MemberId', 'JourneyId']):
    if table.shape[0] >= lenTable:
        actionDF = table.head(lenTable).reset_index()
    else:
        actionDF = table.reset_index()
        #actionDF['TotalNumberOfDays'] = actionDF.groupby(['Event','Element'],as_index=False).size()['size']
    actionDF1=  pd.DataFrame(data = list())
    actionDF1[['Event','Element','ActionCount']] = actionDF.groupby(['Event','Element'], as_index=False).size()
    actionDF1['TotalNumberOfDays'] = actionDF1['ActionCount']/24
    actionDF1['AvgNumberOfDays'] = actionDF1['TotalNumberOfDays'].mean()
    actionDF1['StdDevNumberOfDays'] = actionDF1['TotalNumberOfDays'].std()
    actionDF1['MemberId'] = actionDF['MemberId']
    actionDF1['JourneyId'] = actionDF['JourneyId']
    actionDF1['target'] = actionDF['target']
    actionDF1['Time_JourneyStarted_week'] = actionDF['Time_JourneyStarted_week']




    actionDF2_Event = pd.DataFrame(data=list())
    # actionDF2_Element= pd.DataFrame(data=list())
    actionDF2_Event[['Event','EventCount']] = actionDF.groupby(['Event'], as_index=False).size()
    Event_list = actionDF2_Event['Event'].to_list()
    actionDF1[Event_list] = actionDF2_Event['EventCount']
    actionDF1['SumAction'] = actionDF2_Event['EventCount'].sum()


    actionDF2_Element = pd.DataFrame(data=list())
    actionDF2_Element[['Element', 'ElementCount']] = actionDF.groupby(['Element'], as_index=False).size()
    Element_list = actionDF2_Element['Element'].to_list()
    actionDF1[Element_list] = actionDF2_Element['ElementCount']
    actionDF1['LengthCourse'] = actionDF2_Element['ElementCount'].sum()



    D.append(actionDF1.tail(1))

newDF2 = pd.concat(D, ignore_index=True)
# newDF2[Event_Element] = 0
print()
newDF2 = newDF2.fillna(0)
newDF2[newDF2.columns].to_csv(os.path.join(filepath, 'oneRecord_{}_new.csv'.format(lenTable)), mode='a', index=False,header=(os.path.getsize(os.path.join(filepath, 'oneRecord_{}_new.csv'.format(lenTable))) == 0))




