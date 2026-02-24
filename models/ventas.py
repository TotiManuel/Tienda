from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import JSON

db = SQLAlchemy()

class Venta(db.Model):
    __tablename__ = "venta"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    numero = db.Column(db.String(50), nullable=False)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    moneda = db.Column(db.String(10), default="ARS")
    tipo_cambio = db.Column(db.Float, default=1)

    subtotal = db.Column(db.Float, default=0)
    descuento_total = db.Column(db.Float, default=0)
    impuesto_total = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    estado = db.Column(db.String(50), default="pendiente")
    # pendiente, pagada, anulada, parcial

    tipo_comprobante = db.Column(db.String(50))
    observaciones = db.Column(db.Text)

    datos_extra = db.Column(JSON)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class DetalleVenta(db.Model):
    __tablename__ = "detalle_venta"

    id = db.Column(db.Integer, primary_key=True)

    venta_id = db.Column(db.Integer, db.ForeignKey("venta.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("producto.id"))

    descripcion = db.Column(db.String(255), nullable=False)

    cantidad = db.Column(db.Float, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)

    descuento = db.Column(db.Float, default=0)
    impuesto = db.Column(db.Float, default=0)

    subtotal = db.Column(db.Float, nullable=False)
    
class Cotizacion(db.Model):
    __tablename__ = "cotizacion"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    numero = db.Column(db.String(50), nullable=False)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_vencimiento = db.Column(db.DateTime)

    subtotal = db.Column(db.Float, default=0)
    descuento_total = db.Column(db.Float, default=0)
    impuesto_total = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    estado = db.Column(db.String(50), default="borrador")
    # borrador, enviada, aceptada, rechazada, vencida

    notas = db.Column(db.Text)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class DetalleCotizacion(db.Model):
    __tablename__ = "detalle_cotizacion"

    id = db.Column(db.Integer, primary_key=True)

    cotizacion_id = db.Column(db.Integer, db.ForeignKey("cotizacion.id"), nullable=False)

    producto_id = db.Column(db.Integer, db.ForeignKey("producto.id"))

    descripcion = db.Column(db.String(255))
    cantidad = db.Column(db.Float)
    precio_unitario = db.Column(db.Float)

    descuento = db.Column(db.Float, default=0)
    impuesto = db.Column(db.Float, default=0)

    subtotal = db.Column(db.Float)
    
class MetodoPago(db.Model):
    __tablename__ = "metodo_pago"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50))
    # efectivo, tarjeta, transferencia, online

    activo = db.Column(db.Boolean, default=True)

    requiere_referencia = db.Column(db.Boolean, default=False)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class PagoVenta(db.Model):
    __tablename__ = "pago_venta"

    id = db.Column(db.Integer, primary_key=True)

    venta_id = db.Column(db.Integer, db.ForeignKey("venta.id"), nullable=False)
    metodo_pago_id = db.Column(db.Integer, db.ForeignKey("metodo_pago.id"))

    monto = db.Column(db.Float, nullable=False)

    referencia = db.Column(db.String(255))

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    estado = db.Column(db.String(50), default="confirmado")
    
class Devolucion(db.Model):
    __tablename__ = "devolucion"

    id = db.Column(db.Integer, primary_key=True)

    venta_id = db.Column(db.Integer, db.ForeignKey("venta.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))

    motivo = db.Column(db.Text)

    monto_total = db.Column(db.Float)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
class NotaCredito(db.Model):
    __tablename__ = "nota_credito"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)
    venta_id = db.Column(db.Integer, db.ForeignKey("venta.id"))

    numero = db.Column(db.String(50), nullable=False)

    monto = db.Column(db.Float, nullable=False)

    motivo = db.Column(db.Text)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    estado = db.Column(db.String(50), default="emitida")
    
