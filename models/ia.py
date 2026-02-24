from datetime import datetime
from extensions import db


class ReglaAutomatizacion(db.Model):
    __tablename__ = "reglas_automatizacion"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)

    modulo = db.Column(
        db.String(100)
    )  # crm, ventas, rrhh, etc.

    activo = db.Column(db.Boolean, default=True)

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    triggers = db.relationship(
        "Trigger",
        backref="regla",
        lazy=True
    )

    acciones = db.relationship(
        "Accion",
        backref="regla",
        lazy=True
    )
    
class Trigger(db.Model):
    __tablename__ = "triggers"

    id = db.Column(db.Integer, primary_key=True)

    regla_id = db.Column(
        db.Integer,
        db.ForeignKey("reglas_automatizacion.id"),
        nullable=False
    )

    tipo = db.Column(
        db.String(100)
    )  # evento, tiempo, condición

    evento = db.Column(
        db.String(150)
    )  # venta_creada, cliente_nuevo

    configuracion = db.Column(db.JSON)
    # filtros, campos, valores
    
class Accion(db.Model):
    __tablename__ = "acciones"

    id = db.Column(db.Integer, primary_key=True)

    regla_id = db.Column(
        db.Integer,
        db.ForeignKey("reglas_automatizacion.id"),
        nullable=False
    )

    tipo = db.Column(
        db.String(100)
    )  # email, whatsapp, tarea, webhook

    configuracion = db.Column(db.JSON)

    orden = db.Column(db.Integer, default=0)
    
class SugerenciaIA(db.Model):
    __tablename__ = "sugerencias_ia"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    modulo = db.Column(db.String(100))

    tipo = db.Column(
        db.String(100)
    )  # venta, cliente, riesgo

    entidad_id = db.Column(db.Integer)
    # cliente, venta, empleado, etc.

    mensaje = db.Column(db.Text)

    prioridad = db.Column(
        db.String(50)
    )  # alta, media, baja

    score = db.Column(db.Numeric(5, 2))

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    aceptada = db.Column(db.Boolean, default=False)
    
class Prediccion(db.Model):
    __tablename__ = "predicciones"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    tipo = db.Column(
        db.String(100)
    )  # ventas, churn, stock

    periodo = db.Column(db.String(50))

    datos = db.Column(db.JSON)
    # resultados, modelos, métricas

    confianza = db.Column(db.Numeric(5, 2))

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
