# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 17:13:26 2021

@author: ARYAMAN
"""

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "IPaBSf1Wot6_h4V96vdPGcOgSlAq0tSiFO1ZB7cuE6b4"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": [["FULL_TIME_POSITION","PREVAILING_WAGE","YEAR","SOC_N"]], "values": [[1,193066,2016,15]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/435b1a86-eeea-428d-86e5-1bb8d392a672/predictions?version=2021-08-03', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
predictions = response_scoring.json()
output = predictions['predictions'][0]['values'][0][0]

if output==0:
    print('CERTIFIED')
elif output==1:
    print('CERTIFIED-WITHDRAWN')
elif output==2:
    print('DENIED')
elif output==3:
    print('WITHDRAWN')
elif output==4:
    print('PENDING QUALITY AND COMPLIANCE REVIEW - UNASSIGNED')
elif output==5:
    print('REJECTED')
elif output==6:
    print('INVALIDATED')