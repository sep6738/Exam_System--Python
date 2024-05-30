from . import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(64), index=True, unique=True, nullable=False)
    passWord = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True, nullable=False)
    roleID = db.Column(db.Integer, nullable=False)