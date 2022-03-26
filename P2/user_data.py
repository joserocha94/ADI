from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from requests.sessions import session
from datetime import datetime
from sqlalchemy import exists

from init import db, ma

##########################################################
######################## Models ##########################

class UserEntryHistory(db.Model):

    __tablename__ = 'UserEntryhistory'

    #ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FenixID = db.Column(db.String(10), primary_key=True, nullable=False) 
    GateID = db.Column(db.Integer, nullable=False)
    Time = db.Column(db.DateTime, primary_key=True, nullable=False) 
    iValid = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "UserEntryHistory(id=%d dateTime=%d)" % (self.FenixID, self.GateID, self.Time, self.iValid)

    def __init__ (self, FenixID, GateID, Time, iValid):
        self.FenixID = FenixID
        self.GateID = GateID
        self.Time = Time
        self.iValid = iValid

class UserHistorySchema(ma.Schema):
    class Meta:
        fields = ('FenixID', 'GateID', 'Time', 'iValid')

user_history_schema = UserHistorySchema()


class User(db.Model):
    
    __tablename__ = 'User'

    FenixID  = db.Column(db.String(10), primary_key=True)
    Token = db.Column(db.String(400), nullable=False)
    UserCode  = db.Column(db.Integer, autoincrement=True, nullable=False)
    iAdmin = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "user(id=%d token=%d usercode=%d iAdmin=%d)" % (self.FenixID, self.UserCode, self.iAdmin)

    def __init__ (self, FenixID, Token, UserCode, iAdmin):
        self.FenixID = FenixID
        self.Token = Token
        self.UserCode = UserCode
        self.iAdmin = iAdmin

class UserSchema(ma.Schema):
    class Meta:
        fields = ('FenixID', 'Token', 'UserCode', 'iAdmin')

user_schema = UserSchema()


if __name__ == '__main__':
    db.create_all()