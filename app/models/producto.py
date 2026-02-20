from app.database import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Float)
    costo = db.Column(db.Float, default=0)
    stock = db.Column(db.Integer)
