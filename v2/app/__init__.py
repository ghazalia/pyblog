from flask import Flask
from api import api
from commons import db, bcrypt

app = Flask(__name__)

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# initialize api
api.init_app(app)
db.init_app(app)
bcrypt.init_app(app)
