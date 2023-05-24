from flask import request, jsonify,Flask
from werkzeug.security import generate_password_hash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import re
from app.__init__ import app
from app import db
from models.usuariosModel import Usuarios
from resources import usuariosResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin_erp:!fatec123@bd-trabalho-fabricio-fatecrp.postgres.database.azure.com/projeto_erp?sslmode=require"
db = SQLAlchemy(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'guilhemeappflow@gmail.com'
app.config['MAIL_PASSWORD'] = 'oghobneztdbikirt'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
mail = Mail(app)

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

@app.route('/usuarios/obter', methods=['GET'])
def usuarios():
    usuarios = usuariosResource.obter_usuarios()
    return jsonify(usuarios)

@app.route('/usuarios/<id>', methods=['GET'])
def user(id):
    user = usuariosResource.obter_usuario_por_id(id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'})

@app.route("/usuarios/cadastrar", methods=["POST"])
def cadastrar():
    data = request.get_json()
    return usuariosResource.cadastrar_usuario(data)

@app.route("/usuarios/login", methods=["POST"])
def login():
    data = request.get_json()
    return usuariosResource.login(data)

@app.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data["email"]

    user = Usuarios.query.filter_by(email=email).first()
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

    user = Usuarios.query.filter_by(email=email).first()

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

@app.route("usuario/update", methods=["PUT"])
def update_user_by_email():
    data = request.get_json()
    email = data["email"]

    user = Usuarios.query.filter_by(email=email).first()

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

