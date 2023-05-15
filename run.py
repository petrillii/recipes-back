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

@app.route('/')
def index():
    return 'Hello, world!' 
 
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
