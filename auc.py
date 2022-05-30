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
from sklearn.metrics import roc_curve, auc

mainfea=pd.read_csv("oneRecord_20_new.csv")
features_col = [
    'Time_JourneyStarted_week',
    'LengthCourse','AvgLengthCourse',
    'TotalNumberOfActions','AvgNumberOfActions','StdDevNumberOfActions',
    'AudioStarted', 'VideoStarted','AudioPaused','VideoPaused',
    'BookmarkCreated', 'BookmarkViewed',
    'ElementOpened','ElementRetest','JourneyStarted','LinkedInShared',
    'JourneyVisited','ElementInProgress', 'ElementDone',
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





model = clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
fpr, tpr, thresh = roc_curve(y_test, y_pred)
auc = auc(fpr, tpr)
print("AUC:", auc)



plt.plot(fpr, tpr, label='ROC curve (area = %.2f)' %auc)
plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Random')
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.grid()
plt.legend()
plt.show()







