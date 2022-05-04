
Below are the steps we have taken::

1) First, we use the following scripts to get the basic statistics of our data frame (main table from ‘nhMemberEvent’ Table in NewHeroes dataset ). It shows dtypes,  number of null, number of unique values, plus statistics per column. 


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


Then we extract the finished journeys  (finished.py, start_end.xlsx) and unfinished journeys (unfinished.py, start_without_end.xlsx).  In the above tables, Time_JourneyStarted column shows the started date of journey and Time_JourneyCompleted shows the end date of journey. Therefore, Time_JourneyCompleted for the finished journeys will be a specific date which is shown in  start_end.xlsx but there’s no completed date in start_without_end.xlsx. Since journey has not finishe yet.
 Next, we select all actions (e.g., events, elements) plus Time of actions done by users from ‘nhMemberEvent’ Table in NewHeroes dataset  then we join the above Table  with (start_end.xlsx and start_without_end.xlsx) Tables to have all members and journeys including started date and completed date of jourenys  as well as  the actions  and Time of actions in one single Table. Also, during preprocessing we remove empty journeys without started and completed date (makefeatures.py, featureprocess.csv). Following are the columns:
MemberId: List of users who participate in one or multiple courses (journeys)
JourneyId: List of courses have been taken by users.
Event: all events done by all users for all courses ( e.g., 'AudioStarted', 'VideoStarted','AudioPaused','VideoPaused', 'BookmarkCreated', 'BookmarkViewed', 'CertificateDownloaded', CertificateEarned, GoalCompleted,JourneyCompleted,ElementDone,'BadgeEarned', 'ElementOpened','ElementRetest','JourneyStarted','LinkedInShared', 'JourneyVisited','ElementInProgress','ReviewAdded', 'StuckButtonUsed', 'SupporterFeedbackPosted', 'SupporterInvited',  'JourneyAssignedToGoal','SupporterLinkOpened','SupporterLinkExpired', 'ToggleTranscript').

 ElementType: all types of tasks done by all users for all courses (e.g., 'Goal','InstructionWizard','OpenTask','Questionnaire','Vrt','VideoAssignment','TextualExplanation’). 
Time_JourneyStarted: The started date/time of a journey by a user. (fixed number for each user and course combination).
D: The started date for a journey by a user (exatracted from Time_JourneyStarted but without time). We add this variable to show the number of days (This will be explained in more detail later).
Time_JourneyStarted_week:  The number of week of a year in which a journey started.
Time_JourneyCompleted: the completed date of a journey. As above mentioned, If the journey has been completed, there is a specific date in Time_JourneyCompleted. Otherwise, it will be zero. Since there is no complete date yet.
Target: We add this binary number to see finished and unfinished journeys.If Journey has been completed, it would be 1, otherwise 0.




2) Second, we are going to compute the number of actions has been done by each user for each course from the first day that course has been started. If a user starts a course at a particular time on a particular day, we will call that moment the start of day 1.  After 24 hours, this user has done something in that course, then day 2 starts. So, if we want to classify that information of , for example, 5 days; for each user we identify the period from the moment they started of their course plus 5 times 24 hours (which is 5 days, for now). We then select all actions (events + elements) that have been done by that user in that course in this period of time.  We use this information to classify meaning that for all classifiers (or settings for the classifiers), we will have as many data points/instances as there are user/course combinations in the entire dataset. So below what is needed for each user/course combination:

a. Collect information of the course itself and the user itself (Member_Journey.csv) which extracted from 'featureprocess.csv’ using the following script:

df = pd.read_csv('featureprocess.csv')
df.groupby(['MemberId','JourneyId']).size()
(There are 17323 unique user/course combination).

b. Note the start date/time for this person/course combination (Member_Journey_StartDate.csv) through following script
df.groupby(['MemberId','JourneyId','Time_JourneyStarted']).size()
(There are 17323 unique user/course/start_date combination as well).

c. Collect information on the actions that person has taken within
the course’.


There are two problems in 'featureprocess.csv’ : According to the number of actions that the user has performed for each course, this is repeated for each user/course combination in many entries (data duplication). Also, there are no separate columns for each types of events and elements. As aforementioned,, all types of events are placed in Event column and all types of elements placed in ElementType column.

Therefore, to collect information on the actions that each user has taken for each course from day1, first, we need to normalize our current dataset (i.e., featureprocess.csv) by day. To do this, we create 'table-D_MemberId_JourneyId.csv'  extracted from 'featureprocess.csv'  using (createTable.py) to user/course in formation in daily basis. This way, we also have all types of events and elements in seperate columns so we can calculate the the total number of actions for each user/course combination separately by day.  table-D_MemberId_JourneyId.csv columns are as follows (below we only explain the new and modified columns):
 
Event: total number of all events done by a user for a particular course, namely, total number of  the following columns:  'AudioStarted', 'VideoStarted','AudioPaused','VideoPaused', 'BookmarkCreated', 'BookmarkViewed', 'CertificateDownloaded', CertificateEarned, GoalCompleted,JourneyCompleted,ElementDone,'BadgeEarned', 'ElementOpened','ElementRetest','JourneyStarted','LinkedInShared', 'JourneyVisited','ElementInProgress','ReviewAdded', 'StuckButtonUsed', 'SupporterFeedbackPosted', 'SupporterInvited',  'JourneyAssignedToGoal','SupporterLinkOpened','SupporterLinkExpired', 'ToggleTranscript'. As you can see, each of the above events are currently placed in the separate columns (‘V’ to ‘AU’ columns) so we can calcaulate the total number of them and put the result into the 'Event' column (for each user/course combination).

 ElementType: total number of all types of tasks done by a user for a particular course,  namely, total number of  the following columns: 'Goal','InstructionWizard','OpenTask','Questionnaire','Vrt','VideoAssignment','TextualExplanation'. Similar to Event, each of the above elements are currently placed in separate columns  (‘AV’ to ‘BB’ columns) so we can calculate the total number of them and put it into the 'ElementType' column (for each user/course combination).

DaillyActions: The total number of actions (‘Event’+ ‘ElementType’) for each user/couser combination by day .

‘'TotalNumberOfActions','AvgNumberOfActions', and 'StdDevNumberOfActions' colums will be used on the next code (createTable_nRecords
2.py to create the ‘finalTable.csv’

Perhaps, we can combine the steps 2 and 3 in one single step (single code with one single table). But for the convenience and to keep things more clear, I preferred to run the experiment step by step. 

3) For the ‘‘finalTable.csv’, as above mentioned, we use ‘D’ for keeping the number of days. For example, for MemberId 1953 and JourneyId 2265, the journey has been started on 2016-06-29. As said, the Time_JourneyStarted is a fixed number to show the start date and time for each user/course combination. Therefore, we need to have a variable like D to keep the number of days from the starting date. In other words, we need to add a column as a counter that has the start time/date but then plus X number of days, so ‘D’ is a  column with the start time plus X days, where X can be modified in our script. Because we will be varying this X. Here we have X = 5 days. The number of actions will need to be counted between the start time and the start time + X days. 
To clarify, as said, ‘DaillyActions’ keeps the number of actions for each day as follows:

day 1 8 action
day 2 0 actions
day 3 0 actions
day 4 0 actions
day 5 0 actions

Since there are no actions from day 2 to day 5, we need to add 4 more entries to show 0 actions for  the days in which nothing happened.

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


‘StdDevNumberOfActions’ is the standard deviation also  is computed the same way as AvgNumberOfAction so in total std would be 3.5777088 .

Similarly, we apply the same approach for the rest of user/ course combinations, however, for some users who finished the course (target =1)  on the first day (e.g., user 1953, Journey 2680), we only have one day. Since they have already done on the first day (You can see the related code in createTable_nRecords.py).

The above file that we created per user/course contain something like 5 lines, so 5 instances. Consequently, we get 5 times as many instances as we want.  In other words, if we concatenate all user/course csv files, we will get 5*17323 instances (5 times as many instances) which is not correct whereas the file we need for the classifier has the same number of instances (i.e., 17323). One instance here is description of one user in one course, namely, one user/course combination will always remain to be 1 instance, so 1 line in the csv file. Therefore, we need to create a simple feature vector file with as many instances (17323) which is shown the final result on the last day not one by one for all days., For  example, here, we need to see the final  result  on the fifth day which includes all the results (e.g., ‘TotalNumberOfActions’, ‘AvgNumberOfAction’, ‘StdDevNumberOfAction’) from day 1 to day 5 (or whatever day). This way by changing the number of days, we always have the same number of instances (17323). Therefore, for the classifier we use (oneRecord_5_new.csv) which is created using (createTable_lastRecord.py).    

 

3) Finally, we run random forest classifier using 10CV on the (oneRecord_5_new.csv) through (prediction.py) with the following features: 

'Time_JourneyStarted_week': the number of week in which Journey started

'LengthCourse': (the new name for the ElemenType. Since the ‘ElemenType’ is Number of elements in the course, to clarify we change the name to ‘LengthCourse’).

'TotalNumberOfActions' (Total number of actions (integer number) user has performed in the course).
'AvgNumberOfActions' (Average number of actions (real number) user has performed per day).
'StdDevNumberOfActions' (Standard deviation of number of actions (real number) user has performed per day).
 
All type of elements: 'Goal','InstructionWizard','OpenTask','Questionnaire','Vrt','VideoAssignment','TextualExplanation'

All type of events:
'AudioStarted', 'VideoStarted','AudioPaused','VideoPaused',
 'BookmarkCreated', 'BookmarkViewed','ElementOpened','ElementRetest','ElementDone','JourneyStarted','LinkedInShared','JourneyVisited','ElementInProgress',
   'ReviewAdded','StuckButtonUsed', 'SupporterFeedbackPosted', 'SupporterInvited',  'JourneyAssignedToGoal','SupporterLinkOpened','SupporterLinkExpired','ToggleTranscript':   
 
 
You can obseve the results for the first 5 days as follows:
the value of the features vector  in (Features_value_5.csv) and 
the features importance plus the accuracy e.g., 10CV, recall, precision  results in (Accuracy_FeatureImportance_5.pdf).
To clarify the feature importance plot is shown in (FeatureImportance_plot_5.png) as well. As shown in the Figure,  you can observe the features importance for the first 5 days. These are the list of  features that we use for the prediction model.


P.S. Python codes are shared in the Github ‘’https://github.com/p877/NH’’ and 
Datasets plus results are in the Google Drive ‘’https://drive.google.com/drive/folders/1xg1TsUuTi8S-kFkYm_kPJunvWkcZfqjx?usp=sharing’’.


