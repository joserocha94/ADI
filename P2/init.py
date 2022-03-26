from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.slite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


client_id = "851490151334140"
client_secret = "JeOIdogXEqZzWwYpW39CeP8HYzZToqZ+phmJhj6z6LFJbjIVWkbMYV37djn5Pi6Thpj/UNf6k5PsGMQyXQg5vQ=="
authorization_base_url = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog'
token_url = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'
my_user_fenix_id = "ist194304"


db = SQLAlchemy(app)
ma = Marshmallow(app)


url_ws = 'http://127.0.0.1:5000/'
url_awa = 'http://127.0.0.1:5001/'
url_ws_user = 'http://127.0.0.1:5002/'
url_ws_gate = 'http://127.0.0.1:5003/'


app_errors = {
    "APP_GENERIC_INIT" : 'Contacting server for...',
    "APP_GENERIC_ERROR" : 'ERRO. Operação não concluída',    
    "GATE_APP_SECRET_INVALID" : 'The secret is not valid for this gate. \nExiting…',
    "GATE_APP_SECRET_VALID" : 'The secret is valid for this gate',
    "GATE_APP_ASK_USERCODE" : 'Type the user code: ',
    "GATE_APP_USERCODE_VALID" : '!!! Code valid !!!',
    "GATE_APP_USERCODE_INVALID" : '!!! Code Not valid !!!',
    "GATE_APP_GATE_CLOSING" : '!!! The gate will close in 5s !!!',
    "USER_APP_CODE_RECEIVED" : 'Code Received',
    "USER_APP_TYPE_CODE" : 'Please type the code in the Gate',
    "USER_APP_INVALID_OPERATION" : 'Unable to generate code',
    "WAW_GATE_ADICIONADA" : 'Gate added',
    "WAW_GATE_NAO_ADICIONADA" : 'Gate not added',
}


def HandleCode(status_code):

    valido = True

    if (status_code >= 200 and status_code < 299):
        valido = True
    elif (status_code >= 400 and status_code < 499):
        valido = False
    elif (status_code >= 400 and status_code < 499):
        valido = False
    else:
        valido = False

    return valido