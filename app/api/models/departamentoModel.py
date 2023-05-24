from app import db

class Departamento(db.Model):
    _tablename_ = 'tb_departamento'

    sigla_departamento = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String)
    descricao = db.Column(db.String)

    def __init__(self, sigla_departamento, nome, descricao):
        self.sigla_departamento = sigla_departamento
        self.nome = nome
        self.descricao = descricao