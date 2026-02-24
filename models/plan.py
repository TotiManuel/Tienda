from datetime import datetime
from extensions import db

class Plan(db.Model):
    __tablename__ = "planes"

    id = db.Column(db.Integer, primary_key=True)

    # 🔹 Información comercial
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(300))
    activo = db.Column(db.Boolean, default=True)
    visible = db.Column(db.Boolean, default=True)

    # 🔹 Precio
    precio_mensual = db.Column(db.Float, nullable=False)
    precio_anual = db.Column(db.Float)
    moneda = db.Column(db.String(10), default="USD")

    # 🔹 Límites
    limite_usuarios = db.Column(db.Integer)
    limite_empresas = db.Column(db.Integer)
    limite_almacenamiento_mb = db.Column(db.Integer)
    limite_sucursales = db.Column(db.Integer)

    # 🔹 Funcionalidades
    incluye_crm = db.Column(db.Boolean, default=False)
    incluye_stock = db.Column(db.Boolean, default=False)
    incluye_finanzas = db.Column(db.Boolean, default=False)
    incluye_web = db.Column(db.Boolean, default=False)
    incluye_ia = db.Column(db.Boolean, default=False)
    incluye_api = db.Column(db.Boolean, default=False)

    # 🔹 Configuración
    permite_personalizacion = db.Column(db.Boolean, default=False)
    soporte_prioritario = db.Column(db.Boolean, default=False)

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
class Suscripcion(db.Model):
    __tablename__ = "suscripciones"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey("planes.id"), nullable=False)

    # 🔹 Estado
    estado = db.Column(db.String(50))  
    # activa, trial, vencida, cancelada, suspendida

    # 🔹 Fechas
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime)
    proxima_facturacion = db.Column(db.DateTime)

    # 🔹 Facturación
    tipo_facturacion = db.Column(db.String(20))  
    # mensual, anual

    # 🔹 Trial
    trial_activo = db.Column(db.Boolean, default=False)
    fecha_fin_trial = db.Column(db.DateTime)

    # 🔹 Cancelación
    cancelada_por = db.Column(db.String(100))
    motivo_cancelacion = db.Column(db.String(300))

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
class Pago(db.Model):
    __tablename__ = "pagos"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"))
    suscripcion_id = db.Column(db.Integer, db.ForeignKey("suscripciones.id"))

    monto = db.Column(db.Float)
    moneda = db.Column(db.String(10))

    estado = db.Column(db.String(50))
    # pendiente, aprobado, rechazado, reembolsado

    metodo_pago = db.Column(db.String(50))
    proveedor_pago = db.Column(db.String(50))  
    # stripe, mercado_pago

    id_transaccion_externa = db.Column(db.String(200))

    fecha_pago = db.Column(db.DateTime)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
class FacturaSaaS(db.Model):
    __tablename__ = "facturas_saas"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"))
    suscripcion_id = db.Column(db.Integer, db.ForeignKey("suscripciones.id"))

    numero_factura = db.Column(db.String(100), unique=True)

    subtotal = db.Column(db.Float)
    impuestos = db.Column(db.Float)
    total = db.Column(db.Float)
    moneda = db.Column(db.String(10))

    estado = db.Column(db.String(50))  
    # emitida, pagada, vencida, anulada

    fecha_emision = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_vencimiento = db.Column(db.DateTime)

    url_pdf = db.Column(db.String(300))