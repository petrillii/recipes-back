from app import db

class StatusCliente(db.Model):
    _tablename_ = 'tb_status_cliente'

    id_status_cliente = db.Column(db.Integer, primary_key=True)
    descricao_status_cliente = db.Column(db.String)

    def __init__(self, id_status_cliente, descricao_status_cliente):
        self.id_status_cliente = id_status_cliente
        self.descricao_status_cliente = descricao_status_cliente