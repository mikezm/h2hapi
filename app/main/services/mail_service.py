import requests, os
from app.main.assets import activation_email_payload
from flask import json

def send_email(data):
    url = 'https://services.reachmail.net/EasySmtp/Advanced/{}'.format(os.environ.get('H2H_RM_ACCT_KEY'))
    request_headers = {
        'Authorization': 'Bearer {}'.format(os.environ.get('H2H_RM_TOKEN')),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url=url, json=data, headers=request_headers)
    return response.ok

def send_activation_email(email, token):
    activation_link = 'https://halfwaytohistory.com/user/activate?t={}'.format(token)
    personlization = {
        'To': {
            'Email': email
        },
        'Substitutions': {
            'activation_url': activation_link
        }
    }
    body = dict(activation_email_payload)
    body['Personalizations'].append(personlization)
    
    return send_email(body)