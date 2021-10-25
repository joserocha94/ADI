from flask import request, jsonify
from flask.templating import render_template
from init import app, db, app_errors
from gate_data import Gate


##########################################################
########################## API ###########################
@app.route("/api/awa")
def index():
    return render_template("index.html")   


@app.route("/api/awa/gates")
def listGates():
    try:
        q1 = db.session.query(Gate)
        for i in q1:
            print(str(i.ID) + " " + i.Location + " " + i.Secret + " " + str(i.Activation))

        return render_template("listGates.html", message=jsonify(q1))   
    
    except:
        return app_errors.get['APP_GENERIC_ERROR']


@app.route("/api/awa/gate")
def addGate():   
    try:
        return render_template("newGate.html")   
    
    except:
        return app_errors.get['APP_GENERIC_ERROR']


@app.route("/api/awa/gate", methods=['POST', 'GET'])
def addGate():
    try:
        gate_secret = request.form['gate_id']
        gate_location = request.form['gate_location']

        newGate = Gate(Location=gate_location, Secret=gate_secret, Activation=0)
        db.session.add(newGate)

        return app_errors.get['WAW_GATE_ADICIONADA']
    
    except:
        return app_errors.get['WAW_GATE_NAO_ADICIONADA']


##########################################################
########################## MAIN ##########################
if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 5001, debug=True)