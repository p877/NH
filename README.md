 Below are the steps we have taken:

1) First, we use the following scripts to get the basic statistics of our data frame (main table). It shows dtypes,  number of null, number of unique values, plus statistics per column. Also, we remove the empty journeys without started and completed dates (makefeatures.py and features2.csv). At the same time, we extract the finished journeys  (1xlsfinishedJ.py and start_end1.csv) and unfinished journeys (1xlsunfinishedJ.py and start_without_end1.csv). Here, 'Duration' is considered as Journey length based on day, hour, minute/ second and 'days' is the Journey length only  based on the day.

# Measure basic statistics

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


df_preproc_qa = df_quality(df)
print("\n Raw data statistics:", df_preproc_qa)


# Columns with null values
mask = df_preproc_qa.loc['nulls', :]!=0
col_null = df_preproc_qa.columns[mask]
print(col_null)

2)  If a user starts a course at a particular time on a particular day, we will call that moment the start of day 1.  After 24 hours, this user has done something in that course, then day 2 starts. So, if we want to classify that information of 5 days, for each user we identify the period from the moment they started of their course plus 5 times 24 hours (which is 5 days, for now). We then select all actions (events + elements) that have been done by that user in that course in this period of time.  We use this information to classify. This means that for all classifiers (or settings for the classifiers), we will have as many data points/instances as there are user/course combinations in the entire dataset. So below what is needed for each user/course combination:

a. Collect information of the course itself and the user itself (Member_Journey1.csv) using the following script:

df = pd.read_csv('features2.csv')
df.groupby(['MemberId','JourneyId']).size()
(There are 17323 unique user/course combination).

b. Note the start date/time for this person/course combination (Member_Journey_StartDate1.csv) through following script
df.groupby(['MemberId','JourneyId','Time_JourneyStarted']).size()
(There are 17323 unique user/course/start_date combination).

c. Collect information on the actions that person has taken within
the course.

3) To collect information on the actions that each user has taken for each course from day1, first, we need to normalize our dataset (features2.csv) daily. In view of this, we create a Table (table_3.csv) which is extracted from 'features2.csv'  using (createTable.py). As shown, in 'Features2.csv', there are no separate columns for all types of events and elements. Therefore, we create 'table_3.csv' to put them all in seperate columns to calculate them daily and seperately. table_3.csv columns are as follows:
Event: total number of all events done by a user for a course e.g., 'AudioStarted', 'VideoStarted','AudioPaused','VideoPaused', 'BookmarkCreated', 'BookmarkViewed', 'CertificateDownloaded', CertificateEarned, GoalCompleted,JourneyCompleted,ElementDone,'BadgeEarned', 'ElementOpened','ElementRetest','JourneyStarted','LinkedInShared', 'JourneyVisited','ElementInProgress','ReviewAdded', 'StuckButtonUsed', 'SupporterFeedbackPosted', 'SupporterInvited',  'JourneyAssignedToGoal','SupporterLinkOpened','SupporterLinkExpired', 'ToggleTranscript'. As you can see, each of the above events are located in the separate columns (‘V’ to ‘AU’ columns) so we can calcaulate the total number of them and put the result into the 'Event' column (for each user/course combination).

 ElementType: total number of all types of tasks done by a user for a course e.g., 'Goal','InstructionWizard','OpenTask','Questionnaire','Vrt','VideoAssignment','TextualExplanation'. Similar to Event, each of the above elements is located in separate columns  (‘AV’ to ‘BB’ columns) so we can calculate the total number of them and put it into the 'ElementType' column (for each user/course combination).

Time_JourneyStarted: The started date/time of a journey by a user. (fixed number for each user and course combination).
D: The started date for  a journey by a user ( we use this variable to show the number of days which is started from Day1).
Time_JourneyCompleted: the completed date of a journey. If the journeyhas been completed, there is a specific date in Time_JourneyCompleted. Otherwise, it will be zero. Since there is no complete date yet.
Target: If Journey has been completed, it would be 1, otherwise 0.
 Duration: Journey length based on day, hour, minute/ second.
days:: Journey length only based on day.
Time_JourneyStarted_week:  The number of week in which a journey started.
Time_JourneyStarted_dayofweek: The number of week day in which a journey started (As this feature was not very useful based on previous experiments,  we will not use this feature while running expriment).
Time_JourneyStarted_weekend: If Journey has been started in weekend, it would be 1, otherwise 0 (The same as previous feature, since this feature was not very useful,  we will not consider this feature for expriment).
DaillyActions: The total number of actions for each user/ couser cobination for each day (Event + ElementType).

‘'TotalNumberOfActions','AvgNumberOfActions', and 'StdDevNumberOfActions' colums will be used on the next code (createTable2.py) for  create the ‘finalTable.csv’

Perhaps, we can combine the steps 3 and 4 in one single step (single code with one single table). But for the convenience and to keep things more clear, I preferred to run the experiment step by step. 

4) For the ‘‘finalTable.csv’, as above mentioned, we use ‘D’ for keeping the number of days. For example, for MemberId 1953 and JourneyId 2265, the journey has been started on 2016-06-29. As said, the Time_JourneyStarted is a fixed number for each user/course combination. Therefore, we need to have a variable like D to keep the number of days from the starting date. In other words, we need to add a column as a counter that has the start time/date but then plus X number of days, so ‘D’ is a  column with the start time plus X days, where X can be modified in our script. Because we will be varying this X. Here we have X = 5 days. The number of actions will need to be counted between the start time and the start time + X days. 
As said, ‘DaillyActions’ keeps the number of actions for each day as follows:

day 1 8 action
day 2 0 actions
day 3 0 actions
day 4 0 actions
day 5 0 actions

Since there are no actions from day 2 to day 5, we need to add 4 more rows to show 0 actions for  the days in which nothing happened.

‘TotalNumberOfActions’ will be the total number of actions of the current day plus the number of actions from the previous days  as follows:

day 1 8 action
day 2 8 actions
day 3 8 actions
day 4 8 actions
day 5 8 actions

‘AvgNumberOfActions’ counted as the total number  actions divide by the number of days as follows:

day 1 8.0 action
day 2 4.0 actions
day 3 2.6 actions
day 4 2.0 actions
day 5 1.6 actions




‘StdDevNumberOfActions’ is the standard deviation also  is computed the same way as mean.

Similarly, we apply the same approach for the rest of user/ course combinations, however, for some users who finished the course (target =1)  on the first day (e.g., user 1953, Journey 2680), we only have one day. Since they have already done on the first day (createTable2.py is the related code).

5) Finally , we run a classifier using 10CV on the above file (finalTable.csv) through (prediction.py) with the following accuracy:

Accuracy [0.80304569, 0.81482234, 0.81035533, 0.81482234, 0.80751269, 0.80913706
 0.81563452, 0.8111675,1 0.81360406, 0.81701868].

Also, you can see the plot that shows the features importance in ‘day.png’. As shown in the Figure,  you can observe the features importance for the first 5 days. These are the list of  features that we use for the prediction model.

P.S. Python codes are shared in the Github and datasets in the Google Drive.
