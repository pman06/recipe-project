import requests

END_POINT = 'http://127.0.0.1:8000/api/user/'
CREATE_USER_URL = END_POINT + 'create/'
ME_URL = END_POINT + 'me/'
TOKEN_URL = END_POINT + 'token/'


def create_sample_user(data):
    """Create a user in the database"""
    res = requests.post(CREATE_USER_URL, data=data)
    print(res.json())


def authenticate_user(data):
    """Authenticate created user"""
    res = requests.post(TOKEN_URL, data=data)
    print(res.json())
    return res.json()['token']


def update_user(data, headers):
    res = requests.put(ME_URL, headers=headers, data=data)
    print(res.json())


payload = {'email': 'mynew@email.com',
           'password': 'mynewpass',
           'name': 'Tunde'
           }

# create_sample_user(payload)
token = authenticate_user(payload)
print(token)
headers = {}
headers['Authorization'] = 'Token '+token

# update_user(payload,headers)
