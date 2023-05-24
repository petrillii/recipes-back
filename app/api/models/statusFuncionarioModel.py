from app import db

class StatusFuncionario(db.Model):
    _tablename_ = 'tb_status_funcionario'

    id_status_funcionario = db.Column(db.Integer, primary_key=True)
    descricao_status_funcionario = db.Column(db.String)

    def __init__(self, id_status_funcionario, descricao_status_funcionario):
        self.id_status_funcionario = id_status_funcionario
        self.descricao_status_funcionario = descricao_status_funcionario