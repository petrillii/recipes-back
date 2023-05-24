from app import db

class StatusFornecedor(db.Model):
    _tablename_ = 'tb_status_cliente'

    id_status_fornecedor = db.Column(db.Integer, primary_key=True)
    descricao_status_fornecedor = db.Column(db.String)

    def __init__(self, id_status_fornecedor, descricao_status_fornecedor):
        self.id_status_fornecedor = id_status_fornecedor
        self.descricao_status_fornecedor = descricao_status_fornecedor