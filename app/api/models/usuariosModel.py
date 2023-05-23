from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuarios(db.Model):
    __tablename__ = 'tb_usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String)
    senha = db.Column(db.String)

    def __init__(self, usuario, senha):
        self.usuario = usuario
        self.senha = generate_password_hash(senha)

    def verify_password(self, senha):
        return check_password_hash(self.senha, senha)
    