from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
print(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://sam:ksam8657@localhost/newsagg'


db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

app.config['SECRET_KEY']= '88d981b544da6ddbfbb1b967'

from newsagg import routes