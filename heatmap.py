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
import seaborn as sns
df=pd.read_csv("FeatureImportance.csv", sep=";", index_col=0)

#print(df.head(10))

plt.figure(figsize=(10, 10))
ax = sns.heatmap(df, annot=False, linewidths=.5, cmap="Blues_r", cbar = False)
ax.set(ylabel="")
#ax.set_xticklabels(rotation = 30)
#ax.xaxis.set_tick_params(labeltop='on')
plt.tight_layout()
plt.savefig("heatmap.png")

