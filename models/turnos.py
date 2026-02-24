from datetime import datetime, time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import JSON

db = SQLAlchemy()

class Calendario(db.Model): 
    __tablename__ = "calendario"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)

    tipo = db.Column(db.String(50))
    # personal, equipo, sala, general

    color = db.Column(db.String(20))

    activo = db.Column(db.Boolean, default=True)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class Evento(db.Model):
    __tablename__ = "evento"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    calendario_id = db.Column(
        db.Integer, db.ForeignKey("calendario.id"), nullable=False
    )

    titulo = db.Column(db.String(200), nullable=False)

    descripcion = db.Column(db.Text)

    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)

    todo_el_dia = db.Column(db.Boolean, default=False)

    color = db.Column(db.String(20))

    ubicacion = db.Column(db.String(255))

    datos_extra = db.Column(JSON)

    creado_por = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class Recurso(db.Model):
    __tablename__ = "recurso"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)

    tipo = db.Column(db.String(50))
    # profesional, sala, equipo

    especialidad = db.Column(db.String(150))

    activo = db.Column(db.Boolean, default=True)

    datos_extra = db.Column(JSON)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class Disponibilidad(db.Model):
    __tablename__ = "disponibilidad"

    id = db.Column(db.Integer, primary_key=True)

    recurso_id = db.Column(
        db.Integer, db.ForeignKey("recurso.id"), nullable=False
    )

    dia_semana = db.Column(db.Integer)
    # 0 lunes, 6 domingo

    hora_inicio = db.Column(db.Time)
    hora_fin = db.Column(db.Time)

    intervalo_minutos = db.Column(db.Integer, default=30)

    activo = db.Column(db.Boolean, default=True)
    
class Turno(db.Model):
    __tablename__ = "turno"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))

    recurso_id = db.Column(db.Integer, db.ForeignKey("recurso.id"))

    calendario_id = db.Column(db.Integer, db.ForeignKey("calendario.id"))

    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)

    estado = db.Column(db.String(50), default="pendiente")
    # pendiente, confirmado, atendido, cancelado, no_asistio

    servicio = db.Column(db.String(150))

    precio = db.Column(db.Float)

    notas = db.Column(db.Text)

    recordatorio_enviado = db.Column(db.Boolean, default=False)

    creado_por = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
