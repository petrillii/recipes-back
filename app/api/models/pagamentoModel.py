from app import db

class Pagamento(db.Model):
    _tablename_ = 'tb_pagamento'

    id_forma_pagamento = db.Column(db.Integer, primary_key=True)
    descricao_pagamento = db.Column(db.String)

    def __init__(self, id_forma_pagamento, descricao_pagamento):
        self.id_forma_pagamento = id_forma_pagamento
        self.descricao_pagamento = descricao_pagamento