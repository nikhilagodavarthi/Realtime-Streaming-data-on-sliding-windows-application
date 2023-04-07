from flask import Flask,render_template,redirect,request,session
from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

client=MongoClient('localhost',27017)
db=client['A8']
c=db['dataset']

app=Flask(__name__)

def window3():
    data=[]
    for i in c.find():
        dummy=[]
        dummy.append(i['Humidity'])
        dummy.append(i['Temperature'])
        dummy.append(i['Rainfall'])
        dummy.append(i['Moisture'])
        dummy.append(i['pH'])
        dummy.append(i['label'])
        dummy.append(i['timestamp'])
        data.append(dummy)
    dataframe=pd.DataFrame(data)
    dataframe.to_csv('dataset.csv')

def window4():
    dataset=pd.read_csv('dataset.csv')
    X=dataset.iloc[:,0].values
    Y=dataset.iloc[:,-2].values
    X=X.reshape(-1,1)
    
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2)
    return (X_train,X_test,Y_train,Y_test)


@app.route('/')
def homePage():
    data=[]
    for i in c.find():
        dummy=[]
        dummy.append(i['Humidity'])
        dummy.append(i['Temperature'])
        dummy.append(i['Rainfall'])
        dummy.append(i['Moisture'])
        dummy.append(i['pH'])
        dummy.append(i['label'])
        dummy.append(i['timestamp'])
        data.append(dummy)
    return render_template('index.html',dashboard_data=data,len=len(data))

@app.route('/predict')
def predictedDataPage():
    window3()
    X_train,X_test,Y_train,Y_test=window4()
    regressor=LogisticRegression()
    regressor.fit(X_train,Y_train)

    data=[]
    for i in c.find():
        dummy=[]
        dummy.append(i['Humidity'])
        dummy.append(i['Temperature'])
        dummy.append(i['Rainfall'])
        dummy.append(i['Moisture'])
        dummy.append(i['pH'])
        dummy.append(i['label'])
        dummy.append(i['timestamp'])
        result=regressor.predict([i['Humidity']])
        dummy.append(result[0])
        data.append(dummy)
    return render_template('model.html',dashboard_data=data,len=len(data))


if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000)