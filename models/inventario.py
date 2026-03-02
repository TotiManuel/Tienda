from datetime import datetime
from extensions import db

class Producto(db.Model):
    __tablename__ = "producto"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    nombre = db.Column(db.String(200), nullable=False)
    codigo = db.Column(db.String(100))
    stock = db.Column(db.Integer, default=0)
    precio = db.Column(db.Float, default=0)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    empresa = db.relationship(
        "Usuario",
        back_populates="productos"
    )