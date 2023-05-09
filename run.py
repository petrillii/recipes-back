from flask import Flask,request,jsonify
from app.api.resources import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin_erp:!fatec123@bd-trabalho-fabricio-fatecrp.postgres.database.azure.com/projeto_erp?sslmode=require"
db = SQLAlchemy(app)

class tb_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)

@app.route('/')
def index():
    return 'Hello, world!'

@app.route("/register",methods=["POST"])
def register():
    if request.methods == 'POST':
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        user = tb_user(
            username,
            email,
            password
        )
        db.session.add(user)
        db.session.commit()
        results = user.query.filter_by(email=email).first()
        return jsonify(results)
    
if __name__ == '__main__':
    app.run(debug=True)