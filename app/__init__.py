from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin_erp:!fatec123@bd-trabalho-fabricio-fatecrp.postgres.database.azure.com/projeto_erp?sslmode=require"
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)