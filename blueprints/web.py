from flask import Blueprint, render_template, session, request, redirect, url_for
from models import Producto, Carrito, TurnoCaja, Venta, DetalleVenta
from models import db
from models import Configuracion

def get_config(clave, default=None):
    config = Configuracion.query.filter_by(clave=clave).first()
    return config.valor if config else default

web_bp = Blueprint("web", __name__)

# ================= WEB PÚBLICA =================
@web_bp.route("/")
def home():
    usuario = session.get("usuario")

    banner_imagen = get_config("banner_imagen", "banner.jpg")
    banner_titulo = get_config("nombre_tienda", "Mi Tienda Online")
    banner_subtitulo = get_config(
        "slogan",
        "Encuentra los mejores productos al mejor precio"
    )

    # Productos destacados (ejemplo: primeros 6)
    productos = Producto.query.limit(6).all()

    ofertas = [
        {"descripcion": "50% de descuento en productos seleccionados"},
        {"descripcion": "Envío gratuito en compras mayores a $50"},
        {"descripcion": "Promoción 2x1 en productos destacados"},
    ]

    beneficios = [
        {"titulo": "Envío rápido", "descripcion": "Recibe tus productos en tiempo récord."},
        {"titulo": "Calidad garantizada", "descripcion": "Solo trabajamos con productos de alta calidad."},
        {"titulo": "Soporte 24/7", "descripcion": "Estamos disponibles para ayudarte en cualquier momento."},
    ]

    return render_template(
        "web/home.html",
        usuario=usuario,
        banner_imagen=banner_imagen,
        banner_titulo=banner_titulo,
        banner_subtitulo=banner_subtitulo,
        productos=productos,
        ofertas=ofertas,
        beneficios=beneficios
    )

@web_bp.route("/tienda")
def tienda():
    productos = Producto.query.all()

    categorias = sorted(
        set(p.descripcion for p in productos if p.descripcion)
    )

    return render_template(
        "web/tienda.html",
        productos=productos,
        categorias=categorias
    )


# ================= CARRITO =================
@web_bp.route("/carrito")
def carrito():
    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    usuario_id = session["usuario"]["id"]
    items = Carrito.query.filter_by(usuario_id=usuario_id).all()
    total = sum(item.producto.precio * item.cantidad for item in items)
    return render_template("web/carrito.html", carrito=items, total=total)

@web_bp.route("/carrito/agregar/<int:producto_id>", methods=["POST"])
def agregar_carrito(producto_id):
    if "usuario" not in session:
        return redirect(url_for("web.login"))

    usuario_id = session["usuario"]["id"]
    cantidad = int(request.form.get("cantidad", 1))
    producto = Producto.query.get_or_404(producto_id)

    if producto.stock < cantidad:
        return "Stock insuficiente", 400

    item = Carrito.query.filter_by(usuario_id=usuario_id, producto_id=producto_id).first()
    if item:
        if producto.stock < item.cantidad + cantidad:
            return "Stock insuficiente", 400
        item.cantidad += cantidad
    else:
        item = Carrito(usuario_id=usuario_id, producto_id=producto_id, cantidad=cantidad)
        db.session.add(item)

    db.session.commit()
    return redirect(url_for("web.carrito"))

@web_bp.route("/carrito/actualizar/<int:item_id>", methods=["POST"])
def actualizar_carrito(item_id):
    item = Carrito.query.get_or_404(item_id)
    cantidad = int(request.form["cantidad"])
    if cantidad <= 0:
        db.session.delete(item)
    else:
        if item.producto.stock < cantidad:
            return "Stock insuficiente", 400
        item.cantidad = cantidad
    db.session.commit()
    return redirect(url_for("web.carrito"))

@web_bp.route("/carrito/eliminar/<int:item_id>")
def eliminar_carrito(item_id):
    item = Carrito.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("web.carrito"))

@web_bp.route("/carrito/pagar", methods=["POST"])
def pagar():
    if "usuario" not in session:
        return redirect(url_for("web.login"))

    usuario_id = session["usuario"]["id"]

    # 🔹 Turno activo (igual que en api_cobrar)
    turno = TurnoCaja.query.filter_by(
        vendedor_id=usuario_id,
        fin=None
    ).first()

    if not turno:
        return "<h2>No hay turno de caja activo</h2>", 400

    items = Carrito.query.filter_by(usuario_id=usuario_id).all()

    if not items:
        return "<h2>Carrito vacío</h2>", 400

    # 🔹 Verificar stock
    for item in items:
        if item.producto.stock < item.cantidad:
            return f"""
                <h2>Stock insuficiente</h2>
                <p>{item.producto.nombre}</p>
                <a href="/web/tienda">Volver</a>
            """, 400

    # 🔹 Total (entero, sin centavos)
    total = sum(
        int(item.producto.precio) * item.cantidad
        for item in items
    )

    # 🔹 Crear venta (igual que API)
    venta = Venta(
        usuario_id=usuario_id,
        total=total,
        turno_id=turno.id
    )
    db.session.add(venta)
    db.session.commit()

    # 🔹 Detalles + descuento de stock
    for item in items:
        detalle = DetalleVenta(
            venta_id=venta.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=int(item.producto.precio)
        )
        db.session.add(detalle)

        item.producto.stock -= item.cantidad
        db.session.delete(item)

    db.session.commit()

    return render_template(
        "web/pago_ok.html",
        total=total,
        venta=venta
    )

