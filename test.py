import flask
from flask import *
import url_handler as uh
import main
from drive_utils import OneDrive
from logger import Logger

log = Logger('log.txt')
app = Flask(__name__)



@app.route('/callback')
def callback():
    code = request.args.get('code')

    if code is None:
        return redirect('Callback invalid')

    # tk is the access token dict
    tk = get_token(code)
    if tk:
        if "access_token" in tk:

            # defining response object
            resp = make_response(redirect('/'))
            # setting the access token in the cookie
            resp.set_cookie('access_token', value=tk['access_token'])

            return resp

        else:
            return tk['error']
    else:
        return 'Token not found'


def get_token(code):
    return main.get_token(
        uh.TOKEN_URL,
        code,
        uh.DEFAULT_SCOPES,
        uh.CALLBACK_URL
    )


@app.route('/login')
def login():
    return redirect(uh.AUTHORIZE_URL)

def getUserProfile():
    access_token = request.cookies.get('access_token')
    response = main.getUserProfile(access_token)
    return response
@app.route('/')
def index():
    cookie = request.cookies.get('access_token')
    if cookie:
        data = getUserProfile()
        if 'error' in data:
            return data['error']
        name = data['displayName']
        return f'Hello {name}'
    else:
        return render_template("login.html")

@app.route('/folders')
def folders():
    access_token = request.cookies.get('access_token')
    response_json = main.getChildrenInRoot(access_token)

    if 'error' in response_json: return response_json

    return render_template('folders.html',folder_json={

        'folders': [folder['name'] for folder in OneDrive.getFolders_Only(response_json) ],
        'id': [folder['id'] for folder in OneDrive.getFolders_Only(response_json) ]

    })

@app.route('/test-upload')
def test_upload():
    return render_template("upload.html")

@app.route('/begin-upload')
def begin_upload():

    test_file = open('data.json', 'rb')
    response_json = main.getChildrenInRoot(request.cookies.get('access_token'))

    if 'error' in response_json: return response_json

    # return {
    #     'files': [file['name'] for file in OneDrive.getFiles_Only(response_json) ],
    #     'folders': [folder['name'] for folder in OneDrive.getFolders_Only(response_json) ]
    #
    # }

if __name__ == '__main__':
    app.run(port=8000, debug=True)
