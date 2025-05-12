from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(120), unique=True, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def set_password(self, raw: str):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password_hash, raw)


class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(255))

    pedidos = db.relationship("Pedido", backref="cliente", lazy=True)


class Produto(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=True)
    descricao = db.Column(db.Text)
    preco_unitaro = db.Column(db.Numeric(10, 2), nullable=False)  # 10 digitos, sendo 2 para casas decimais
    sku = db.Column(db.String(50), unique=True)

    itens = db.relationship("ItemPedido", backref="produto", lazy=True)
    estoque = db.relationship("Estoque", backref="produto", uselist=False)


class Pedido(db.Model):
    __tablename__ = "pedidos"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    status = db.Column(db.String(30), nullable=False, default="aberto")

    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"))
    itens = db.relationship("ItemPedido", backref="pedido", lazy=True)


class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"
    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)

    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)


class Estoque(db.Model):
    __tablename__ = "estoque"
    id = db.Column(db.Integer, primary_key=True)
    quantidade_disponivel = db.Column(db.Integer, nullable=False, default=0)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), unique=True, nullable=False)
