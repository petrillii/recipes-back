from app import db

class Produto(db.Model):
    _tablename_ = 'tb_produto'

    id_produto = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String)
    descricao = db.Column(db.String)
    preco = db.Column(db.Numeric(precision = 9, scale = 2)) 
    quantidade = db.Column(db.Numeric(precision = 9, scale = 2)) 

    def __init__(self, id_produto, nome_produto, descricao, preco, quantidade):
        self.id_produto = id_produto
        self.nome_produto = nome_produto
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade