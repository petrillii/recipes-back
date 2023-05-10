import traceback
from flask import Flask, request, jsonify
from app.api.resources import *
from werkzeug.security import generate_password_hash, check_password_hash
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

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    user = tb_user()
    user.email = data["email"]
    user.username = data["username"]
    user.password = generate_password_hash(data["password"])

    db.session.add(user)

    try:
        db.session.commit()  
        return jsonify({
            "username": user.username,
            "email": user.email,
            "password": user.password
        }), 201
    except Exception as error:
        print(error)
        traceback.print_exc()
        return jsonify({
            "message": "Por algum motivo não conseguimos fazer o cadastro do usuário.",
            "statusCode": 500
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
