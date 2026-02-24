from datetime import datetime
from extensions import db


class Workflow(db.Model):
    __tablename__ = "workflows"

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
    )  # compras, rrhh, crm

    activo = db.Column(db.Boolean, default=True)

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
class Aprobacion(db.Model):
    __tablename__ = "aprobaciones"

    id = db.Column(db.Integer, primary_key=True)

    workflow_id = db.Column(
        db.Integer,
        db.ForeignKey("workflows.id"),
        nullable=False
    )

    entidad = db.Column(
        db.String(100)
    )  # orden_compra, contrato, etc.

    entidad_id = db.Column(db.Integer)

    estado = db.Column(
        db.String(50),
        default="pendiente"
    )  # aprobado, rechazado

    aprobado_por = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id")
    )

    fecha = db.Column(db.DateTime)

    comentario = db.Column(db.Text)
    
class NotasInternas(db.Model):
    __tablename__ = "notas_internas"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    modulo = db.Column(
        db.String(100)
    )

    entidad_id = db.Column(db.Integer)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id")
    )

    contenido = db.Column(db.Text)

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
class Comentarios(db.Model):
    __tablename__ = "comentarios"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    modulo = db.Column(db.String(100))

    entidad_id = db.Column(db.Integer)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id")
    )

    contenido = db.Column(db.Text)

    archivo_id = db.Column(
        db.Integer,
        db.ForeignKey("archivos.id")
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

class ChatInterno(db.Model):
    __tablename__ = "chat_interno"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    canal = db.Column(db.String(150))

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id")
    )

    mensaje = db.Column(db.Text)

    archivo_id = db.Column(
        db.Integer,
        db.ForeignKey("archivos.id")
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
class Encuesta(db.Model):
    __tablename__ = "encuestas"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    nombre = db.Column(db.String(150))

    descripcion = db.Column(db.Text)

    preguntas = db.Column(db.JSON)

    activa = db.Column(db.Boolean, default=True)

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
class FeedbackCliente(db.Model):
    __tablename__ = "feedback_clientes"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("cliente.id")
    )

    tipo = db.Column(
        db.String(100)
    )  # sugerencia, problema, elogio

    mensaje = db.Column(db.Text)

    prioridad = db.Column(
        db.String(50)
    )

    estado = db.Column(
        db.String(50),
        default="nuevo"
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
