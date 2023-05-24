from app import db

class Venda(db.Model):
    _tablename_ = 'tb_venda'

    id_venda = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(db.Integer, db.ForeignKey('tb_produto.id_produto'))
    quantidade = db.Column(db.Integer)
    data_venda = db.Column(db.DateTime)
    id_usuario = db.Column(db.Integer, db.ForeignKey('tb_usuarios.id_usuario'))
    id_status_venda = db.Column(db.Integer, db.ForeignKey('tb_status_venda.id_status_venda'))
    id_forma_pagamento = db.Column(db.Integer, db.ForeignKey('tb_pagamento.id_forma_pagamento'))
    id_cliente = db.Column(db.Integer, db.ForeignKey('tb_cliente.id_cliente'))

    produto = db.relationship('Produto', foreign_keys = [id_produto])
    usuario = db.relationship('Usuarios', foreign_keys = [id_usuario])
    status_venda = db.relationship('StatusVenda', foreign_keys = [id_status_venda])
    forma_pagamento = db.relationship('Pagamento', foreign_keys = [id_forma_pagamento])
    cliente = db.relationship('Cliente', foreign_keys = [id_cliente])


    def __init__(self, id_venda, id_produto, quantidade, data_venda, id_usuario, id_status_venda, id_forma_pagamento, id_cliente):
        self.id_venda = id_venda
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.data_venda = data_venda
        self.id_usuario = id_usuario
        self.id_status_venda = id_status_venda
        self.id_forma_pagamento = id_forma_pagamento
        self.id_cliente = id_cliente