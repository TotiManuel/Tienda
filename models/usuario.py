from datetime import datetime
from extensions import db

# ==============================
# USUARIO
# ==============================

class Usuario(db.Model):
    __tablename__ = "usuarios"
    # 🔹 Identificación
    id = db.Column(db.Integer, primary_key=True)
    # 🔹 Datos personales
    nombre = db.Column(db.String(120))
    apellido = db.Column(db.String(120))
    email = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(50))
    # 🔹 Autenticación
    password = db.Column(db.String(255), nullable=False)
    # 🔹 Configuración
    idioma = db.Column(db.String(10))
    # 🔹 Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
