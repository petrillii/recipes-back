from app import db

class Fornecedor(db.Model):
    _tablename_ = 'tb_fornecedor'
    
    id_fornecedor = db.Column(db.Integer, primary_key=True)
    nome_fornecedor = db.Column(db.String)
    cnpj = db.Column(db.String)
    email = db.Column(db.String)
    telefone = db.Column(db.String)
    id_status_fornecedor = db.Column(db.Integer, db.ForeignKey('tb_status_fornecedor.id_status_fornecedor'))
    id_endereco = db.Column(db.Integer, db.ForeignKey('tb_endereco.id_endereco'))

    status_forncedor = db.relationship('StatusFornecedor', foreign_keys = [id_status_fornecedor])
    endereco = db.relationship('Endereco', foreign_keys = [id_endereco])

    def __init__(self, id_fornecedor, nome_fornecedor, cnpj, email, telefone, id_status_fornecedor, id_endereco):
        self.id_fornecedor = id_fornecedor
        self.nome_fornecedor = nome_fornecedor
        self.cnpj = cnpj
        self.email = email
        self.telefone = telefone
        self.id_status_fornecedor = id_status_fornecedor
        self.id_endereco = id_endereco
        