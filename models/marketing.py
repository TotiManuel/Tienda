from datetime import datetime
from extensions import db


class Campana(db.Model):
    __tablename__ = "campanas"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    nombre = db.Column(db.String(150), nullable=False)

    descripcion = db.Column(db.Text)

    tipo = db.Column(
        db.String(50)
    )  # email, whatsapp, sms, redes

    estado = db.Column(
        db.String(50),
        default="borrador"
    )  # activa, pausada, finalizada

    fecha_inicio = db.Column(db.DateTime)
    fecha_fin = db.Column(db.DateTime)

    presupuesto = db.Column(db.Numeric(12, 2))

    objetivo = db.Column(
        db.String(100)
    )  # leads, ventas, tráfico

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    emails = db.relationship("EmailMarketing", backref="campana", lazy=True)
    
class EmailMarketing(db.Model):
    __tablename__ = "email_marketing"

    id = db.Column(db.Integer, primary_key=True)

    campana_id = db.Column(
        db.Integer,
        db.ForeignKey("campanas.id"),
        nullable=False
    )

    asunto = db.Column(db.String(200))
    contenido = db.Column(db.Text)

    plantilla = db.Column(db.String(150))

    programado = db.Column(db.Boolean, default=False)
    fecha_envio = db.Column(db.DateTime)

    estado = db.Column(
        db.String(50),
        default="pendiente"
    )

    enviados = db.Column(db.Integer, default=0)
    abiertos = db.Column(db.Integer, default=0)
    clics = db.Column(db.Integer, default=0)
    
class Segmento(db.Model):
    __tablename__ = "segmentos"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    nombre = db.Column(db.String(150))

    descripcion = db.Column(db.Text)

    criterios = db.Column(db.JSON)
    # filtros: clientes, leads, compras, etc.

    publico = db.Column(db.Boolean, default=False)
    
class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    nombre = db.Column(db.String(150))
    email = db.Column(db.String(150))
    telefono = db.Column(db.String(50))

    origen = db.Column(
        db.String(100)
    )  # landing, ads, formulario

    estado = db.Column(
        db.String(50),
        default="nuevo"
    )  # contactado, calificado, convertido

    puntaje = db.Column(db.Numeric(5, 2))

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id")
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
class Formulario(db.Model):
    __tablename__ = "formularios"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    nombre = db.Column(db.String(150))

    descripcion = db.Column(db.Text)

    campos = db.Column(db.JSON)
    # nombre, email, teléfono, etc.

    activo = db.Column(db.Boolean, default=True)

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
class Landing(db.Model):
    __tablename__ = "landings"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    nombre = db.Column(db.String(150))

    url = db.Column(db.String(200))

    plantilla = db.Column(db.String(150))

    configuracion = db.Column(db.JSON)

    formulario_id = db.Column(
        db.Integer,
        db.ForeignKey("formularios.id")
    )

    activa = db.Column(db.Boolean, default=True)

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
