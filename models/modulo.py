from datetime import datetime

from api.index import db

class Modulo(db.Model):
    __tablename__ = "modulos"

    id = db.Column(db.Integer, primary_key=True)

    # 🔹 Identificación
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    codigo = db.Column(db.String(100), unique=True, nullable=False)  
    # ej: ventas, crm, stock

    descripcion = db.Column(db.String(300))
    categoria = db.Column(db.String(100))  
    # ventas, marketing, finanzas

    # 🔹 Visual
    icono = db.Column(db.String(300))
    color = db.Column(db.String(20))

    # 🔹 Estado
    activo = db.Column(db.Boolean, default=True)
    visible = db.Column(db.Boolean, default=True)

    # 🔹 Monetización
    precio_mensual = db.Column(db.Float, default=0)
    precio_anual = db.Column(db.Float)
    es_premium = db.Column(db.Boolean, default=False)

    # 🔹 Planes compatibles
    requiere_plan = db.Column(db.Boolean, default=False)

    # 🔹 Dependencias
    depende_de = db.Column(db.String(100))  
    # ej: ecommerce depende de ventas

    # 🔹 Control de acceso
    requiere_permiso = db.Column(db.Boolean, default=True)

    # 🔹 Configuración avanzada
    tiene_configuracion = db.Column(db.Boolean, default=False)

    # 🔹 Marketplace
    es_publico = db.Column(db.Boolean, default=True)
    desarrollador = db.Column(db.String(200))

    # 🔹 Integraciones
    es_integracion = db.Column(db.Boolean, default=False)
    api_externa = db.Column(db.String(300))

    # 🔹 IA futura
    usa_ia = db.Column(db.Boolean, default=False)

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)