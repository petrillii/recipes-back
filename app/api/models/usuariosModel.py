from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Usuarios(db.Model, UserMixin):
    __tablename__ = 'tb_usuarios'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    usuario = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True)
    senha = db.Column(db.String(128), nullable=False)

    def __init__(self, usuario, email, senha):
        self.usuario = usuario
        self.email = email
        self.senha = generate_password_hash(senha)

    def verify_password(self, pwd):
        return check_password_hash(self.senha, pwd)