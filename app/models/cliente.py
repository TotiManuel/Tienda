from datetime import datetime
from app.database import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    direccion = db.Column(db.String(200))
    saldo_deuda = db.Column(db.Float, default=0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    ventas = db.relationship("Venta", backref="cliente", lazy=True)
    pagos = db.relationship("Pago", backref="cliente", lazy=True)
