from app import db


class cliente(db.Model):
    _tablename_ = 'tb_cliente'

    id_cliente = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String)
    cnpj = db.Column(db.String)
    email = db.Column(db.String)
    telefone = db.Column(db.String)
    id_status_cliente = db.Column(db.Integer, db.ForeignKey('tb_status_funcionario.id_status_funcionario'))
    id_endereco = db.Column(db.Integer, db.ForeignKey('tb_endereco.id_endereco'))

    status_cliente = db.relationship('StatusCliente', foreign_keys = [id_status_cliente])
    endereco = db.relationship('Endereco', foreign_keys = [id_endereco])

    def __init__(self, id_cliente, nome_cliente, cnpj, email, telefone, id_status_cliente, id_endereco):
        self.id_cliente = id_cliente
        self.nome_cliente = nome_cliente
        self.cnpj = cnpj
        self.email = email
        self.telefone = telefone
        self.id_status_cliente = id_status_cliente
        self.id_endereco = id_endereco