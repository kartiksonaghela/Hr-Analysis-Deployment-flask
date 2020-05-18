import pandas as pd
import numpy as np
from sklearn import model_selection, tree, preprocessing, metrics, linear_model
import math, time, random, datetime
import pickle
train = pd.read_csv('train.csv')
train['previous_year_rating'].fillna((train['previous_year_rating'].mean()),inplace=True)
train=train.replace(["Master's & above","Bachelor's","Below Secondary"],[0,1,2])
train.drop(['region','recruitment_channel'],axis=1,inplace=True)
train['education']=train['education'].round()
train['previous_year_rating']=train['previous_year_rating'].round()
train.drop('length_of_service',axis=1,inplace=True)
train['avg_training_score']=pd.cut(train['avg_training_score'], bins=5)
x_train=pd.get_dummies(train,columns=['department','education','gender','no_of_trainings','previous_year_rating','KPIs_met >80%','awards_won?','avg_training_score'])
x_train=x_train.drop('is_promoted',axis=1)
x_train=x_train.drop('no_of_trainings_10',axis=1)
x_train=x_train.drop('age',axis=1)
x_train=x_train.drop('employee_id',axis=1)
y_train=train.is_promoted
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()

#Fitting model with trainig data
regressor.fit(x_train, y_train)

# Saving model to disk
pickle.dump(regressor, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))

pickle.dump(model,open('model.pkl','wb'))
