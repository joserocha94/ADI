from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from requests.sessions import session
from datetime import datetime
from sqlalchemy import exists

from init import db, ma

##########################################################
######################## Models ##########################

class Gate(db.Model):

    __tablename__ = 'gate'

    ID  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Location = db.Column(db.String(100), nullable=False)
    Secret = db.Column(db.String(100), nullable=False)
    Activation = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Gate(id=%d location=%s secret=%s activation=%d)" % (self.ID, self.Location, self.Secret, self.Activation)

    def __init__ (self, Location, Secret, Activation):
        self.Location = Location
        self.Secret = Secret
        self.Activation = Activation

class GateSchema(ma.Schema):
    class Meta:
        fields = ('Location', 'Secret', 'Activation')

gate_schema = GateSchema()


##########################################################
########################## MAIN ##########################
#if __name__ == '__main__':
#    db.create_all()
#    app.run(debug=True)