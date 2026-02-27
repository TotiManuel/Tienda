from datetime import datetime
from werkzeug.security import generate_password_hash
from extensions import db

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120))
    apellido = db.Column(db.String(120))
    email = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(50))
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(120))
    idioma = db.Column(db.String(10))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
    empresa = db.Column(db.String(120))
    
    def set_password(self, password):
        self.password=generate_password_hash(password)
