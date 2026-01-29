from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    carrito_items = db.relationship("Carrito", backref="usuario", cascade="all, delete-orphan")
    ventas = db.relationship("Venta", backref="usuario", cascade="all, delete-orphan")

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)
class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    precio = db.Column(db.Float, nullable=False)
    imagen = db.Column(db.String(100))
    stock = db.Column(db.Integer, default=0)

    proveedor_id = db.Column(
        db.Integer,
        db.ForeignKey("proveedores.id"),
        nullable=False
    )
class Carrito(db.Model):
    __tablename__ = "carrito"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"))
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    producto = db.relationship("Producto")
class Venta(db.Model):
    __tablename__ = "ventas"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    turno_id = db.Column(db.Integer, db.ForeignKey("turnos_caja.id"))

    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    total = db.Column(db.Float, nullable=False)

    detalles = db.relationship(
        "DetalleVenta",
        backref="venta",
        cascade="all, delete-orphan"
    )

class DetalleVenta(db.Model):
    __tablename__ = "detalle_ventas"
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey("ventas.id"))
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"))
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    producto = db.relationship("Producto")
class Proveedor(db.Model):
    __tablename__ = "proveedores"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    email = db.Column(db.String(100))

    productos = db.relationship("Producto", backref="proveedor")
class Promocion(db.Model):
    __tablename__ = "promociones"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200))
    descuento = db.Column(db.Float)
class Configuracion(db.Model):
    __tablename__ = "configuracion"
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.String(200), nullable=False)
class TurnoCaja(db.Model):
    __tablename__ = "turnos_caja"

    id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    inicio = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fin = db.Column(db.DateTime, nullable=True)

    ventas = db.relationship("Venta", backref="turno")
