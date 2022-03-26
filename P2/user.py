from datetime import datetime
from flask import Flask, render_template, redirect, request, session, url_for
from init import app, db, app_errors, authorization_base_url, token_url, client_id, client_secret, my_user_fenix_id
from user_data import UserEntryHistory, user_history_schema, User, user_schema
from requests_oauthlib import OAuth2Session
import os


# home
@app.route("/")
def run():
    try:     
        return render_template('user_index.html', flag = False, usercode = 0)
    except:
        return app_errors.get['APP_GENERIC_ERROR']


# gerar qrcode
@app.route("/qrcode")
def generateQRcode():
    try: 
        return render_template('user_QRcode.html')
    except:
        return app_errors.get['APP_GENERIC_ERROR']



# add entrada
@app.route('/user-entry-history')
def add_entry():

    try:      
        new_entry = UserEntryHistory(my_user_fenix_id, 1, datetime.now())
        db.session.add(new_entry)
        db.session.commit()
    
        return user_history_schema.jsonify(new_entry)

    except:
        return app_errors.get['APP_GENERIC_ERROR']



# get entrada
@app.route('/user-stats')
def stats():

    # passar userID
    try:
        q1 = db.session.query(UserEntryHistory)        
        string = ""

        for i in q1:
            string += str(i.FenixID) + " " + str(i.GateID) + " " + str(i.Time) + " ### "
            print(str(i.FenixID) + " " + str(i.GateID) + " " + str(i.Time))

        return string

    except:
        return app_errors.get['APP_GENERIC_ERROR']



# begin login
@app.route("/login", methods=["GET"])
def demo():

    github = OAuth2Session(client_id, redirect_uri="http://localhost:5000/callback")
    authorization_url, state = github.authorization_url(authorization_base_url)
    session['oauth_state'] = state

    return redirect(authorization_url)



# user has authorization
@app.route("/callback", methods=["GET"])
def callback():

    cliente = OAuth2Session(client_id, redirect_uri="http://localhost:5000/callback")
    token = cliente.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    github = OAuth2Session(client_id, token=token)
    user_info = github.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person').json()

    #guardar dados para a sessão
    session['oauth_token'] = token
    session['username'] = user_info["username"]
  
    new_token_access = session['oauth_token']['access_token']
    new_username = session['username'] 

    #atualizar token do utilizador + incrementa user_code
    try:
        q1 = db.session.query(User)
        user = q1.filter_by(FenixID = new_username).first()
        user.Token = new_token_access
        user.UserCode = user.UserCode+1
        db.session.commit()

        session['user_code'] = user.UserCode;
 
    except:
        return app_errors.get['APP_GENERIC_ERROR']  

    return redirect(url_for('.profile'))



# validate user
@app.route("/profile", methods=["GET"])
def profile():

    try:
        #verificar se o token esta associado ao username 
        current_user = db.session.query(User).filter(User.FenixID == session['username'], User.Token == session['oauth_token']['access_token'])
        if (current_user.count() > 0):
            return render_template('user_index.html', flag = True, usercode = session['user_code'])
        else:
            return render_template('user_index.html', flag = False, usercode = 0)

    except:
        return app_errors.get['APP_GENERIC_ERROR']  




# add user for testing
@app.route('/user', methods=['GET'])
def addUser():

    try:      
        new_user = User(
            'ist194304', 
            'NTcwMDIzNzY0Njg4MjAzOjJjOGJmNzYzNjIyMmRjMTUyNDIxOTFiMjY1Nzg3MmQ2ZDkwYWE4NjAxYjQ0ODQzNjJkNWZjZDIyNGM5NmMwNDNmZDA4MjA3NGJiNmZiYTA0YTY4OWNiY2I4Y2VmMDM4OGZjODY1NTU4MTU5ODAzMTNlNDk0NDY1NDY0YzU3ZTk3', 
            1, 
            False)

        db.session.add(new_user);
        db.session.commit();  
        return user_schema.jsonify(new_user);
    
    except:
        return app_errors.get['APP_GENERIC_ERROR']



# list all users for testing
@app.route('/user-list', methods=['GET'])
def getUsers():

    try:
        q1 = db.session.query(User)

        
        for i in q1:
            print(i.FenixID + " " + i.Token + " " + str(i.UserCode) + " " + str(i.iAdmin))

        return user_schema.jsonify(q1.all());
    
    except:
        return app_errors.get['APP_GENERIC_ERROR']     




if __name__ == '__main__':

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(24)
    app.run(host="localhost", port = 5000, debug=True)