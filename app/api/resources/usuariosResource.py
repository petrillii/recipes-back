from models import usuariosModel
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from werkzeug.security import check_password_hash

app = Flask(__name__)
db = SQLAlchemy(app)

def obter_todos_usuarios():
    users = usuariosModel.Usuarios.query.all()
    return [usuarios.to_dict() for usuarios in users]

def obter_usuario_por_id(id):
    user = usuariosModel.Usuarios.query.filter_by(id=id).first()
    if user:
        return user.to_dict()
    else:
        return None
    
def cadastrar_usuario(data):
    usuario = data["usuario"]
    senha = data["senha"]

    dbUsuario = usuariosModel.Usuarios(usuario, senha)
    db.session.add(dbUsuario)

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
        
def login(data):
    usuario = data["usuario"]
    senha = data["senha"]

    dbUsuario = usuariosModel.Usuarios.query.filter_by(usuario=usuario).first()
    if not dbUsuario or not check_password_hash(dbUsuario.senha, senha):
        return jsonify({
            "message": "Credenciais inválidas.",
            "statusCode": 401
        }), 401

    return jsonify({
        "message": "Login bem-sucedido!",
        "statusCode": 200
    }), 200
        
    