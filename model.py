import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import style
import statsmodels.api as sm
import seaborn as sb
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from os import system 
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import fbeta_score, make_scorer
from sklearn.grid_search import GridSearchCV
import math


# Read data into a consolidated game and 
project_df = pd.read_csv('CONSOLIDATED_DCB_DATA.csv')
project_df = project_df.drop(project_df.columns[[0]],axis=1)
project_df = project_df[np.isfinite(project_df['Chg_from_50davg'])]

# Statsmodels requires the creation of an intercept
project_df['Intercept'] = 1
train_positives = project_df.iloc[0:39,:]
train_negatives = project_df[project_df['Is_Dead_Cat']==0].iloc[0:259,:]
df_train = train_positives.append(train_negatives, ignore_index=True)

# Now create the test dataset
test_positives = project_df.iloc[39:62]
test_negatives = project_df[project_df['Is_Dead_Cat']==0].iloc[259:,:]
df_test = test_positives.append(test_negatives, ignore_index=True)

# LOG REGRESSION MODEL
x_cols = ['Chg_from_Hi','Chg_from_Lo','Chg_from_50davg','Short_Ratio','Intercept']
x_train = df_train[x_cols]
y_train = df_train['Is_Dead_Cat']

logit = sm.Logit(y_train, x_train)
DCB_model = logit.fit()

# Make predictions on the model
x_test = df_test[x_cols]
df_test['DCB_Prob'] = DCB_model.predict(x_test)

# Keep threshold low to minimize false negatives.
def binary_predictor(x):
    if x > 0.1:
        return int(1)
    else:
        return int(0)

# Test accuracy for overall model
df_test['Log_Prediction'] = df_test.DCB_Prob.map(binary_predictor)
df_test['Check'] = df_test.Log_Prediction == df_test.Is_Dead_Cat
print df_test['Check'].value_counts(True)

# Test accuracy on subset where stocks are Dead Cats
subset = df_test[df_test['Is_Dead_Cat']==1]
print subset['Check'].value_counts(True)



# DECISION TREE MODEL
treeModel = DecisionTreeClassifier(max_depth = 4, criterion="entropy")
tree_cols = ['Chg_from_Hi','Chg_from_Lo','Chg_from_50davg','Short_Ratio']

def visualize_tree(model): 
    dotfile = open("tree.dot", 'w')
    export_graphviz(model, out_file = dotfile, feature_names = X_tree.columns)
    dotfile.close()
    system("dot -Tpng tree.dot -o tree.png")

treedf_train = df_train.copy()
X_tree = treedf_train[tree_cols]
Y_tree = treedf_train['Is_Dead_Cat']

treeModel.fit(X_tree, Y_tree)
visualize_tree(treeModel)

treedf_test = df_test.copy()
treedf_test = treedf_test.drop(['Intercept','DCB_Prob','Log_Prediction','Check'], axis=1)
X_treetest = treedf_test[tree_cols]
#print treedf_test.head()

treedf_test['Tree_Prediction'] = treeModel.predict(X_treetest)
treedf_test['Check'] = treedf_test.Tree_Prediction == treedf_test.Is_Dead_Cat
print treedf_test['Check'].value_counts(True)
print treedf_test.head()

