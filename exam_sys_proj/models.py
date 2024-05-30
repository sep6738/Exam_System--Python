
from exts import db
from datetime import datetime

class Users(db.Model):
    __tablename__ = "users"
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(255), nullable=False)
    passWord = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    roleID = db.Column(db.Integer, db.ForeignKey("role.roleID"), nullable=True)
    createAt = db.Column(db.DateTime, default=datetime.now)
    updateAt = db.Column(db.DateTime, default=datetime.now)
    email = db.Column(db.String(255), nullable=False, unique=True)
    verificationCode = db.Column(db.String(6), nullable=True)
    expirationDate = db.Column(db.DateTime, nullable=True)
    isActive = db.Column(db.Boolean, nullable=False)

class Role(db.Model):
    __tablename__ = "role"
    roleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roleName = db.Column(db.String(255), nullable=True)

class RegistrationCode(db.Model):
    __tablename__ = "registration_code"
    email = db.Column(db.String(255), nullable=False, primary_key=True)
    verificationCode = db.Column(db.String(6), nullable=True)
    expirationDate = db.Column(db.DateTime, nullable=True)
