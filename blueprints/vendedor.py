from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from blueprints.cliente import login_requerido
from models import Carrito, Producto, Proveedor, TurnoCaja, Usuario, Venta, db
from datetime import datetime

vendedor_bp = Blueprint("vendedor", __name__)

def login_requerido():
    return "usuario" in session and "id" in session["usuario"]
def es_vendedor():
    return (
        "usuario" in session and
        session["usuario"].get("rol") == "vendedor"
    )
@vendedor_bp.route("/ventas")
def vendedor_ventas():
    if not login_requerido():
        return redirect(url_for("auth.login"))

    if not es_vendedor():
        flash("No tenés permisos para acceder a esta sección", "error")
        return redirect(url_for("web.home"))

    ventas = (
        Venta.query
        .order_by(Venta.fecha.desc())
        .all()
    )

    return render_template(
        "vendedor/ventas.html",
        ventas=ventas
    )
@vendedor_bp.route("/clientes")
def vendedor_clientes():
    if not login_requerido():
        return redirect(url_for("auth.login"))

    if session["usuario"]["rol"] != "vendedor":
        return redirect(url_for("web.tienda"))

    clientes = Usuario.query.filter_by(rol="cliente").all()

    return render_template(
        "vendedor/clientes.html",
        clientes=clientes
    )
@vendedor_bp.route("/clientes/<int:usuario_id>/pedidos")
def pedidos_cliente(usuario_id):
    if not login_requerido():
        return redirect(url_for("auth.login"))

    if session["usuario"]["rol"] != "vendedor":
        return redirect(url_for("web.tienda"))

    cliente = Usuario.query.get_or_404(usuario_id)

    # Seguridad extra
    if cliente.rol != "cliente":
        return redirect(url_for("vendedor.vendedor_clientes"))

    pedidos = (
        Venta.query
        .filter_by(usuario_id=cliente.id)
        .order_by(Venta.fecha.desc())
        .all()
    )

    return render_template(
        "vendedor/pedidos_cliente.html",
        cliente=cliente,
        pedidos=pedidos
    )
@vendedor_bp.route("/caja")
def vendedor_caja():
    if session["usuario"]["rol"] != "vendedor":
        return redirect(url_for("web.tienda"))

    vendedor_id = session["usuario"]["id"]

    turno = (
        TurnoCaja.query
        .filter_by(vendedor_id=vendedor_id, fin=None)
        .first()
    )

    if not turno:
        turno = TurnoCaja(vendedor_id=vendedor_id)
        db.session.add(turno)
        db.session.commit()

    ventas = (
        Venta.query
        .filter_by(turno_id=turno.id)
        .order_by(Venta.fecha.desc())
        .all()
    )

    total = sum(v.total for v in ventas)

    return render_template(
        "vendedor/caja.html",
        ventas=ventas,
        total=total,
        turno=turno
    )
@vendedor_bp.route("/caja/cerrar", methods=["POST"])
def cerrar_caja():
    turno = TurnoCaja.query.filter_by(
        vendedor_id=session["usuario"]["id"],
        fin=None
    ).first()

    if turno:
        turno.fin = datetime.utcnow()
        db.session.commit()

    return redirect(url_for("vendedor.vendedor_caja"))
@vendedor_bp.route("/productos")
def vendedor_productos():
    if not login_requerido():
        return redirect(url_for("auth.login"))

    if session["usuario"]["rol"] != "vendedor":
        return redirect(url_for("web.tienda"))

    productos = Producto.query.all()
    proveedores = Proveedor.query.all()

    return render_template(
        "vendedor/productos.html",
        productos=productos,
        proveedores=proveedores
    )
@vendedor_bp.route("/api/carrito/agregar", methods=["POST"])
def api_agregar_carrito():
    data = request.json
    producto_id = data["producto_id"]
    cantidad = int(data["cantidad"])
    usuario_id = session["usuario"]["id"]

    item = Carrito.query.filter_by(
        usuario_id=usuario_id,
        producto_id=producto_id
    ).first()

    if item:
        item.cantidad += cantidad
    else:
        item = Carrito(
            usuario_id=usuario_id,
            producto_id=producto_id,
            cantidad=cantidad
        )
        db.session.add(item)

    db.session.commit()
    return {"ok": True}
@vendedor_bp.route("/api/carrito")
def api_carrito():
    usuario_id = session["usuario"]["id"]
    items = Carrito.query.filter_by(usuario_id=usuario_id).all()

    total = sum(int(i.producto.precio) * i.cantidad for i in items)

    return {
        "items": [
            {
                "id": i.id,
                "nombre": i.producto.nombre,
                "cantidad": i.cantidad,
                "precio": int(i.producto.precio),
                "subtotal": int(i.producto.precio) * i.cantidad
            }
            for i in items
        ],
        "total": total
    }
@vendedor_bp.route("/api/carrito/eliminar/<int:item_id>", methods=["POST"])
def api_eliminar_carrito(item_id):
    item = Carrito.query.get_or_404(item_id)

    if item.cantidad > 1:
        item.cantidad -= 1
    else:
        db.session.delete(item)

    db.session.commit()
    return {"ok": True}
@vendedor_bp.route("/api/carrito/cobrar", methods=["POST"])
def api_cobrar():
    if not login_requerido() or not es_vendedor():
        return {"error": "No autorizado"}, 403

    usuario_id = session["usuario"]["id"]

    # Turno activo
    turno = TurnoCaja.query.filter_by(
        vendedor_id=usuario_id,
        fin=None
    ).first()

    if not turno:
        return {"error": "No hay turno activo"}, 400

    items = Carrito.query.filter_by(usuario_id=usuario_id).all()

    if not items:
        return {"error": "Carrito vacío"}, 400

    # Verificar stock
    for item in items:
        if item.producto.stock < item.cantidad:
            return {
                "error": f"Stock insuficiente para {item.producto.nombre}"
            }, 400

    # Total
    total = sum(
        int(item.producto.precio) * item.cantidad
        for item in items
    )

    # Crear venta
    venta = Venta(
        usuario_id=usuario_id,
        total=total,
        turno_id=turno.id
    )
    db.session.add(venta)
    db.session.commit()

    # Detalles + stock
    from models import DetalleVenta

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

    return {
        "ok": True,
        "venta_id": venta.id,
        "total": total
    }

