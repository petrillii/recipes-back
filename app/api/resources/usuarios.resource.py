from flask import request, jsonify
from controllers import usuarios
from run import app

@app.route('/usuarios', methods=['GET'])
def usuarios():
    usuarios = usuarios.get_all_usuarios()
    return jsonify(usuarios)

@app.route('/usuarios/<id>', methods=['GET'])
def user(id):
    user = usuarios.get_user_by_id(id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'})