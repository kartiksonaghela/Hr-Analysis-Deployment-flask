import numpy as np
import pandas as pd
from flask import Flask,request,jsonify,render_template
import pickle

def cal(x,y):
    if(y==1):
        x='department_'+x
        dict1={'department_Analytics':0,'department_Finance':0,'department_HR':0,'department_Legal':0,'department_Operations':0,'department_Procurement':0,'department_R&D':0,'department_Sales & Marketing':0,'department_Technology':0}
        if x in dict1:
            dict1[x]=1
    elif(y==2):
        dict1={'education_0.0':0,'education_1.0':0,'education_2.0':0}
        if(x=='Masters'):
            dict1['education_0.0']=1
        if(x=='Bachelors'):
            dict1['education_1.0']=1
        if(x=='Below Secondary'):
            dict1['education_2.0']=1
    elif(y==3):
        x='gender_'+x
        dict1={'gender_f':0, 'gender_m':0}
        if x in dict1:
            dict1[x]=1
    elif(y==4):
        x='no_of_trainings_'+x
        dict1={'no_of_trainings_1':0,
       'no_of_trainings_2':0, 'no_of_trainings_3':0, 'no_of_trainings_4':0,
       'no_of_trainings_5':0, 'no_of_trainings_6':0, 'no_of_trainings_7':0,
       'no_of_trainings_8':0, 'no_of_trainings_9':0}
        if x in dict1:
            dict1[x]=1
    elif(y==5):
        x='previous_year_rating_'+x+'.0'
        dict1={'previous_year_rating_1.0':0,
       'previous_year_rating_2.0':0, 'previous_year_rating_3.0':0,
       'previous_year_rating_4.0':0, 'previous_year_rating_5.0':0}
        if x in dict1:
            dict1[x]=1
    elif(y==6):
        dict1={'KPIs_met >80%_0':0, 'KPIs_met >80%_1':0}
        if(x=='Yes'):
            dict1['KPIs_met >80%_1']=1
        if(x=='No'):
            dict1['KPIs_met >80%_0']=1
    elif(y==7):
        dict1={'awards_won?_0':0, 'awards_won?_1':0}
        if(x=='Yes'):
            dict1['awards_won?_1']=1
        if(x=='No'):
            dict1['awards_won?_0']=1
    else:
        x=int(x)
        dict1={'avg_training_score_(38.94, 51.0]':0, 'avg_training_score_(51.0, 63.0]':0,
       'avg_training_score_(63.0, 75.0]':0, 'avg_training_score_(75.0, 87.0]':0,
       'avg_training_score_(87.0, 99.0]':0}
        if  38.94<x<=51.0:
            dict1['avg_training_score_(38.94, 51.0]']=1
        if  51.0<x<=63.0:
            dict1['avg_training_score_(51.0, 63.0]']=1
        if  63.0 <x<=75.0:
            dict1['avg_training_score_(63.0, 75.0]']=1
        if  75.0<x <= 87.0:
            dict1['avg_training_score_(75.0, 87.0]']=1
        if  87.0 < x <= 99.0:
            dict1['avg_training_score_(87.0, 99.0]']=1    
    return dict1     
            
app=Flask(__name__,template_folder='templates')
model=pickle.load(open('model.pkl','rb'))
@app.route('/')
def index():
	
	return render_template('index2.html')
@app.route('/results', methods=['POST'])
def predict():
    Department=request.form['Department']
    dept=cal(Department,1)
    Education=request.form['Education']
    edu=cal(Education,2)
    Gender=request.form['Gender']
    gen=cal(Gender,3)
    No_of_trainings=request.form['No_of_trainings']
    train=cal(No_of_trainings,4)
    previous_year_rating=request.form['previous_year_rating']
    previous=cal(previous_year_rating,5)
    KPIs_met=request.form['KPIs_met']
    kpi=cal(KPIs_met,6)
    Awards=request.form['Awards_won']
    award=cal(Awards,7)
    Avg_training_score=request.form['Avg_training_score']
    avg_train=cal(Avg_training_score,8)
    input_data =[{**dept,**edu,**gen,**train,**previous,**kpi,**award,**avg_train}]
    final=[]
    data = pd.DataFrame(input_data)
    prediction = model.predict(data)[0]
    prediction=round(prediction)
    print(prediction)
    if (prediction==1.0):
        output='Is_promoted'
    else:
        output='Not_promoted'
    return render_template('index2.html',prediction_text="The employee is {}".format(output))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)