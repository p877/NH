import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyodbc

cnxn = pyodbc.connect('Driver={ODBC Driver 11 for SQL Server};Server=localhost;Database=Full SQL database;Trusted_Connection=yes')

cursor = cnxn.cursor()
pd.set_option('display.max_columns', None)

def df_quality(df):
    """
    Data quality checks per dataframe
    :param df:
    :param db_dtypes:
    :return:
    """

    def null_count(df):
        """
        Percentage of Null values
        :param df:
        :return:
        """

        return df.isna().sum()

    def dtypes(df):
        """
        Dataframe data types
        :param df:
        :return:
        """
        return df.dtypes

    def uniqueness(df):
        """
        Dataframe unique values per column
        :param df:
        :return:
        """
        return df.nunique()

    def df_describe(df):
        """
        Dataframe statistics
        :param df:
        :return:
        """
        return df.describe(include='all')

    df = df.copy()
    data_describe = df_describe(df)
    data_types = dtypes(df)
    data_unique = uniqueness(df)

    data_describe.loc['nulls'] = null_count(df)
    data_describe.loc['dtypes'] = data_types
    data_describe.loc['unique'] = data_unique

    return data_describe


def temporal_features(df, date_cols):
    """
    extracting check-in features
    :param df: dataframe tat includes booking.checkin_at
    :return booking_core: dataframe with new columns for extracted features
            new_cols: list of features label
    """
    df[date_cols]=df[date_cols].apply(pd.to_datetime)
    for col in date_cols:
        df[col + '_week'] = df[col].dt.isocalendar().week
        # df[col + '_dayofyear'] = df[col].dt.dayofyear
        df[col + '_dayofweek'] = df[col].dt.dayofweek
        df[col + '_weekend'] = 0
        df.loc[df[col + '_dayofweek'].isin([5, 6]), col + '_weekend'] = 1


    return df


# import matplotlib.pyplot as plt

df1=pd.read_sql("select Event,MemberId,JourneyId,ElementType, CAST(Time as DATE) D  from nhMemberEvent",cnxn)
df2=pd.read_excel('start_end1.xlsx',sheet_name='s1',engine='openpyxl')
df3=pd.read_excel('start_without_end1.xlsx',sheet_name='s1',engine='openpyxl')
df2["target"]=1
df12=df2

print(df3.dtypes)
print(df12.dtypes)
df12["JourneyId"] = df12["JourneyId"].astype("int")
df3=df3.drop("Time_JourneyCompleted", axis=1)
df3["target"]=0
df13=df3
df123=pd.concat([df12, df13])


print(df123.dtypes)
col_date=["Time_JourneyStarted"]
features=temporal_features(df123, col_date)

#Remove empty journeyId and empty journey started and journey completed
features["Time_JourneyCompleted_year"].fillna(0, inplace=True)
features= features[features['JourneyId'].notna()]
features["Time_JourneyCompleted"].fillna(0, inplace=True)
features["Time_JourneyStarted"].fillna(0, inplace=True)
#Journey length based on day, hour, minute/ second
features["Duration"].fillna(-1, inplace=True)
#Journey length based on day
features["days"].fillna(-1, inplace=True)

features.to_csv("features2.csv")


