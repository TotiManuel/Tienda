from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON
from extensions import db

class LogActividad(db.Model):
    __tablename__ = "log_actividad"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)
    usuarios_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    modulo_id = db.Column(db.Integer, db.ForeignKey("modulos.id"), nullable=True)
 
    accion = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)

    entidad = db.Column(db.String(100))
    entidad_id = db.Column(db.Integer)

    ip = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    dispositivo = db.Column(db.String(100))
    ubicacion_aproximada = db.Column(db.String(150))

    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)

    exito = db.Column(db.Boolean, default=True)

    datos_extra = db.Column(JSON)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<LogActividad {self.accion} - Usuario {self.usuario_id}>"
    
class Notificacion(db.Model):
    __tablename__ = "notificacion"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    tipo = db.Column(db.String(50), nullable=False)

    titulo = db.Column(db.String(255), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

    canal = db.Column(db.String(50), default="app")

    estado = db.Column(db.String(50), default="pendiente")

    prioridad = db.Column(db.String(20), default="media")

    url_destino = db.Column(db.String(255))

    fecha_envio = db.Column(db.DateTime)
    fecha_lectura = db.Column(db.DateTime)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def marcar_leida(self):
        self.estado = "leída"
        self.fecha_lectura = datetime.utcnow()

class HistorialCambios(db.Model):
    __tablename__ = "historial_cambios"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)

    entidad = db.Column(db.String(100), nullable=False)
    entidad_id = db.Column(db.Integer, nullable=False)

    campo = db.Column(db.String(100))

    valor_anterior = db.Column(db.Text)
    valor_nuevo = db.Column(db.Text)

    tipo_cambio = db.Column(db.String(50), nullable=False)

    motivo = db.Column(db.Text)

    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Cambio {self.entidad} {self.tipo_cambio}>"
    
class SesionUsuario(db.Model):
    __tablename__ = "sesion_usuario"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    token = db.Column(db.String(255), nullable=False)

    ip = db.Column(db.String(45))
    dispositivo = db.Column(db.String(150))

    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime)

    activo = db.Column(db.Boolean, default=True)
    
class AlertaSeguridad(db.Model):
    __tablename__ = "alerta_seguridad"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    tipo = db.Column(db.String(100))
    descripcion = db.Column(db.Text)

    gravedad = db.Column(db.String(20), default="media")

    resuelta = db.Column(db.Boolean, default=False)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
class ExportacionAuditoria(db.Model):
    __tablename__ = "exportacion_auditoria"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    tipo_exportacion = db.Column(db.String(100))
    formato = db.Column(db.String(50))

    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
def registrar_log(
    empresa_id,
    accion,
    usuario_id=None,
    descripcion=None,
    entidad=None,
    entidad_id=None,
    ip=None,
    exito=True,
    datos_extra=None,
):
    log = LogActividad(
        empresa_id=empresa_id,
        usuario_id=usuario_id,
        accion=accion,
        descripcion=descripcion,
        entidad=entidad,
        entidad_id=entidad_id,
        ip=ip,
        exito=exito,
        datos_extra=datos_extra,
    )

    db.session.add(log)
    db.session.commit()