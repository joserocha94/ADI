import requests, sys, json, time
from init import HandleCode, app_errors, url_ws


gate_id = 0; 
gate_secret = 0;
data = {};

# verifica se gate existe
def validateGate(gate_id, gate_secret):

    try:

        data = {
            'gate_id' : gate_id,
            'gate_secret' : gate_secret
        }

        print(app_errors.get('APP_GENERIC_INIT'))
        response = requests.post(url_ws + 'ws/gate/secret', json=data)

        if HandleCode(response.status_code):
            if(response.text == "True"):
                print(app_errors.get('GATE_APP_SECRET_VALID'))
                validaUserCode()    
                adicionaAtivacao(gate_id, gate_secret)    
            else:
                print(app_errors.get('GATE_APP_SECRET_INVALID'))

        else:
            print(app_errors.get('GATE_APP_GENERIC_ERROR') + response.text)
            
    except:
        print(app_errors.get('GATE_APP_GENERIC_ERROR'))


# verifica se user code é válido
def validaUserCode():

    try:
        print(app_errors.get('APP_GENERIC_INIT'))
        msg = app_errors.get('GATE_APP_ASK_USERCODE')
        name = input(msg)

        data = {
            'usercode' : name
        }
        
        print(app_errors.get('APP_GENERIC_INIT'))
        response = requests.post(url_ws + 'ws/user/usercode', json=data)
        if HandleCode(response.status_code):
            if(response.text == "True"):
                print(app_errors.get('GATE_APP_USERCODE_VALID'))   
                print(app_errors.get('GATE_APP_GATE_CLOSING'))      
            else:
                print(app_errors.get('GATE_APP_USERCODE_INVALID'))

    except:
        print(app_errors.get('GATE_APP_GENERIC_ERROR'))


# adiciona utilização da gate
def adicionaAtivacao(gate_id, gate_secret):
    
    try:
        data = {
            'gate_id' : gate_id,
            'gate_secret' : gate_secret
        }

        response = requests.post(url_ws + 'ws/gate/activation', json=data)
        if (HandleCode(response.status_code) != True):
            print(app_errors.get('GATE_APP_GENERIC_ERROR'))                               

    except:
        print(app_errors.get('GATE_APP_GENERIC_ERROR'))


##########################################################
########################## MAIN ##########################
if __name__ == '__main__':

    gate_id = sys.argv[1]
    gate_secret = sys.argv[2]
    validateGate(gate_id, gate_secret)

