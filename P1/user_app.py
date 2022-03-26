import requests
from init import HandleCode, app_errors, url_ws

def ask_code():

    try:

        print(app_errors.get('APP_GENERIC_INIT'))
        response = requests.get(url_ws + 'ws/usercode')
        
        if HandleCode(response.status_code):
            print(app_errors.get('USER_APP_CODE_RECEIVED'))
            print(">>> " + response.text.replace('\n','') + " <<<")
            print(app_errors.get('USER_APP_TYPE_CODE'))
        else:
            print(app_errors.get('USER_APP_INVALID_OPERATION') + response.text)

    except:
        print(app_errors.get('APP_GENERIC_ERROR'))


if __name__ == '__main__':
    
    ask_code()