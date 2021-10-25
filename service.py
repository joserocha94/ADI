from re import I
from flask import request, jsonify
from datetime import datetime
from init import app, db, app_errors
from gate_data import Gate, gate_schema


usercode = 0
time = datetime.now()
isValid = True 


# get list of gates
@app.route('/gates', methods=['GET'])
def get_gates():

    try:
        q1 = db.session.query(Gate)
        total = str(q1.count())        
        for i in q1:
            print(str(i.ID) + " " + i.Location + " " + i.Secret + " " + str(i.Activation))

        return (jsonify(q1))
    
    except:
        return app_errors.get['APP_GENERIC_ERROR']


# delete every gate
@app.route("/ws/gate/reset", methods=['GET'])
def delete_gates():

    try:
        db.session.query(Gate).delete()
        return "0"
    except:
        return app_errors.get['APP_GENERIC_ERROR']   


# adds new gate
@app.route('/ws/gate', methods=['POST'])
def add_gate():

    try:
        Location = request.json['Location']
        Secret = request.json['Secret']
        Activation = request.json['Activation']

        new_gate = Gate(Location, Secret, Activation)
        db.session.add(new_gate)
        db.session.commit()

        return gate_schema.jsonify(new_gate)
    
    except:
        return app_errors.get['APP_GENERIC_ERROR']


# checks gate secret
@app.route('/ws/gate/secret', methods=['POST'])
def check_gate_secret():

    try:
        valido = False
        gate_id = request.json['gate_id']
        gate_secret = request.json['gate_secret']

        valido = (0 < db.session.query(Gate).filter(Gate.ID == gate_id, Gate.Secret == gate_secret).count())
    
        return (str(valido))

    except:
        return app_errors.get['APP_GENERIC_ERROR']


# creates new user code
@app.route('/ws/usercode', methods=['GET'])
def generate_usercode():

    try: 
        global usercode, time, isValid

        new_code = usercode + 1
        new_time = datetime.now()

        time = new_time
        usercode = new_code
        isValid = True

        return (jsonify(usercode))

    except:
        return app_errors.get['APP_GENERIC_ERROR']


# valida usercode enviado
@app.route('/ws/user/usercode', methods=['POST'])
def validates_usercode():

    try:
        global usercode, isValid, time
        valido = False
        usercode_sended = int(request.json['usercode'])

        if(usercode == 0 or not (isValid)):
            valido = False
        elif (usercode_sended == usercode and (time.now()-time).total_seconds() < 60):
            valido = True
            isValid = False
        else:
            valido = False

        return (str(valido))

    except:
        return app_errors.get['APP_GENERIC_ERROR']



# add activation
@app.route('/ws/gate/activation', methods=['POST'])
def update_gate_activations():

    try:
        gate_id = request.json['gate_id']
        gate_secret = request.json['gate_secret']

        used_gate = db.session.query(Gate).filter(Gate.ID == gate_id, Gate.Secret == gate_secret).first()
        used_gate.Activation += 1
        db.session.commit()

        return("Adicionado")

    except:
        return app_errors.get['APP_GENERIC_ERROR']


# main
if __name__ == '__main__':
    
    app.run(debug=True)
