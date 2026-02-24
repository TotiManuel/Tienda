from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON
from extensions import db

class Proveedor(db.Model):
    __tablename__ = "proveedor"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)

    tipo = db.Column(db.String(50))
    # persona, empresa, fabricante, distribuidor

    documento = db.Column(db.String(50))
    email = db.Column(db.String(150))
    telefono = db.Column(db.String(50))

    direccion = db.Column(db.String(255))
    ciudad = db.Column(db.String(100))
    pais = db.Column(db.String(100))

    estado = db.Column(db.String(50), default="activo")

    contacto_principal = db.Column(db.String(150))

    condiciones_pago = db.Column(db.String(150))
    dias_credito = db.Column(db.Integer)

    notas = db.Column(db.Text)

    etiquetas = db.Column(JSON)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
class OrdenCompra(db.Model):
    __tablename__ = "orden_compra"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey("proveedor.id"), nullable=False)

    numero = db.Column(db.String(50), nullable=False)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_entrega_estimada = db.Column(db.DateTime)

    moneda = db.Column(db.String(10), default="ARS")
    tipo_cambio = db.Column(db.Float, default=1)

    subtotal = db.Column(db.Float, default=0)
    descuento_total = db.Column(db.Float, default=0)
    impuesto_total = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    estado = db.Column(db.String(50), default="borrador")
    # borrador, enviada, aprobada, recibida, cancelada

    notas = db.Column(db.Text)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class DetalleOrdenCompra(db.Model):
    __tablename__ = "detalle_orden_compra"

    id = db.Column(db.Integer, primary_key=True)

    orden_compra_id = db.Column(
        db.Integer, db.ForeignKey("orden_compra.id"), nullable=False
    )

    producto_id = db.Column(db.Integer, db.ForeignKey("producto.id"))

    descripcion = db.Column(db.String(255), nullable=False)

    cantidad = db.Column(db.Float, nullable=False)

    precio_unitario = db.Column(db.Float, nullable=False)

    descuento = db.Column(db.Float, default=0)
    impuesto = db.Column(db.Float, default=0)

    subtotal = db.Column(db.Float, nullable=False)
    
class FacturaProveedor(db.Model):
    __tablename__ = "factura_proveedor"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    proveedor_id = db.Column(db.Integer, db.ForeignKey("proveedor.id"), nullable=False)

    orden_compra_id = db.Column(db.Integer, db.ForeignKey("orden_compra.id"))

    numero = db.Column(db.String(50), nullable=False)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    fecha_vencimiento = db.Column(db.DateTime)

    moneda = db.Column(db.String(10), default="ARS")

    subtotal = db.Column(db.Float, default=0)
    impuestos = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

    estado = db.Column(db.String(50), default="pendiente")
    # pendiente, pagada, parcial

    datos_extra = db.Column(JSON)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class PagoProveedor(db.Model):
    __tablename__ = "pago_proveedor"

    id = db.Column(db.Integer, primary_key=True)

    factura_id = db.Column(
        db.Integer, db.ForeignKey("factura_proveedor.id"), nullable=False
    )

    metodo_pago_id = db.Column(db.Integer, db.ForeignKey("metodo_pago.id"))

    monto = db.Column(db.Float, nullable=False)

    referencia = db.Column(db.String(255))

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    estado = db.Column(db.String(50), default="confirmado")

