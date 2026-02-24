from datetime import datetime
from extensions import db
import secrets



class Integracion(db.Model):
    __tablename__ = "integraciones"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    nombre = db.Column(db.String(150), nullable=False)

    tipo = db.Column(
        db.String(100)
    )
    # stripe, mercado_pago, whatsapp, afip, zapier, custom

    proveedor = db.Column(db.String(150))

    configuracion = db.Column(db.JSON)
    # tokens, secretos, endpoints

    activa = db.Column(db.Boolean, default=True)

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    ultimo_sync = db.Column(db.DateTime)

    estado = db.Column(
        db.String(50),
        default="conectado"
    )
    # conectado, error, pendiente
    
class APIKey(db.Model):
    __tablename__ = "api_keys"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    nombre = db.Column(db.String(150))

    key = db.Column(db.String(255), unique=True, nullable=False)

    permisos = db.Column(db.JSON)
    # lectura, escritura, crm, ventas, etc.

    activa = db.Column(db.Boolean, default=True)

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    ultimo_uso = db.Column(db.DateTime)

    def generar_key(self):
        self.key = secrets.token_urlsafe(32)
        
class Webhook(db.Model):
    __tablename__ = "webhooks"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    url = db.Column(db.String(300), nullable=False)

    evento = db.Column(
        db.String(150)
    )
    # venta_creada, cliente_nuevo, turno_cancelado

    secreto = db.Column(db.String(255))

    activo = db.Column(db.Boolean, default=True)

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    ultimo_envio = db.Column(db.DateTime)

    estado = db.Column(
        db.String(50),
        default="activo"
    )
    
class EventoIntegracion(db.Model):
    __tablename__ = "eventos_integracion"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresa.id"),
        nullable=False
    )

    tipo = db.Column(
        db.String(100)
    )
    # enviado, recibido

    origen = db.Column(
        db.String(150)
    )
    # stripe, webhook, api

    evento = db.Column(db.String(150))

    payload = db.Column(db.JSON)

    respuesta = db.Column(db.JSON)

    estado = db.Column(
        db.String(50),
        default="pendiente"
    )
    # exitoso, error

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
