# -*- coding: utf-8 -*-
"""
@author: ARYAMAN
"""

from flask import Flask, request, render_template

# create smtp session

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "IPaBSf1Wot6_h4V96vdPGcOgSlAq0tSiFO1ZB7cuE6b4"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

#lg_model=joblib.load('logreg.save')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/prediction')
def prediction():
    return render_template('index.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/prediction/y_predict',methods=['POST'])
def y_predict():
    x_test=[[x for x in request.form.values()]]
    print(x_test)
    #Job duration
    if x_test[0][0] == 'Full Time':
        x_test[0][0] = 1
    else:
        x_test[0][0] = 0
    
    print(x_test)
    #Soc_id
    if x_test[0][1] == 'Administrative':
        x_test[0][1] = 0
    elif x_test[0][1] == 'Agriculture':
        x_test[0][1] = 1
    elif x_test[0][1] == 'Audit':
        x_test[0][1] = 2
    elif x_test[0][1] == 'Database':
        x_test[0][1] = 3
    elif x_test[0][1] == 'Education':
        x_test[0][1] = 4
    elif x_test[0][1] == 'Estate':
        x_test[0][1] = 5
    elif x_test[0][1] == 'Executives':
        x_test[0][1] = 6
    elif x_test[0][1] == 'Finance':
        x_test[0][1] = 7
    elif x_test[0][1] == 'H.R':
        x_test[0][1] = 8
    elif x_test[0][1] == 'IT':
        x_test[0][1] = 9
    elif x_test[0][1] == 'Manager':
        x_test[0][1] = 10
    elif x_test[0][1] == 'Mechanical':
        x_test[0][1] = 11
    elif x_test[0][1] == 'Medical':
        x_test[0][1] = 12
    elif x_test[0][1] == 'P.R':
        x_test[0][1] = 13
    elif x_test[0][1] == 'Sales & Market':
        x_test[0][1] = 14
    elif x_test[0][1] == 'others':
        x_test[0][1] = 15
    
    #prediction = lg_model.predict(x_test)
    #print(prediction)
    #output = prediction[0]
    #print(output)
    print(x_test)
    
    payload_scoring = {"input_data": [{"field": [["FULL_TIME_POSITION","SOC_N","PREVAILING_WAGE","YEAR"]], "values": [[int(x_test[0][0]),int(x_test[0][1]),int(x_test[0][2]),int(x_test[0][3])]]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/435b1a86-eeea-428d-86e5-1bb8d392a672/predictions?version=2021-08-03', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    output = predictions['predictions'][0]['values'][0][0]
    
    if output==0:
        pred='CERTIFIED'
    elif output==1:
        pred='CERTIFIED-WITHDRAWN'
    elif output==2:
        pred='DENIED'
    elif output==3:
        pred='WITHDRAWN'
    elif output==4:
        pred='PENDING QUALITY AND COMPLIANCE REVIEW - UNASSIGNED'
    elif output==5:
        pred='REJECTED'
    elif output==6:
        pred='INVALIDATED'
    
    return render_template('index.html',prediction_text='{}'.format(pred))



if __name__=='__main__':
    app.run(debug=True)
    
# -*- coding: utf-8 -*-

