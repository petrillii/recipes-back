from app import db

class Funcionario(db.Model):
    _tablename_ = 'tb_funcionario'

    id_funcionario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    sobrenome = db.Column(db.String)
    cpf = db.Column(db.String)
    data_nascimento = db.Column(db.Date)
    email = db.Column(db.String)
    telefone = db.Column(db.String)
    id_status_funcionario = db.Column(db.Integer, db.ForeignKey('tb_status_funcionario.id_status_funcionario'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('tb_usuarios.id_usuario'))
    sigla_cargo = db.Column(db.Integer, db.ForeignKey('tb_cargo.id_cargo'))
    id_endereco = db.Column(db.String, db.ForeignKey('tb_endereco.id_endereco'))

    status_funcionario = db.relationship('StatusFuncionario', foreign_keys=[id_status_funcionario])
    usuario = db.relationship('Usuarios', foreign_keys = [id_usuario])
    cargo = db.relationship('Cargo', foreign_keys = [sigla_cargo])
    endereco = db.relationship('Endereco', foreign_keys = [id_endereco])

    def __init__(self, id_funcionario, nome, sobrenome, cpf, data_nascimento, email, telefone, id_status_funcionario, id_usuario, sigla_cargo, id_endereco):
        self.id_funcionario = id_funcionario
        self.nome = nome
        self. sobrenome = sobrenome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.email = email
        self.telefone = telefone
        self.id_status_funcionario = id_status_funcionario
        self.id_usuario = id_usuario
        self.sigla_cargo = sigla_cargo
        self.id_endereco = id_endereco