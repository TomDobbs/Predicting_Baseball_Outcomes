# -*- coding: utf-8 -*-
"""
YELP DATA HOMEWORK

- Thomas Dobbs
"""
import itertools as it
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics
import statsmodels.formula.api as smf

# visualization
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

# 1
data = pd.read_csv('yelp.csv', index_col=0)
# 2
data.head()
sns.pairplot(data)
data.corr()

# 3
    # create X and y
feature_cols = ['useful', 'cool', 'funny']
X = data[feature_cols]
y = data.stars

# 4
    # instantiate and fit
linreg = LinearRegression()
linreg.fit(X, y)
    # print the coefficients
print linreg.intercept_
print linreg.coef_
    # pair the feature names with the coefficients
zip(feature_cols, linreg.coef_)
    # create a fitted model with all three features
lm = smf.ols(formula='stars ~ useful + funny + cool', data=data).fit()
lm.summary()
# 5
    # print the p-values for the model coefficients
print lm.pvalues
# define a function that accepts X and y and computes testing RMSE
def train_test_rmse(X, y):s
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)
    y_pred = linreg.predict(X_test)
    return np.sqrt(metrics.mean_squared_error(y_test, y_pred))
# include everything
def best_rmse(dataset,target,features):
    best_fit = None
    y = dataset[target]
    for i in range(1, len(feature_cols)+1):    
        for subset in it.combinations(feature_cols, i):
            subset = list(subset)  
            X = dataset[subset]
            rmse = train_test_rmse(X, y)
            if best_fit is None:
                best_fit = rmse
            elif rmse < best_fit:
                best_fit = rmse
            else:
                pass
    print 'RMSE of',best_fit,'for',subset,'subset'

feature_cols = ['useful', 'funny', 'cool']
target = ['stars']                
best_rmse(data,target,feature_cols)

#6
    # exclude Useful
feature_cols = ['funny', 'cool']
X = data[feature_cols]
print train_test_rmse(X, y)
    # exclude Cool
feature_cols = ['funny', 'useful']
X = data[feature_cols] 
print train_test_rmse(X, y)
    # exclude Funny
feature_cols = ['useful', 'cool']
X = data[feature_cols]
print train_test_rmse(X, y)