from flask import request, jsonify
from controllers import usuariosConstroller
from run import app

@app.route('/usuarios/obter', methods=['GET'])
def usuarios():
    usuarios = usuariosConstroller.obter_usuarios()
    return jsonify(usuarios)

@app.route('/usuarios/<id>', methods=['GET'])
def user(id):
    user = usuariosConstroller.obter_usuario_por_id(id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'})

@app.route("/usuarios/cadastrar", methods=["POST"])
def cadastrar():
    data = request.get_json()
    return usuariosConstroller.cadastrar_usuario(data)

@app.route("/usuarios/login", methods=["POST"])
def login():
    data = request.get_json()
    return usuariosConstroller.login(data)