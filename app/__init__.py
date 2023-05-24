from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from api.controllers import *
from flask_restful import Api
import config
from flask_cors import CORS

app=Flask(__name__)
api=Api(app)
cors=CORS(app,resources={r"/api/*": {"origins": "*"}})
db = SQLAlchemy(app)
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS

if __name__ == '__main__':
    app.run(debug=True)
