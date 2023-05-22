from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://seu_usuario:senha@localhost/seu_banco'
db = SQLAlchemy(app)

# Definição da classe que representa a tabela "tb_status_funcionario"
class StatusFuncionario(db.Model):
    _tablename_ = 'tb_status_funcionario'

    id_status_funcionario = db.Column(db.Integer, primary_key=True)
    descricao_status_funcionario = db.Column(db.String)


class Usuario(db.Model):
    _tablename_ = 'tb_usuario'

    id_usuario = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String)
    senha = db.Column(db.String)

# Definição da classe que representa a tabela "tb_funcionario"
class Funcionario(db.Model):
    _tablename_ = 'tb_funcionario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    sobrenome = db.Column(db.String)
    cpf = db.Column(db.String)
    data_nascimento = db.Column(db.Date)
    email = db.Column(db.String)
    telefone = db.Column(db.String)
    id_status_funcionario = db.Column(db.Integer, db.ForeignKey('tb_status_funcionario.id_status_funcionario'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('tb_usuario.id_usuario'))
    id_cargo = db.Column(db.Integer, db.ForeignKey('tb_cargo.id_cargo'))

    status_funcionario = db.relationship('StatusFuncionario', foreign_keys=[id_status_funcionario])

class Endereco(db.Model):
    _tablename_ = 'tb_endereco'

    id_endereco = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.Integer)
    cidade = db.Column(db.String)
    estado = db.Column(db.String)
    bairro = db.Column(db.String)
    complemento = db.Column(db.String)
    numero = db.Column(db.String)
    complemento_endereco = db.Column(db.String)
    observacao = db.Column(db.String)
    id_funcionario = db.Column(db.Integer), db.ForeignKey('tb_funcionario.id')

    funcionario = db.relationship('Funcionario', foreign_keys=[id])

class Cargo(db.Model):
    _tablename_ = 'tb_cargo'

    id_cargo = db.Column(db.String, primary_key=True)
    status = db.Column(db.String)
    descricao = db.Column(db.String)
    id_departamento = db.Column(db.Integer), db.ForeignKey('tb_departamento.id_departamento')
    departamento = db.relationship('Departamento', foreign_key=[id_departamento])

class Departamento(db.Model):
    _tablename_ = 'tb_departamento'

    sigla_departamento = id_cargo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    descricao = db.Column(db.String)

class Produto(db.Model):
    _tablename_ = 'tb_produto'

    id_produto = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String)
    descricao = db.Column(db.String)
    preco = db.Column(db.Integer) #Coloquei integer para tratar isso no front, ou a gente vê se tem alguma varáivel adequada para dinheiro, porque float tem aquele problema.
    quantidade = db.Column(db.Integer) #Outro que a gente precisa ver qual variável é mais adequada.

class Pagamento(db.Model):
    _tablename_ = 'tb_pagamento'

    id_forma_pagamento = db.Column(db.Integer, primary_key=True)
    descricao_pagamento = db.Column(db.String)

class cliente(db.Model):
    _tablename_ = 'tb_cliente'

    id_cliente = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String)
    cnpj = db.Column(db.String)
    email = db.Column(db.String)
    telefone = db.Column(db.String)
    id_status_cliente = db.Column(db.Integer, db.ForeignKey('tb_status_funcionario.id_status_funcionario'))
    id_endereco = db.Column(db.Integer, db.ForeignKey('tb_endereco.id_endereco'))

class StatusCliente(db.Model):
    _tablename_ = 'tb_status_cliente'

    id_status_cliente = db.Column(db.Integer, primary_key=True)
    descricao_status_cliente = db.Column(db.String)

class Fornecedor(db.Model):
    _tablename_ = 'tb_fornecedor'
    
    id_fornecedor = db.Column(db.Integer, primary_key=True)
    nome_fornecedor = db.Column(db.String)
    cnpj = db.Column(db.String)
    email = db.Column(db.String)
    telefone = db.Column(db.String)
    id_status_fornecedor = db.Column(db.Integer, db.ForeignKey('tb_status_fornecedor.id_status_fornecedor'))
    id_endereco = db.Column(db.Integer, db.ForeignKey('tb_endereco.id_endereco'))

class StatusFornecedor(db.Model):
    _tablename_ = 'tb_status_cliente'

    id_status_fornecedor = db.Column(db.Integer, primary_key=True)
    descricao_status_fornecedor = db.Column(db.String)

class Venda(db.Model):
    _tablename_ = 'tb_venda'

    id_venda = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(db.Integer, db.ForeignKey('tb_produto.id_produto'))
    quantidade = db.Column(db.Integer)
    data_venda = db.Column(db.Date)
    id_usuario = db.Column(db.Integer, db.ForeignKey('tb_usuario.id_usuario'))
    id_status = db.Column(db.Integer, db.ForeignKey('tb_produto.id_produto'))
    id_forma_pagamento = db.Column(db.Integer, db.ForeignKey('tb_pagamento.id_forma_pagamento'))
    id_cliente = db.Column(db.Integer, db.ForeignKey('tb_cliente.id_cliente'))

class StatusVenda(db.Modelo):
    _tablename_ = 'tb_status_venda'

    id_status_venda = db.Column(db.Integer, primary_key=True)
    status_venda = db.Column(db.String)

# Cria as tabelas no banco de dados, caso elas não existam
db.create_all()

if _name_ == '_main_':
    app.run()