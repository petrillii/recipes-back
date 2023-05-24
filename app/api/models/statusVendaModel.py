from app import db

class StatusVenda(db.Modelo):
    _tablename_ = 'tb_status_venda'

    id_status_venda = db.Column(db.Integer, primary_key=True)
    status_venda = db.Column(db.String)

    def __init__(self, id_status_venda, status_venda):
        self.id_status_venda = id_status_venda
        self.status_venda = status_venda