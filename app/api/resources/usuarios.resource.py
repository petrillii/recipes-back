from flask import request, jsonify
from controllers import usuarios
from run import app

@app.route('/usuarios', methods=['GET'])
def usuarios():
    usuarios = usuarios.getAllUsuarios()
    return jsonify(usuarios)

@app.route('/usuarios/<id>', methods=['GET'])
def user(id):
    user = usuarios.getUserById(id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'})