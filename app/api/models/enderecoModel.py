from app import db

class Endereco(db.Model):
    _tablename_ = 'tb_endereco'

    id_endereco = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.Integer)
    logradouro = db.Column(db.String)
    cidade = db.Column(db.String)
    estado = db.Column(db.String)
    bairro = db.Column(db.String)
    complemento = db.Column(db.String)
    numero = db.Column(db.String)
    observacao = db.Column(db.String)


    funcionario = db.relationship('Funcionario', foreign_keys=[id])

    def __init__(self, id_endereco, cep, logradouro, cidade, estado, bairro, complemento, numero, observacao, id_funcionario):
        self.id_endereco = id_endereco
        self.cep = cep
        self.logradouro = logradouro
        self.cidade = cidade
        self.estado = estado
        self.bairro = bairro
        self.complemento = complemento
        self.numero = numero
        self.observacao = observacao