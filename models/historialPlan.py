from datetime import datetime
from extensions import db

class HistorialPlan(db.Model):
    __tablename__ = "historial_planes"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"))
    plan_anterior_id = db.Column(db.Integer)
    plan_nuevo_id = db.Column(db.Integer)

    fecha_cambio = db.Column(db.DateTime, default=datetime.utcnow)
    motivo = db.Column(db.String(300))