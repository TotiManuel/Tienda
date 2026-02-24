from datetime import datetime
from api.index import db

class PaginaWeb(db.Model):
    __tablename__ = "paginas_web"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    plantilla_id = db.Column(
        db.Integer,
        db.ForeignKey("plantillas.id")
    )

    activo = db.Column(db.Boolean, default=True)

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relaciones
    secciones = db.relationship("Seccion", backref="pagina", lazy=True)
    dominios = db.relationship("Dominio", backref="pagina", lazy=True)
    blog = db.relationship("Blog", backref="pagina", uselist=False)
    ecommerce = db.relationship("Ecommerce", backref="pagina", uselist=False)
    
class Seccion(db.Model):
    __tablename__ = "secciones"

    id = db.Column(db.Integer, primary_key=True)

    pagina_id = db.Column(
        db.Integer,
        db.ForeignKey("paginas_web.id"),
        nullable=False
    )

    nombre = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150))

    orden = db.Column(db.Integer, default=0)

    visible = db.Column(db.Boolean, default=True)

    bloques = db.relationship("Bloque", backref="seccion", lazy=True)
    
class Bloque(db.Model):
    __tablename__ = "bloques"

    id = db.Column(db.Integer, primary_key=True)

    seccion_id = db.Column(
        db.Integer,
        db.ForeignKey("secciones.id"),
        nullable=False
    )

    tipo = db.Column(db.String(100))
    # ejemplo: texto, imagen, galeria, formulario, video

    contenido = db.Column(db.JSON)

    orden = db.Column(db.Integer, default=0)

    visible = db.Column(db.Boolean, default=True)
    
class Plantilla(db.Model):
    __tablename__ = "plantillas"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)

    preview = db.Column(db.String(300))

    css = db.Column(db.Text)
    configuracion = db.Column(db.JSON)

    premium = db.Column(db.Boolean, default=False)
    
class Dominio(db.Model):
    __tablename__ = "dominios"

    id = db.Column(db.Integer, primary_key=True)

    pagina_id = db.Column(
        db.Integer,
        db.ForeignKey("paginas_web.id"),
        nullable=False
    )

    dominio = db.Column(db.String(200), nullable=False)

    verificado = db.Column(db.Boolean, default=False)

    ssl_activo = db.Column(db.Boolean, default=False)
    
class SEO(db.Model):
    __tablename__ = "seo"

    id = db.Column(db.Integer, primary_key=True)

    pagina_id = db.Column(
        db.Integer,
        db.ForeignKey("paginas_web.id"),
        nullable=False
    )

    titulo = db.Column(db.String(200))
    descripcion = db.Column(db.String(300))

    palabras_clave = db.Column(db.String(300))

    og_imagen = db.Column(db.String(300))
    
class Blog(db.Model):
    __tablename__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)

    pagina_id = db.Column(
        db.Integer,
        db.ForeignKey("paginas_web.id"),
        nullable=False
    )

    activo = db.Column(db.Boolean, default=True)

    entradas = db.relationship("EntradaBlog", backref="blog", lazy=True)
    
class EntradaBlog(db.Model):
    __tablename__ = "entradas_blog"

    id = db.Column(db.Integer, primary_key=True)

    blog_id = db.Column(
        db.Integer,
        db.ForeignKey("blogs.id"),
        nullable=False
    )

    titulo = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200))

    contenido = db.Column(db.Text)

    imagen = db.Column(db.String(300))

    publicado = db.Column(db.Boolean, default=False)

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
class Ecommerce(db.Model):
    __tablename__ = "ecommerce"

    id = db.Column(db.Integer, primary_key=True)

    pagina_id = db.Column(
        db.Integer,
        db.ForeignKey("paginas_web.id"),
        nullable=False
    )

    activo = db.Column(db.Boolean, default=True)

    pedidos = db.relationship("Pedido", backref="ecommerce", lazy=True)
    
class Carrito(db.Model):
    __tablename__ = "carritos"

    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id")
    )

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    activo = db.Column(db.Boolean, default=True)

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)

    ecommerce_id = db.Column(
        db.Integer,
        db.ForeignKey("ecommerce.id"),
        nullable=False
    )

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id")
    )

    estado = db.Column(
        db.String(50),
        default="pendiente"
    )

    total = db.Column(db.Numeric(10, 2))

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    detalles = db.relationship("DetallePedido", backref="pedido", lazy=True)
    
class DetallePedido(db.Model):
    __tablename__ = "detalle_pedido"

    id = db.Column(db.Integer, primary_key=True)

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id"),
        nullable=False
    )

    producto_id = db.Column(
        db.Integer,
        db.ForeignKey("productos.id"),
        nullable=False
    )

    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10, 2))
    
class MetodoEnvio(db.Model):
    __tablename__ = "metodos_envio"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    nombre = db.Column(db.String(150))
    precio = db.Column(db.Numeric(10, 2))
    tiempo = db.Column(db.String(100))
    
class Envio(db.Model):
    __tablename__ = "envios"

    id = db.Column(db.Integer, primary_key=True)

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id"),
        nullable=False
    )

    metodo_envio_id = db.Column(
        db.Integer,
        db.ForeignKey("metodos_envio.id")
    )

    direccion_id = db.Column(
        db.Integer,
        db.ForeignKey("direcciones.id")
    )

    estado = db.Column(db.String(50))
    tracking = db.Column(db.String(150))
    
class Direccion(db.Model):
    __tablename__ = "direcciones"

    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id")
    )

    calle = db.Column(db.String(200))
    ciudad = db.Column(db.String(100))
    provincia = db.Column(db.String(100))
    pais = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(20))

