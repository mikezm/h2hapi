import os

path = os.path.dirname(__file__)
from_address = 'contact@halfwaytohistory.com'
from_name = 'Halfway To History'


# peronsalizations use the Substituton key {{activation_url}}
activation_email_content = open(os.path.join(path, 'activation_email.html')).read().replace('\n', '')
activation_email_payload = {
    'Personalizations' : [],
    'From': {
        'Name': from_name,
        'Email': from_address
    },
    'ReplyTo': {
        'Name': from_name,
        'Email': from_address
    },
    'Contents': [
        {   
            'Type': 'text/html',
            'Content': activation_email_content
        }
    ],
    'Headers': {
        'x-dkim-options': 's=k1; i={}'.format(from_address)
    },
    'Subject': 'Activate your HalfwayToHistory User Account'
}