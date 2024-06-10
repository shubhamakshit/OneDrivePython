import os
import requests
from urllib.parse import urlencode
from logger import Logger

log = Logger('log.txt')
os.environ['CLIENT_ID'] = '957cc50e-1bdc-45f2-82e1-8fb66bd99166'
os.environ['TENANT_ID'] = '7ad9d758-a664-44ae-b6d7-82eab1ba960d'
os.environ['CLIENT_SECRET'] = 'V538Q~vmaz8Nwa3btNqPkuWkSPkxMyxGA5pBQbmy'


# Retrieve the environment variables
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
tenant_id = os.getenv('TENANT_ID')


authority = f'https://login.microsoftonline.com/{tenant_id}'
base_url = 'https://graph.microsoft.com/v1.0'
endpoint = f'{base_url}/me'

def get_auth_url(scopes):

    SCOPES = scopes

    # authenticate using authorization code flow
    base_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize'
    params = {
        'client_id': f'{client_id}',
        'response_type': 'code',
        'redirect_uri': 'http://localhost:8000/callback',
        'response_mode': 'query',
        'scope': ' '.join(SCOPES)
    }
    return  f'{base_url}?{urlencode(params)}'

def get_token_url():
    return f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

def get_token(url,code,scopes,callback):
    import requests

    data = {
        'client_id': f"{client_id}",
        'grant_type': "authorization_code",
        'scope': " ".join(scopes),
        'code': f"{code}",
        'redirect_uri': f"{callback}"
    }

    response = requests.post(url, headers={}, data=data)
    log.log(f'Access token: {response.text}')
    if response.json():
        if 'access_token' in response.json():
            return {'access_token' : response.json()['access_token']}
        else:
            return {'error': response.json()}
    else:
        return {'error': 'Token not found/Invalid code'}

def getUserProfile(access_token):
    import url_handler as uh
    headers ={
        "Authorization": f"Bearer {access_token}"
    }

    log.log(f'Access token in getUser : {access_token}')
    response = requests.get(uh.USER_ENDPOINT, headers=headers)

    if response.json():
        return response.json()
    else:
        return {'error': 'User not found'}

def getChildrenInRoot(access_token):
    import url_handler as uh
    headers ={
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(uh.DRIVE_ROOT_ENDPOINT, headers=headers)
    if response.json():
        return response.json()
    else:
        return {'error': 'Children not found'}

def createUploadSession(access_token,file_name,folder_id="root"):
    createUploadSessionUrl = f"/me/drive/items/{folder_id}:/{file_name}:/createUploadSession"
    headers ={
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(f'{base_url}{createUploadSessionUrl}', headers=headers)

    if response.json():
        return response.json()
    else:
        return {'error': 'Upload session not created'}

def uploadBytesToUploadSession(access_token,upload_url,start,byte_data,total_bytes):
    headers = {
        "Content-Length": f"{len(byte_data)}",
        "Content-Range": f"bytes {start}-{start + len(byte_data) - 1}/{int(total_bytes)}",
    }

    data = byte_data

    response = requests.put(upload_url, headers=headers, data=data)

    if response.json():
        return response.json()
    else:
        return {'error': 'Upload failed'}

def getChildrenInFolder(access_token,folder_id):
    import url_handler as uh
    headers ={
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(uh.CONSTRUCT_DRIVE_URL(folder_id), headers=headers)

    log.log(f'Folder ID: {folder_id}')
    log.log(f'Access token in getChildrenInFolder: {access_token}')
    log.log(f'Response: {response.json()}')

    if response.json():
        return response.json()
    else:
        return {'error': 'Children not found'}
