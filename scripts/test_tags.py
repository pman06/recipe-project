import requests

TAG_LIST_ENDPOINT = 'http://127.0.0.1:8000/api/recipe/tags/'
TOKEN_ENDPOINT = 'http://127.0.0.1:8000/api/user/token/'


def authenticate_user(payload):
    """First authenticate user"""
    res = requests.post(TOKEN_ENDPOINT, payload)
    return res.json()['token']


def create_tag(data, headers):
    """Create tags"""
    res = requests.post(TAG_LIST_ENDPOINT, data=data, headers=headers)
    return res.json()


def list_tags(headers):
    """list created tags"""
    res = requests.get(TAG_LIST_ENDPOINT, headers=headers)
    return res.json()


payload = {'email': 'mynew@email.com',
           'password': 'mynewpass'
           }

token = authenticate_user(payload)
print(token)
headers = {}
headers['Authorization'] = 'Token ' + token

data = {'name': 'Breakfasts'}

print(create_tag(data, headers))

print(list_tags(headers))
