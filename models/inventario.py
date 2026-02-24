from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON
from extensions import db

class CategoriaProducto(db.Model):
    __tablename__ = "categoria_producto"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)

    categoria_padre_id = db.Column(
        db.Integer, db.ForeignKey("categoria_producto.id")
    )

    activo = db.Column(db.Boolean, default=True)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class Producto(db.Model):
    __tablename__ = "producto"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)

    sku = db.Column(db.String(100), unique=True)

    codigo_barras = db.Column(db.String(100))

    categoria_id = db.Column(
        db.Integer, db.ForeignKey("categoria_producto.id")
    )

    tipo = db.Column(db.String(50), default="almacenable")
    # almacenable, servicio, consumible

    precio_compra = db.Column(db.Float)
    precio_venta = db.Column(db.Float)

    impuesto = db.Column(db.Float, default=0)

    stock_minimo = db.Column(db.Float, default=0)
    stock_maximo = db.Column(db.Float)

    permite_lote = db.Column(db.Boolean, default=False)
    permite_serie = db.Column(db.Boolean, default=False)

    activo = db.Column(db.Boolean, default=True)

    atributos_extra = db.Column(JSON)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class VarianteProducto(db.Model):
    __tablename__ = "variante_producto"

    id = db.Column(db.Integer, primary_key=True)

    producto_id = db.Column(
        db.Integer, db.ForeignKey("producto.id"), nullable=False
    )

    sku = db.Column(db.String(100), unique=True)

    atributos = db.Column(JSON)
    # {"color": "rojo", "talle": "L"}

    precio_extra = db.Column(db.Float, default=0)

    activo = db.Column(db.Boolean, default=True)
    
class AtributoProducto(db.Model):
    __tablename__ = "atributo_producto"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(100), nullable=False)

    valores = db.Column(JSON)
    # ["rojo", "azul", "verde"]
    
class ImagenProducto(db.Model):
    __tablename__ = "imagen_producto"

    id = db.Column(db.Integer, primary_key=True)

    producto_id = db.Column(
        db.Integer, db.ForeignKey("producto.id"), nullable=False
    )

    url = db.Column(db.String(500), nullable=False)

    orden = db.Column(db.Integer, default=0)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class Almacen(db.Model):
    __tablename__ = "almacen"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    nombre = db.Column(db.String(150), nullable=False)

    direccion = db.Column(db.String(255))

    activo = db.Column(db.Boolean, default=True)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class Ubicacion(db.Model):
    __tablename__ = "ubicacion"

    id = db.Column(db.Integer, primary_key=True)

    almacen_id = db.Column(
        db.Integer, db.ForeignKey("almacen.id"), nullable=False
    )

    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))

    activo = db.Column(db.Boolean, default=True)
    
class Lote(db.Model):
    __tablename__ = "lote"

    id = db.Column(db.Integer, primary_key=True)

    producto_id = db.Column(
        db.Integer, db.ForeignKey("producto.id"), nullable=False
    )

    numero_lote = db.Column(db.String(100), nullable=False)

    fecha_vencimiento = db.Column(db.Date)

    cantidad = db.Column(db.Float, default=0)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class Serie(db.Model):
    __tablename__ = "serie"

    id = db.Column(db.Integer, primary_key=True)

    producto_id = db.Column(
        db.Integer, db.ForeignKey("producto.id"), nullable=False
    )

    numero_serie = db.Column(db.String(150), unique=True)

    estado = db.Column(db.String(50), default="disponible")
    # disponible, vendido, devuelto, defectuoso

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
class MovimientoStock(db.Model):
    __tablename__ = "movimiento_stock"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    producto_id = db.Column(db.Integer, db.ForeignKey("producto.id"))

    almacen_origen_id = db.Column(db.Integer, db.ForeignKey("almacen.id"))
    almacen_destino_id = db.Column(db.Integer, db.ForeignKey("almacen.id"))

    ubicacion_id = db.Column(db.Integer, db.ForeignKey("ubicacion.id"))

    tipo = db.Column(db.String(50))
    # entrada, salida, transferencia, ajuste

    cantidad = db.Column(db.Float, nullable=False)

    lote_id = db.Column(db.Integer, db.ForeignKey("lote.id"))
    serie_id = db.Column(db.Integer, db.ForeignKey("serie.id"))

    referencia = db.Column(db.String(100))
    # venta_id, compra_id, ajuste_id

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    creado_por = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    
class AjusteStock(db.Model):
    __tablename__ = "ajuste_stock"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    motivo = db.Column(db.String(255))

    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    creado_por = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    
