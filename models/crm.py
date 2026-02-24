from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON

from api.index import db

class Cliente(db.Model):
    __tablename__ = "cliente"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)
    apellido = db.Column(db.String(150))

    tipo = db.Column(db.String(50))  
    # persona, empresa, paciente, proveedor, etc.

    documento = db.Column(db.String(50))

    email = db.Column(db.String(150))
    telefono = db.Column(db.String(50))

    direccion = db.Column(db.String(255))
    ciudad = db.Column(db.String(100))
    pais = db.Column(db.String(100))

    fecha_nacimiento = db.Column(db.Date)

    estado = db.Column(db.String(50), default="activo")

    origen = db.Column(db.String(100))
    # web, whatsapp, referido, campaña, etc.

    valor_estimado = db.Column(db.Float)

    notas = db.Column(db.Text)

    etiquetas = db.Column(JSON)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Cliente {self.nombre}>"
    
class Contacto(db.Model):
    __tablename__ = "contacto"

    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)
    cargo = db.Column(db.String(150))

    email = db.Column(db.String(150))
    telefono = db.Column(db.String(50))

    es_principal = db.Column(db.Boolean, default=False)

    notas = db.Column(db.Text)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class SegmentoCliente(db.Model):
    __tablename__ = "segmento_cliente"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)

    criterios = db.Column(JSON)  
    # Ej: {"pais": "Argentina", "valor": ">1000"}

    activo = db.Column(db.Boolean, default=True)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class Interaccion(db.Model):
    __tablename__ = "interaccion"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    tipo = db.Column(db.String(50))
    # llamada, whatsapp, email, visita, etc.

    asunto = db.Column(db.String(255))
    descripcion = db.Column(db.Text)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    resultado = db.Column(db.String(100))

    adjuntos = db.Column(JSON)
    
class TareaCRM(db.Model):
    __tablename__ = "tarea_crm"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))
    oportunidad_id = db.Column(db.Integer, db.ForeignKey("oportunidad.id"))

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    titulo = db.Column(db.String(255))
    descripcion = db.Column(db.Text)

    prioridad = db.Column(db.String(50), default="media")

    fecha_vencimiento = db.Column(db.DateTime)

    estado = db.Column(db.String(50), default="pendiente")

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class Pipeline(db.Model):
    __tablename__ = "pipeline"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)

    activo = db.Column(db.Boolean, default=True)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class EtapaPipeline(db.Model):
    __tablename__ = "etapa_pipeline"

    id = db.Column(db.Integer, primary_key=True)

    pipeline_id = db.Column(db.Integer, db.ForeignKey("pipeline.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)

    orden = db.Column(db.Integer)

    probabilidad = db.Column(db.Float)

    activo = db.Column(db.Boolean, default=True)
    
class Oportunidad(db.Model):
    __tablename__ = "oportunidad"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))

    pipeline_id = db.Column(db.Integer, db.ForeignKey("pipeline.id"))
    etapa_id = db.Column(db.Integer, db.ForeignKey("etapa_pipeline.id"))

    nombre = db.Column(db.String(255), nullable=False)

    valor = db.Column(db.Float)

    moneda = db.Column(db.String(20), default="ARS")

    probabilidad = db.Column(db.Float)

    fecha_cierre_estimada = db.Column(db.DateTime)

    estado = db.Column(db.String(50), default="abierta")

    origen = db.Column(db.String(100))

    notas = db.Column(db.Text)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class Actividad(db.Model):
    __tablename__ = "actividad"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    tipo = db.Column(db.String(50))

    descripcion = db.Column(db.Text)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))
    oportunidad_id = db.Column(db.Integer, db.ForeignKey("oportunidad.id"))

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

