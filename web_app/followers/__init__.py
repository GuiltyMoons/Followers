import os
import sys
from flask_sqlalchemy import SQLAlchemy

from flask import Flask

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
else:
    app = Flask(__name__)

app.config['SECRET_KEY'] = '112665d4a46cd2053a877d88dbd4fa5e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///followers.db'
db = SQLAlchemy(app)



#Create settings for user if not already existing
from followers.models import Settings
settings = Settings.query.all()
if not settings:
    db.session.add(Settings())
    db.session.commit()

from followers import routes
