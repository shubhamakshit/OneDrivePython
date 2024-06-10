from main import get_auth_url, get_token_url
base_url = 'https://graph.microsoft.com/v1.0'

DEFAULT_SCOPES = [
    'User.Read',
    'User.Export.All',
    'files.readwrite',
    'offline_access',
    'Sites.FullControl.All'
]

def CONSTRUCT_DRIVE_URL(iten_id):
    return f'{base_url}/me/drive/items/{iten_id}/children'

AUTHORIZE_URL = get_auth_url(DEFAULT_SCOPES)
TOKEN_URL =  get_token_url()
CALLBACK_URL = 'http://localhost:8000/callback'
USER_ENDPOINT = f'{base_url}/me'
DRIVE_ENDPOINT = f'{base_url}/me/drive'
DRIVE_ROOT_ENDPOINT = f'{base_url}/me/drive/root/children'