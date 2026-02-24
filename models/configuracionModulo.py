from datetime import datetime

from api.index import db

class ConfiguracionModulo(db.Model):
    __tablename__ = "configuracion_modulos"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer)
    modulo_id = db.Column(db.Integer)

    clave = db.Column(db.String(100))
    valor = db.Column(db.Text)

    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)