from datetime import datetime
from extensions import db


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)

    productos = db.relationship("Producto", backref="categoria", lazy=True)


class Producto(db.Model):
    __tablename__ = "producto"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(200), nullable=False)
    codigo = db.Column(db.String(100), unique=True)

    stock = db.Column(db.Integer, default=0)
    precio = db.Column(db.Float, default=0)

    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"))

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)