from datetime import datetime
from extensions import db


class Reporte(db.Model):
    __tablename__ = "reportes"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    ) 

    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)

    tipo = db.Column(
        db.String(50)
    )  # ventas, crm, inventario, finanzas, rrhh

    configuracion = db.Column(db.JSON)
    # filtros, columnas, etc.

    formato = db.Column(
        db.String(20),
        default="tabla"
    )  # grafico, tabla, excel, pdf

    creado_por = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id")
    )

    programado = db.Column(db.Boolean, default=False)
    frecuencia = db.Column(
        db.String(50)
    )  # diario, semanal, mensual

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    activo = db.Column(db.Boolean, default=True)
    
class Metrica(db.Model):
    __tablename__ = "metricas"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    nombre = db.Column(db.String(150), nullable=False)

    descripcion = db.Column(db.Text)

    tipo = db.Column(
        db.String(50)
    )  # suma, promedio, conteo, tasa

    origen = db.Column(
        db.String(100)
    )  # ventas, crm, ecommerce, etc.

    configuracion = db.Column(db.JSON)
    # columnas, filtros, fórmulas

    publico = db.Column(db.Boolean, default=False)
    
class Dashboard(db.Model):
    __tablename__ = "dashboards"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    nombre = db.Column(db.String(150), nullable=False)

    descripcion = db.Column(db.Text)

    creado_por = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id")
    )

    publico = db.Column(db.Boolean, default=False)

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    widgets = db.relationship("Widget", backref="dashboard", lazy=True)
    
class Widget(db.Model):
    __tablename__ = "widgets"

    id = db.Column(db.Integer, primary_key=True)

    dashboard_id = db.Column(
        db.Integer,
        db.ForeignKey("dashboards.id"),
        nullable=False
    )

    metrica_id = db.Column(
        db.Integer,
        db.ForeignKey("metricas.id"),
        nullable=True
    )

    tipo = db.Column(
        db.String(50)
    )  # grafico_linea, barra, tabla, indicador

    configuracion = db.Column(db.JSON)

    posicion = db.Column(db.JSON)
    # x, y, width, height

    orden = db.Column(db.Integer, default=0)

    visible = db.Column(db.Boolean, default=True)
    
