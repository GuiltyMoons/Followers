from datetime import datetime

from followers import app, db

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    color_scheme = db.Column(db.String(), nullable=False, default='dark')

class Account(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    history = db.relationship('History', backref='owner', lazy=True)#connects a history to a user

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    followers = db.Column(db.Integer)
    following = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),nullable=False)#connects a stock to a user
