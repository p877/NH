import pyodbc
import datetime
cnxn = pyodbc.connect('Driver={ODBC Driver 11 for SQL Server};Server=localhost;Database=Full SQL database;Trusted_Connection=yes')

import pandas as pd
cursor = cnxn.cursor()
# cursor.execute('select E.Event,E.Time,E.JourneyId,E.MemberId,S.CompletedDate from nhMemberEvent E INNER JOIN nhJourneyStatus S on E.MemberId=S.MemberId and E.JourneyId=S.JourneyId where S.status=1 ')
# cursor.execute("select distinct JourneyId,MemberId from nhJourneyStatus ")

c=0
for r in cursor:
    print(c+1)
    c+=1
    # print(r)
L=[]
L2=[]
# df=pd.read_sql("select E.JourneyId,E.MemberId,E.Event,E.Time,E2.Event,E2.Time  from nhMemberEvent E INNER JOIN nhMemberEvent E2 on E.MemberId=E2.MemberId and E.JourneyId=E2.JourneyId where E.Event='JourneyStarted' and E2.Event='JourneyCompleted'",cnxn)
df=pd.read_sql("select E.JourneyId,E.MemberId,E.Event,E.Time,S.Status,S.CompletedDate  from nhMemberEvent E INNER JOIN nhJourneyStatus S on E.MemberId=S.MemberId and E.JourneyId=S.JourneyId where S.Status=0 and E.Event='JourneyStarted' ",cnxn)
for i in range(df.shape[0]):
    t1=df.iloc[i,3]
    t2=df.iloc[i,5]
    t3=t2-t1
    L.append(str(t3))
    L2.append(t3.days)
#
#
df['Duration']=L
df['days']=L2
df.to_excel('start_end.xlsx',sheet_name='s1')
print(df)