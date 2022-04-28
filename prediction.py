import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier

#mainfea=pd.read_csv("finalTable.csv")
mainfea=pd.read_csv("finalTable.csv")
features_col = [
    'Time_JourneyStarted_week',
     #'Event',
    'ElementType',
    'TotalNumberOfActions','AvgNumberOfActions','StdDevNumberOfActions',
     'AudioStarted', 'VideoStarted','AudioPaused','VideoPaused',
            'BookmarkCreated', 'BookmarkViewed',
    # CertificateDownloaded, CertificateEarned, GoalCompleted,JourneyCompleted,ElementDone,'BadgeEarned',
     'ElementOpened','ElementRetest','JourneyStarted','LinkedInShared',
    'JourneyVisited','ElementInProgress',
     'ReviewAdded',
    'StuckButtonUsed', 'SupporterFeedbackPosted', 'SupporterInvited',  'JourneyAssignedToGoal','SupporterLinkOpened','SupporterLinkExpired',
    'ToggleTranscript',
    'Goal','InstructionWizard','OpenTask','Questionnaire','Vrt','VideoAssignment','TextualExplanation'
]

######################
print("Class Sizes")
print(mainfea.groupby("target").size())
X = mainfea[features_col]
X = X.fillna(0)
y = mainfea["target"]
X_train, X_test, y_train, y_test = train_test_split(X, y)
kf=KFold(n_splits=10, random_state=None, shuffle=True)
# X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
#max_depth=10,
clf = RandomForestClassifier(max_depth=10, random_state=0, n_estimators=10)
#clf = DecisionTreeClassifier()
#clf = SVC()
scores = cross_val_score(clf, X, y, scoring='accuracy', cv=kf)

print("Accuracy", scores)
model = clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
#
# from sklearn.metrics import accuracy_score
# print("Accuracy", accuracy_score(y_test, y_pred))
# from sklearn.metrics import confusion_matrix
# print("Confusion", confusion_matrix(y_test, y_pred))

print("Features Importance", clf.feature_importances_)
print("Features Labels", features_col)
indices = np.argsort(clf.feature_importances_)
importances = clf.feature_importances_

mainfea_importances = pd.Series(clf.feature_importances_, index=X.columns)
mainfea_importances.nlargest(len(X.columns)).plot(kind='barh', figsize = (10, 10))
plt.tight_layout()
#plt.show()
plt.savefig("day.png")
# from sklearn.metrics import classification_report
# print(classification_report(y_test,y_pred))
# k = 0
# leenTable = 5
# total = pd.Series(data=np.zeros(shape=len(mainfea)))
# for i in range(len(mainfea)):
#         if (i+1)%leenTable == 0:
#          total[k] = mainfea.loc[i,'TotalNumberOfActions']
#         k = k + 1
# print(total[:k-1])

leenTable = 5
total = pd.Series(data=np.array(len(mainfea)))
avg= pd.Series(data=np.array(len(mainfea)))
std= pd.Series(data=np.array(len(mainfea)))
k = 0
for i, table in mainfea.groupby(['MemberId', 'JourneyId']):
    vals = table.index.values
    total[k] = table.loc[vals[table.__len__()-1], 'TotalNumberOfActions']
    avg[k] = table.loc[vals[table.__len__() - 1], 'AvgNumberOfActions']
    std[k] = table.loc[vals[table.__len__() - 1], 'StdDevNumberOfActions']
    k = k + 1
print("TotalNumberOfActions")
print(total)
print("AvgNumberOfActions")
print(avg)
print("StdDevNumberOfActions")
print(std)

# print("TotalNumberOfActions")
# print(mainfea['TotalNumberOfActions'].unique())
# print("AvgNumberOfActions")
# print(mainfea['AvgNumberOfActions'].unique())
# print("StdDevNumberOfActions")
# print(mainfea['StdDevNumberOfActions'].unique())

# df = mainfea[['MemberId', 'JourneyId','Time_JourneyStarted','D']]
# df.to_csv("Member_Journey_StartDate_D.csv")
#mainfea['MemberId'].nunique()
#mainfea['JourneyId'].nunique()
#len(pd.read_csv("features2.csv").groupby(['MemberId','JourneyId']).size())
#len(mainfea.groupby(['MemberId','JourneyId']).size())

# file_path = 'randomfile.txt'
# sys.stdout = open(file_path, "w")
# print(mainfea['AvgNumberOfActions'].unique())
