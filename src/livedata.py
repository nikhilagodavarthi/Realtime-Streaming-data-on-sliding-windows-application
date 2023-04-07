import datasource as ds
import time
import json
from pymongo import MongoClient
from datetime import datetime


client=MongoClient('localhost',27017)
db=client['A8']
c=db['dataset']

label=0

def window1(temp):
    global label
    temp=json.loads(temp)
    h=temp['H']
    t=temp['T']
    r=temp['R']
    m=temp['M']
    pH=temp['pH']
    if(h>20 and h<40):
        label=0
    elif(h>40 and h<60):
        label=1
    elif(h>60 and h<80):
        label=2
    elif(h>80 and h<=100):
        label=3
    print('The values are {}, {}, {}, {}, {}, {}'.format(h,t,r,m,pH,label))
    window2(h,t,r,m,pH,label)
    
def window2(h,t,r,m,pH,label):
    k={}
    k['Humidity']=h
    k['Temperature']=t
    k['Rainfall']=r
    k['Moisture']=m
    k['pH']=pH
    k['label']=label
    k['timestamp']=str(datetime.now())
    c.insert_one(k)
    print('Data Inserted into Database')

while True:
    dataStream=ds.dataSource()
    time.sleep(4)
    window1(dataStream)

    