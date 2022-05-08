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
from sklearn.dummy import DummyClassifier

mainfea=pd.read_csv("oneRecord_1_new.csv")
features_col = [
    'Time_JourneyStarted_week',
    'LengthCourse',
    'TotalNumberOfActions','AvgNumberOfActions','StdDevNumberOfActions',
    'AudioStarted', 'VideoStarted','AudioPaused','VideoPaused',
    'BookmarkCreated', 'BookmarkViewed',
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
clf = RandomForestClassifier(max_depth=10, random_state=0, n_estimators=10)

# clf = DummyClassifier(strategy="most_frequent")
# #clf.fit(X, y)
# DummyClassifier(strategy='most_frequent')
# #clf.predict(X)
# model = clf.fit(X_train, y_train)
# y_pred = clf.predict(X_test)

#scores = cross_val_score(clf, X, y, scoring='accuracy', cv=kf)
# print("Accuracy", scores)

score_accuracy = cross_val_score(clf, X, y, scoring='accuracy', cv=kf)
print("Accuracy", score_accuracy)
# mean_accuracy= cross_val_score(clf, X, y, scoring='accuracy', cv=kf).mean()
# print("AvgAccuracy", mean_accuracy)
# std_accuracy= cross_val_score(clf, X, y, scoring='accuracy', cv=kf).std()
# print("StdAccuracy", std_accuracy)

score_precision = cross_val_score(clf, X, y, scoring='precision', cv=kf)
print("precision", score_precision)
# mean_precision= cross_val_score(clf, X, y, scoring='precision', cv=kf).mean()
# print("AvgPrecision", mean_precision)
# std_precision= cross_val_score(clf, X, y, scoring='precision', cv=kf).std()
# print("StdPrecision", std_precision)

score_recall = cross_val_score(clf, X, y, scoring='recall', cv=kf)
print("recall", score_recall)
# mean_recall= cross_val_score(clf, X, y, scoring='recall', cv=kf).mean()
# print("AvgRecall", mean_recall)
# std_recall= cross_val_score(clf, X, y, scoring='recall', cv=kf).std()
# print("StdRecall", std_recall)

score_f1 = cross_val_score(clf, X, y, scoring='f1', cv=kf)
print("f1-score", score_f1)
# mean_f1= cross_val_score(clf, X, y, scoring='f1', cv=kf).mean()
# print("Avgf1-score", mean_f1)
# std_f1= cross_val_score(clf, X, y, scoring='f1', cv=kf).std()
# print("Stdf1-score", std_f1)

model = clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# from sklearn.metrics import accuracy_score
# print("Accuracy", accuracy_score(y_test, y_pred))
from sklearn.metrics import confusion_matrix
print("Confusion", confusion_matrix(y_test, y_pred))

print("Features Importance", clf.feature_importances_)
print("Features Labels", features_col)
indices = np.argsort(clf.feature_importances_)
importances = clf.feature_importances_

mainfea_importances = pd.Series(clf.feature_importances_, index=X.columns)
mainfea_importances.nlargest(len(X.columns)).plot(kind='barh', figsize = (10, 10))
plt.tight_layout()
#plt.show()
plt.savefig("day.png")
from sklearn.metrics import classification_report
print(classification_report(y_test,y_pred))

# leenTable = 5
# total = pd.Series(data=np.array(len(mainfea)))
# avg= pd.Series(data=np.array(len(mainfea)))
# std= pd.Series(data=np.array(len(mainfea)))
# k = 0
# for i, table in mainfea.groupby(['MemberId', 'JourneyId']):
#     vals = table.index.values
#     total[k] = table.loc[vals[table.__len__()-1], 'TotalNumberOfActions']
#     avg[k] = table.loc[vals[table.__len__() - 1], 'AvgNumberOfActions']
#     std[k] = table.loc[vals[table.__len__() - 1], 'StdDevNumberOfActions']
#     k = k + 1
# print("TotalNumberOfActions")
# print(total)
# print("AvgNumberOfActions")
# print(avg)
# print("StdDevNumberOfActions")
# print(std)


