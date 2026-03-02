from datetime import datetime
from extensions import db


class Empresa(db.Model):
    __tablename__ = "empresa"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)

    productos = db.relationship("Producto", backref="empresa", lazy=True)


class Producto(db.Model):
    __tablename__ = "producto"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    nombre = db.Column(db.String(200), nullable=False)
    codigo = db.Column(db.String(100))
    stock = db.Column(db.Integer, default=0)
    precio = db.Column(db.Float, default=0)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)