# models/venta.py

from extensions import db
from datetime import datetime

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    total = db.Column(db.Float, default=0)
    metodo_pago = db.Column(db.String(50))
    cliente = db.Column(db.String(120))

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    empresa_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    empresa = db.relationship("Usuario", backref="ventas")

    usuario_id = db.Column(db.Integer)  # quien registró la venta