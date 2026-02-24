from datetime import datetime

from api.index import db

class EmpresaModulo(db.Model):
    __tablename__ = "empresas_modulos"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"), nullable=False)
    modulo_id = db.Column(db.Integer, db.ForeignKey("modulos.id"), nullable=False)

    # 🔹 Estado
    activo = db.Column(db.Boolean, default=True)

    # 🔹 Fechas
    fecha_activacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_desactivacion = db.Column(db.DateTime)

    # 🔹 Monetización
    precio_personalizado = db.Column(db.Float)
    incluido_en_plan = db.Column(db.Boolean, default=True)

    # 🔹 Límites
    limite_uso = db.Column(db.Integer)

    # 🔹 Configuración específica
    configuracion = db.Column(db.JSON)

    # 🔹 Auditoría
    activado_por = db.Column(db.Integer)
    motivo = db.Column(db.String(300))