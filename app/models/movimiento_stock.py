# app/models/movimiento_stock.py
from datetime import datetime
from app import db

class MovimientoStock(db.Model):
    __tablename__ = "movimiento_stock"

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("producto.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # "Ingreso" o "Salida"
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con Producto
    producto = db.relationship("Producto", backref="movimientos_stock")
