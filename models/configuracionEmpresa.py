from datetime import datetime
from extensions import db

class ConfiguracionEmpresa(db.Model):
    __tablename__ = "configuracion_empresa"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    # 🔹 Clave-valor
    clave = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Text)

    # 🔹 Tipo de dato
    tipo = db.Column(db.String(50))  
    # texto, numero, booleano, json

    # 🔹 Categoría
    categoria = db.Column(db.String(100))  
    # facturacion, stock, crm, seguridad

    # 🔹 Descripción
    descripcion = db.Column(db.String(300))

    # 🔹 Sistema
    editable = db.Column(db.Boolean, default=True)
    visible = db.Column(db.Boolean, default=True)

    # 🔹 Auditoría
    actualizado_por = db.Column(db.Integer)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
class PreferenciaUsuario(db.Model):
    __tablename__ = "preferencias_usuario"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    # 🔹 Clave-valor
    clave = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Text)

    # 🔹 Tipo
    tipo = db.Column(db.String(50))

    # 🔹 Categoría
    categoria = db.Column(db.String(100))  
    # interfaz, notificaciones, panel

    # 🔹 UI
    visible = db.Column(db.Boolean, default=True)

    # 🔹 Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)