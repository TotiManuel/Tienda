from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Usuario, Producto, Proveedor, Venta, DetalleVenta, Promocion, Configuracion
from utils.decorators import rol_requerido

admin_bp = Blueprint("admin", __name__)

# ================== CONTEXTO ==================
@admin_bp.app_context_processor
def inject_usuario():
    return dict(usuario=session.get("usuario"))

# ================== USUARIOS ==================
@admin_bp.route("/usuarios")
@rol_requerido("admin")
def admin_usuarios():
    usuarios = Usuario.query.all()
    return render_template("admin/usuarios.html", usuarios=usuarios)
@admin_bp.route("/usuarios/agregar", methods=["POST"])
def agregar_usuario():
    nombre = request.form["nombre"]
    password = request.form["password"]
    rol = request.form["rol"]

    if Usuario.query.filter_by(nombre=nombre).first():
        flash("El nombre de usuario ya existe.", "error")
    else:
        nuevo = Usuario(nombre=nombre, rol=rol)
        nuevo.set_password(password)
        db.session.add(nuevo)
        db.session.commit()
        flash("Usuario agregado correctamente.", "success")

    return redirect(url_for("admin.admin_usuarios"))

@admin_bp.route("/usuarios/editar/<int:user_id>", methods=["POST"])
def editar_usuario(user_id):
    user = Usuario.query.get_or_404(user_id)
    user.nombre = request.form["nombre"]
    user.rol = request.form["rol"]
    if request.form["password"]:
        user.set_password(request.form["password"])
    db.session.commit()
    flash("Usuario actualizado.", "success")
    return redirect(url_for("admin.admin_usuarios"))

@admin_bp.route("/usuarios/eliminar/<int:user_id>", methods=["POST"])
def eliminar_usuario(user_id):
    user = Usuario.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Usuario eliminado.", "success")
    return redirect(url_for("admin.admin_usuarios"))

# ================== PRODUCTOS ==================
@admin_bp.route("/productos")
def admin_productos():
    productos = Producto.query.all()
    proveedores = Proveedor.query.all()
    return render_template(
        "admin/productos.html",
        productos=productos,
        proveedores=proveedores
    )


@admin_bp.route("/productos/agregar", methods=["POST"])
def agregar_producto():
    nuevo = Producto(
        nombre=request.form["nombre"],
        descripcion=request.form["descripcion"],
        precio=float(request.form["precio"]),
        imagen=request.form["imagen"],
        stock=int(request.form["stock"]),
        proveedor_id=int(request.form["proveedor_id"])
    )
    db.session.add(nuevo)
    db.session.commit()
    flash("Producto agregado correctamente.", "success")
    return redirect(url_for("admin.admin_productos"))


@admin_bp.route("/productos/editar/<int:producto_id>", methods=["POST"])
def editar_producto(producto_id):
    p = Producto.query.get_or_404(producto_id)

    p.nombre = request.form["nombre"]
    p.descripcion = request.form["descripcion"]
    p.precio = float(request.form["precio"])
    p.imagen = request.form["imagen"]
    p.stock = int(request.form["stock"])
    p.proveedor_id = int(request.form["proveedor_id"])

    db.session.commit()
    flash("Producto actualizado.", "success")
    return redirect(url_for("admin.admin_productos"))


@admin_bp.route("/productos/eliminar/<int:producto_id>", methods=["POST"])
def eliminar_producto(producto_id):
    p = Producto.query.get_or_404(producto_id)
    db.session.delete(p)
    db.session.commit()
    flash("Producto eliminado.", "success")
    return redirect(url_for("admin.admin_productos"))

# ================== PROVEEDORES ==================
@admin_bp.route("/proveedores")
def admin_proveedores():
    proveedores = Proveedor.query.all()
    return render_template("admin/proveedores.html", proveedores=proveedores)

@admin_bp.route("/proveedores/agregar", methods=["POST"])
def agregar_proveedor():
    proveedor = Proveedor(
        nombre=request.form["nombre"],
        contacto=request.form["contacto"],
        telefono=request.form["telefono"],
        email=request.form["email"]
    )
    db.session.add(proveedor)
    db.session.commit()
    return redirect(url_for("admin.admin_proveedores"))

@admin_bp.route("/proveedores/editar/<int:proveedor_id>", methods=["POST"])
def editar_proveedor(proveedor_id):
    proveedor = Proveedor.query.get_or_404(proveedor_id)
    proveedor.nombre = request.form["nombre"]
    proveedor.contacto = request.form["contacto"]
    proveedor.telefono = request.form["telefono"]
    proveedor.email = request.form["email"]
    db.session.commit()
    return redirect(url_for("admin.admin_proveedores"))

@admin_bp.route("/proveedores/eliminar/<int:proveedor_id>", methods=["POST"])
def eliminar_proveedor(proveedor_id):
    proveedor = Proveedor.query.get_or_404(proveedor_id)
    db.session.delete(proveedor)
    db.session.commit()
    return redirect(url_for("admin.admin_proveedores"))

# ================== STOCK ==================
@admin_bp.route("/stock")
def admin_stock():
    productos = Producto.query.order_by(Producto.nombre).all()
    return render_template("admin/stock.html", productos=productos)

@admin_bp.route("/stock/actualizar/<int:producto_id>", methods=["POST"])
def actualizar_stock(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    nuevo_stock = int(request.form["stock"])
    if nuevo_stock < 0:
        flash("El stock no puede ser negativo", "error")
        return redirect(url_for("admin.admin_stock"))
    producto.stock = nuevo_stock
    db.session.commit()
    flash("Stock actualizado correctamente", "success")
    return redirect(url_for("admin.admin_stock"))

@admin_bp.route("/stock/sumar/<int:producto_id>", methods=["POST"])
def sumar_stock(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    cantidad = int(request.form["cantidad"])
    if cantidad <= 0:
        flash("Cantidad inválida", "error")
        return redirect(url_for("admin.admin_stock"))
    producto.stock += cantidad
    db.session.commit()
    flash("Stock agregado correctamente", "success")
    return redirect(url_for("admin.admin_stock"))

# ================== VENTAS ==================
@admin_bp.route("/ventas")
def admin_ventas():
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template("admin/ventas.html", ventas=ventas)

@admin_bp.route("/ventas/<int:venta_id>")
def ver_venta(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    return render_template("admin/venta_detalle.html", venta=venta)

# ================== CLIENTES ==================
@admin_bp.route("/clientes")
def admin_clientes():
    clientes = Usuario.query.filter_by(rol="cliente").all()
    return render_template("admin/clientes.html", clientes=clientes)

@admin_bp.route("/clientes/eliminar/<int:cliente_id>", methods=["POST"])
def eliminar_cliente(cliente_id):
    cliente = Usuario.query.get_or_404(cliente_id)
    if cliente.rol != "cliente":
        return "Acción no permitida", 403
    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente eliminado correctamente", "success")
    return redirect(url_for("admin.admin_clientes"))

# ================== PROMOCIONES ==================
@admin_bp.route("/promociones")
def admin_promociones():
    promociones = Promocion.query.all()
    return render_template("admin/promociones.html", promociones=promociones)

@admin_bp.route("/promociones/agregar", methods=["POST"])
def agregar_promocion():
    descripcion = request.form["descripcion"]
    descuento = float(request.form["descuento"])
    if descuento <= 0 or descuento > 100:
        flash("El descuento debe estar entre 1 y 100", "error")
        return redirect(url_for("admin.admin_promociones"))

    promo = Promocion(descripcion=descripcion, descuento=descuento)
    db.session.add(promo)
    db.session.commit()
    flash("Promoción creada correctamente", "success")
    return redirect(url_for("admin.admin_promociones"))

@admin_bp.route("/promociones/editar/<int:promo_id>", methods=["POST"])
def editar_promocion(promo_id):
    promo = Promocion.query.get_or_404(promo_id)
    promo.descripcion = request.form["descripcion"]
    promo.descuento = float(request.form["descuento"])
    db.session.commit()
    flash("Promoción actualizada", "success")
    return redirect(url_for("admin.admin_promociones"))

@admin_bp.route("/promociones/eliminar/<int:promo_id>", methods=["POST"])
def eliminar_promocion(promo_id):
    promo = Promocion.query.get_or_404(promo_id)
    db.session.delete(promo)
    db.session.commit()
    flash("Promoción eliminada", "success")
    return redirect(url_for("admin.admin_promociones"))

# ================== CONFIGURACIÓN ==================
@admin_bp.route("/configuracion", methods=["GET", "POST"])
def admin_configuracion():
    if "usuario" not in session or session["usuario"]["rol"] != "admin":
        return "Acceso denegado", 403

    if request.method == "POST":
        for clave, valor in request.form.items():
            config = Configuracion.query.filter_by(clave=clave).first()
            if config:
                config.valor = valor
        db.session.commit()
        flash("Configuración actualizada correctamente", "success")
        return redirect(url_for("admin.admin_configuracion"))

    configs = Configuracion.query.all()
    config_dict = {c.clave: c.valor for c in configs}
    return render_template("admin/configuracion.html", config=config_dict)
