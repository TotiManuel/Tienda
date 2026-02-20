from app.database import db

class DetalleVenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey("venta.id"))
    producto_id = db.Column(db.Integer)
    nombre_producto = db.Column(db.String(100))
    precio = db.Column(db.Float)
    costo = db.Column(db.Float)
    cantidad = db.Column(db.Integer)
    subtotal = db.Column(db.Float)
    margen = db.Column(db.Float)
