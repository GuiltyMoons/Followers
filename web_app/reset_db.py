from followers.models import Account, History
from followers import db
from datetime import datetime

def reset():
    db.drop_all()
    db.create_all()

def testUser():
    account = Account(username="erickmeyer")
    db.session.add(account)
    db.session.commit()

def testHistory():
    account = Account(username="facebook")
    db.session.add(account)
    db.session.commit()

    db.session.add(History(date=datetime(2021, 3, 6),followers="630372", following="15", owner = account))
    db.session.add(History(date=datetime(2021, 3, 7),followers="630374", following="15", owner = account))
    db.session.add(History(date=datetime(2021, 3, 8),followers="630389", following="15", owner = account))
    db.session.add(History(date=datetime(2021, 3, 9),followers="630380", following="15", owner = account))
    db.session.add(History(date=datetime(2021, 3, 10),followers="630386", following="15", owner = account))
    db.session.add(History(date=datetime(2021, 3, 11),followers="630452", following="15", owner = account))
    db.session.add(History(date=datetime(2021, 3, 12),followers="630460", following="15", owner = account))
    db.session.add(History(date=datetime(2021, 3, 13),followers="630435", following="15", owner = account))
    db.session.add(History(date=datetime(2021, 3, 14),followers="630450", following="15", owner = account))
    db.session.add(History(date=datetime(2021, 3, 15),followers="630454", following="15", owner = account))
    db.session.commit()
