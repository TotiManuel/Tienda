from datetime import datetime
from extensions import db
class Modulo(db.Model):
    __tablename__ = "modulos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    codigo = db.Column(db.String(100), unique=True, nullable=False)  
    descripcion = db.Column(db.String(300))
    categoria = db.Column(db.String(100))  
    icono = db.Column(db.String(300))
    color = db.Column(db.String(20))    