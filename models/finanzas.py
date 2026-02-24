from datetime import datetime
from extensions import db

class CuentaContable(db.Model):
    __tablename__ = "cuenta_contable"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    codigo = db.Column(db.String(50), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)

    tipo = db.Column(db.String(50))
    # activo, pasivo, patrimonio, ingreso, gasto

    cuenta_padre_id = db.Column(
        db.Integer, db.ForeignKey("cuenta_contable.id")
    )

    nivel = db.Column(db.Integer)

    permite_movimientos = db.Column(db.Boolean, default=True)

    moneda = db.Column(db.String(10), default="ARS")

    activo = db.Column(db.Boolean, default=True)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class Transaccion(db.Model):
    __tablename__ = "transaccion"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    tipo = db.Column(db.String(50))
    # ingreso, egreso, transferencia

    referencia = db.Column(db.String(100))
    # venta, compra, pago, etc.

    moneda = db.Column(db.String(10), default="ARS")

    monto = db.Column(db.Float, nullable=False)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    descripcion = db.Column(db.Text)

    creado_por = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    
class LibroDiario(db.Model):
    __tablename__ = "libro_diario"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)

    tipo = db.Column(db.String(50))
    # ventas, compras, general, banco

    activo = db.Column(db.Boolean, default=True)
    
class Asiento(db.Model):
    __tablename__ = "asiento"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    libro_id = db.Column(db.Integer, db.ForeignKey("libro_diario.id"))

    numero = db.Column(db.String(50))

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    descripcion = db.Column(db.Text)

    referencia = db.Column(db.String(100))

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class DetalleAsiento(db.Model):
    __tablename__ = "detalle_asiento"

    id = db.Column(db.Integer, primary_key=True)

    asiento_id = db.Column(db.Integer, db.ForeignKey("asiento.id"), nullable=False)

    cuenta_id = db.Column(db.Integer, db.ForeignKey("cuenta_contable.id"))

    debe = db.Column(db.Float, default=0)
    haber = db.Column(db.Float, default=0)

    moneda = db.Column(db.String(10), default="ARS")

    centro_costo_id = db.Column(db.Integer, db.ForeignKey("centro_costo.id"))

    descripcion = db.Column(db.String(255))

class Impuesto(db.Model):
    __tablename__ = "impuesto"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)

    porcentaje = db.Column(db.Float, nullable=False)

    tipo = db.Column(db.String(50))
    # IVA, retención, etc.

    activo = db.Column(db.Boolean, default=True)
    
class CentroCosto(db.Model):
    __tablename__ = "centro_costo"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)

    descripcion = db.Column(db.Text)

    activo = db.Column(db.Boolean, default=True)
    
class FlujoCaja(db.Model):
    __tablename__ = "flujo_caja"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    tipo = db.Column(db.String(50))
    # ingreso, egreso

    categoria = db.Column(db.String(150))

    monto = db.Column(db.Float, nullable=False)

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    referencia = db.Column(db.String(100))

    creado_por = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    
class Presupuesto(db.Model):
    __tablename__ = "presupuesto"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)

    periodo = db.Column(db.String(50))
    # mensual, anual

    moneda = db.Column(db.String(10), default="ARS")

    monto_total = db.Column(db.Float)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class DetallePresupuesto(db.Model):
    __tablename__ = "detalle_presupuesto"

    id = db.Column(db.Integer, primary_key=True)

    presupuesto_id = db.Column(
        db.Integer, db.ForeignKey("presupuesto.id"), nullable=False
    )

    cuenta_id = db.Column(db.Integer, db.ForeignKey("cuenta_contable.id"))

    monto = db.Column(db.Float)

    centro_costo_id = db.Column(db.Integer, db.ForeignKey("centro_costo.id"))
    
