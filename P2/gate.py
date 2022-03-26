from datetime import datetime
from flask import render_template, request, jsonify, session
from init import app, db, app_errors, my_user_fenix_id
from gate_data import Gate
from user_data import User, user_schema, UserEntryHistory, user_history_schema


# home
@app.route("/")
def run():
    try:
        return render_template('gate_index.html', flag = "False")
    except:
        return app_errors.get['APP_GENERIC_ERROR']



# get list of gates
@app.route('/gates', methods=['GET'])
def get_gates():

    try:
        q1 = db.session.query(Gate)
        
        for i in q1:
            print(str(i.ID) + " " + i.Location + " " + i.Secret + " " + str(i.Activation))

        return jsonify(q1.all())
    
    except:
        return app_errors.get['APP_GENERIC_ERROR']



# valide qrcode
@app.route('/qrcode', methods=['POST'])
def validaQRcode():

    try:

        usercode = request.json
        q1 = db.session.query(User).filter_by(UserCode = usercode)

        if (q1.count() > 0):
            addEntry(my_user_fenix_id, True)
            return "OK"
        else:
            addEntry("ist194304", False)
            return "NOK"

    except:
        return app_errors.get['APP_GENERIC_ERROR']



# add user entry
@app.route('/new-user-entry-history', methods=['POST'])
def addEntry(FenixID, iValid):

    try:

        new_user_entry_history = UserEntryHistory(FenixID, 1, datetime.now(), iValid)
        db.session.add(new_user_entry_history);
        db.session.commit();

        return jsonify("ok")

    except:
        return app_errors.get['APP_GENERIC_ERROR']   


# main
if __name__ == '__main__':

    app.run(host="localhost", port = 5003, debug=True)