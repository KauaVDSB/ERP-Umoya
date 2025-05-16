from app.extensions import db


item_categoria = db.Table(
    "item_categoria",
    db.Column(
        "item_id", db.Integer, db.ForeignKey("itens.id"), primary_key=True
    ),
    db.Column(
        "categoria_id",
        db.Integer,
        db.ForeignKey("categorias.id"),
        primary_key=True,
    ),
)


class Entidade(db.Model):
    __tablename__ = "entidades"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)


class Categoria(db.Model):
    __tablename__ = "categorias"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("categorias.id"))
    parent = db.relationship("Categoria", remote_side=[id])

    items = db.relationship(
        "Item", secondary=item_categoria, back_populates="categorias"
    )


class Item(db.Model):
    __tablename__ = "itens"
    id = db.Column(db.Integer, primary_key=True)

    codigo = db.Column(db.String(20), unique=True, nullable=False)
    codigo_barra = db.Column(db.String(50))

    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    imagem_url = db.Column(db.String(255))

    unidade = db.Column(db.String(5))
    peso = db.Column(db.Numeric(10, 3))
    comprimento = db.Column(db.Numeric(10, 3))
    largura = db.Column(db.Numeric(10, 3))
    profundidade = db.Column(db.Numeric(10, 3))

    entidade_id = db.Column(db.Integer, db.ForeignKey("entidades.id"))
    entidade = db.relationship("Entidade")

    categorias = db.relationship(
        "Categoria", secondary=item_categoria, back_populates="items"
    )
