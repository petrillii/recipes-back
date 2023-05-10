import traceback
from flask import Flask, request, jsonify,send_file
from app.api.resources import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import re
from flask_mail import Mail, Message
import zipfile
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin_erp:!fatec123@bd-trabalho-fabricio-fatecrp.postgres.database.azure.com/projeto_erp?sslmode=require"
db = SQLAlchemy(app)

# configuração do Flask-Mail para enviar e-mails
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'guilhemeappflow@gmail.com'
app.config['MAIL_PASSWORD'] = 'oghobneztdbikirt'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
mail = Mail(app)

class tb_user(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)

def validate_password(password):
    #mínimo 8 caracteres.
    if len(password) < 8:
        return False
    #mínimo 1 letra minuscula
    if not re.search(r"[a-z]", password):
        return False
    #mínimo 1 letra maiuscula
    if not re.search(r"[A-Z]", password):
        return False
    #mínimo 1 número
    if not re.search(r"\d", password):
        return False

    return True

@app.route('/')
def index():
    return 'Hello, world!'

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data["username"]
    email = data["email"]
    password = data["password"]
    confirm_password = data["confirm_password"]

    if password != confirm_password:
        return jsonify({
            "message": "A senha e a confirmação de senha não correspondem.",
            "statusCode": 400
        }), 400

    if not validate_password(password):
        return jsonify({
            "message": "A senha não atende aos requisitos mínimos.",
            "statusCode": 400
        }), 400

    user = tb_user()
    user.username = username
    user.email = email
    user.password = generate_password_hash(password)

    db.session.add(user)

    try:
        db.session.commit()  
        return jsonify({
        "message": "Cadastro bem-sucedido!",
        "statusCode": 201
        }), 201
    except Exception as error:
        print(error)
        return jsonify({
            "message": "Por algum motivo não conseguimos fazer o cadastro do usuário.",
            "statusCode": 500
        }), 500
    
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = tb_user.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({
            "message": "Credenciais inválidas.",
            "statusCode": 401
        }), 401

    return jsonify({
        "message": "Login bem-sucedido!",
        "statusCode": 200
    }), 200
 
@app.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data["email"]

    user = tb_user.query.filter_by(email=email).first()
    if not user:
        return jsonify({
            "message": "O e-mail fornecido não está cadastrado.",
            "statusCode": 404
        }), 404

    token = generate_password_hash(user.email)

    msg = Message("Redefinição de senha", sender="seu-email@example.com", recipients=[user.email])
    msg.body = f"Para redefinir sua senha, acesse o link: http://seusite.com/reset-password/{token}"
    mail.send(msg)

    return jsonify({
        "message": "Um e-mail de redefinição de senha foi enviado para o endereço fornecido.",
        "statusCode": 200
    }), 200

@app.route("/delete", methods=["DELETE"])
def delete_user_by_email():
    data = request.get_json()
    email = data["email"]

    user = tb_user.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "message": "Usuário não encontrado.",
            "statusCode": 404
        }), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "message": "Usuário deletado com sucesso.",
        "statusCode": 200
    }), 200

@app.route("/update", methods=["PUT"])
def update_user_by_email():
    data = request.get_json()
    email = data["email"]

    user = tb_user.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "message": "Usuário não encontrado.",
            "statusCode": 404
        }), 404

    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        password = data["password"]

        if not validate_password(password):
            return jsonify({
                "message": "A senha deve ter no mínimo 8 caracteres e conter pelo menos uma letra maiúscula, uma letra minúscula e um dígito numérico.",
                "statusCode": 400
            }), 400
        
        hashed_password = generate_password_hash(password)
        user.password = hashed_password

    db.session.commit()

    return jsonify({
        "message": "Informações do usuário atualizadas com sucesso.",
        "statusCode": 200
    }), 200

@app.route("/export-users", methods=["GET"])
def export_users():
    users = tb_user.query.all()
    users_data = []

    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        users_data.append(user_data)

    json_filename = "users.json"
    with open(json_filename, "w") as json_file:
        json.dump(users_data, json_file)

    zip_filename = "export.zip"
    table_name = tb_user.__tablename__
    export_folder = os.path.join(app.root_path, "export")
    zip_path = os.path.join(export_folder, zip_filename)

    with zipfile.ZipFile(zip_path, "w") as zip_file:
        zip_file.write(json_filename, f"{table_name}.json")

    os.remove(json_filename)

    return send_file(zip_path, mimetype="application/zip", as_attachment=True, attachment_filename=zip_filename)

if __name__ == '__main__':
    app.run(debug=True)
