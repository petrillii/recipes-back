from app import db

class Cargo(db.Model):
    _tablename_ = 'tb_cargo'

    sigla_cargo = db.Column(db.String, primary_key=True)
    status = db.Column(db.String)
    descricao = db.Column(db.String)
    sigla_departamento = db.Column(db.Integer), db.ForeignKey('tb_departamento.id_departamento')
    
    departamento = db.relationship('Departamento', foreign_keys=[sigla_departamento])

    def __init__(self, sigla_cargo, status, descricao, sigla_deparmetanto):
        self.sigla_cargo = sigla_cargo
        self.status = status
        self.descricao = descricao
        self.sigla_departamento = sigla_deparmetanto