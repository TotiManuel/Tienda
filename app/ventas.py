from datetime import datetime
from flask import Blueprint, render_template, request, redirect, flash, url_for, make_response
from sqlalchemy import func
import pdfkit

from app.database import db
from app.models.cliente import Cliente
from app.models.producto import Producto
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta
from app.models.movimiento_stock import MovimientoStock


ventas_bp = Blueprint("ventas", __name__, url_prefix="/ventas")


# ======================================================
# region Rutas principales
# ======================================================
@ventas_bp.route("/")
def index():
    try:
        productos = Producto.query.all()
        clientes = Cliente.query.all()
        carrito = Venta.obtener_carrito()

        # 🔹 Ventas finalizadas optimizadas
        ventas = Venta.query.filter_by(estado="finalizada").all()

        ventas_detalle = []
        total = 0
        ganancia_total = 0

        for v in ventas:
            for d in v.detalles:
                subtotal = d.subtotal or 0
                margen = d.margen or 0

                ventas_detalle.append({
                    "nombre_producto": d.nombre_producto,
                    "precio": d.precio,
                    "cantidad": d.cantidad,
                    "subtotal": subtotal,
                    "margen": margen,
                    "metodo_pago": v.metodo_pago,
                    "fecha": v.fecha,
                    "id": v.id
                })

                total += subtotal
                ganancia_total += margen

        # 🔹 Estadísticas por método de pago optimizadas
        estadisticas_metodo = {}
        resultados = db.session.query(
            Venta.metodo_pago,
            func.count(Venta.id),
            func.sum(Venta.total)
        ).filter(Venta.estado == "finalizada").group_by(Venta.metodo_pago).all()

        for metodo, cantidad, total_metodo in resultados:
            estadisticas_metodo[metodo] = {
                "cantidad_ventas": cantidad or 0,
                "total_recaudado": total_metodo or 0
            }

        # 🔹 Historial de stock
        movimientos_stock = MovimientoStock.query.order_by(
            MovimientoStock.fecha.desc()
        ).limit(100).all()

        # 🔹 Estadísticas temporales
        ventas_por_dia = db.session.query(
            func.strftime("%d/%m/%Y", Venta.fecha),
            func.sum(Venta.total)
        ).filter(Venta.estado == "finalizada"
        ).group_by(func.strftime("%d/%m/%Y", Venta.fecha)).all()

        ventas_por_mes = db.session.query(
            func.strftime("%m/%Y", Venta.fecha),
            func.sum(Venta.total)
        ).filter(Venta.estado == "finalizada"
        ).group_by(func.strftime("%m/%Y", Venta.fecha)).all()

        # 🔹 Producto más vendido
        producto_mas_vendido = db.session.query(
            DetalleVenta.nombre_producto,
            func.sum(DetalleVenta.cantidad)
        ).join(Venta, Venta.id == DetalleVenta.venta_id
        ).filter(Venta.estado == "finalizada"
        ).group_by(DetalleVenta.nombre_producto
        ).order_by(func.sum(DetalleVenta.cantidad).desc()
        ).first()

        return render_template(
            "ventas.html",
            productos=productos,
            carrito=carrito,
            ventas_detalle=ventas_detalle,
            ventas_totales=total,
            estadisticas_metodo=estadisticas_metodo,
            ventas_por_dia=ventas_por_dia,
            ventas_por_mes=ventas_por_mes,
            producto_mas_vendido=producto_mas_vendido,
            ganancia_total=ganancia_total,
            movimientos_stock=movimientos_stock,
            clientes=clientes,
        )

    except Exception as e:
        flash(f"Error cargando ventas: {e}")
        return redirect("/")
# endregion



# ======================================================
# region Productos
# ======================================================
@ventas_bp.route("/agregar", methods=["POST"])
def agregar_producto():
    try:
        nombre = request.form.get("nombre", "").strip()
        precio = float(request.form.get("precio", 0))
        costo = float(request.form.get("costo", 0))
        stock = int(request.form.get("stock", 0))

        if not nombre or precio < 0 or stock < 0:
            flash("Datos inválidos")
            return redirect("/ventas")

        nuevo = Producto(
            nombre=nombre,
            precio=precio,
            costo=costo,
            stock=stock
        )

        db.session.add(nuevo)
        db.session.commit()

        flash(f"Producto '{nombre}' agregado")

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}")

    return redirect("/ventas")


@ventas_bp.route("/editar/<int:id>", methods=["POST"])
def editar_producto(id):
    try:
        producto = Producto.query.get_or_404(id)

        nombre = request.form.get("nombre", "").strip()
        precio = float(request.form.get("precio", 0))
        costo = float(request.form.get("costo", 0))
        stock_nuevo = int(request.form.get("stock", 0))

        if not nombre or precio < 0 or stock_nuevo < 0:
            flash("Datos inválidos")
            return redirect("/ventas")

        stock_anterior = producto.stock

        producto.nombre = nombre
        producto.precio = precio
        producto.costo = costo
        producto.stock = stock_nuevo

        diferencia = stock_nuevo - stock_anterior

        if diferencia != 0:
            tipo = "Ingreso" if diferencia > 0 else "Salida"

            mov = MovimientoStock(
                producto_id=producto.id,
                cantidad=abs(diferencia),
                tipo=tipo,
                fecha=datetime.now()
            )

            db.session.add(mov)

        db.session.commit()

        flash("Producto actualizado")

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}")

    return redirect("/ventas")


@ventas_bp.route("/eliminar/<int:id>")
def eliminar_producto(id):
    try:
        producto = Producto.query.get_or_404(id)
        db.session.delete(producto)
        db.session.commit()

        flash("Producto eliminado")

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}")

    return redirect("/ventas")
# endregion



# ======================================================
# region Venta directa
# ======================================================
@ventas_bp.route("/vender/<int:id>", methods=["POST"])
def vender(id):
    try:
        producto = Producto.query.get_or_404(id)
        cantidad = int(request.form.get("cantidad", 0))

        cliente_id = request.form.get("cliente_id")
        metodo_pago = request.form.get("metodo_pago")

        if cantidad <= 0:
            flash("Cantidad inválida")
            return redirect(url_for("ventas.index"))

        if producto.stock < cantidad:
            flash("Stock insuficiente")
            return redirect(url_for("ventas.index"))

        venta = Venta(
            estado="finalizada",
            total=0,
            cliente_id=cliente_id if cliente_id else None,
            metodo_pago=metodo_pago
        )

        db.session.add(venta)
        db.session.flush()

        subtotal = producto.precio * cantidad
        margen = (producto.precio - producto.costo) * cantidad

        detalle = DetalleVenta(
            venta_id=venta.id,
            producto_id=producto.id,
            nombre_producto=producto.nombre,
            precio=producto.precio,
            costo=producto.costo,
            cantidad=cantidad,
            subtotal=subtotal,
            margen=margen
        )

        db.session.add(detalle)

        # Stock
        producto.stock -= cantidad

        mov = MovimientoStock(
            producto_id=producto.id,
            cantidad=cantidad,
            tipo="Salida",
            fecha=datetime.now()
        )
        db.session.add(mov)

        venta.recalcular_total()

        # 🔥 Deuda
        if cliente_id and metodo_pago == "fiado":
            cliente = Cliente.query.get(cliente_id)
            if cliente:
                cliente.saldo_deuda += subtotal

        db.session.commit()

        flash("Venta registrada")

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}")

    return redirect(url_for("ventas.index"))
# endregion
# -----------------------------
# Carrito
# -----------------------------
@ventas_bp.route("/carrito/agregar/<int:id>")
def agregar_al_carrito(id):
    carrito = Venta.obtener_carrito()
    producto = Producto.query.get_or_404(id)

    detalle = DetalleVenta.query.filter_by(venta_id=carrito.id, producto_id=id).first()
    if detalle:
        detalle.cantidad += 1
    else:
        detalle = DetalleVenta(
            venta_id=carrito.id,
            producto_id=producto.id,
            nombre_producto=producto.nombre,
            cantidad=1,
            precio=producto.precio,
            subtotal=producto.precio,
            costo=producto.costo,
            margen=producto.precio - producto.costo
        )
        db.session.add(detalle)

    detalle.subtotal = detalle.cantidad * detalle.precio
    carrito.total = sum(d.subtotal for d in carrito.detalles)
    db.session.commit()

    flash(f"Producto {producto.nombre} agregado al carrito")
    return redirect("/ventas")

@ventas_bp.route("/carrito/confirmar", methods=["POST"])
def confirmar_carrito():
    carrito = Venta.obtener_carrito()
    cliente_id = request.form.get("cliente_id")
    metodo_pago = request.form.get("metodo_pago", "Efectivo")

    if not carrito.detalles:
        flash("No hay productos en el carrito", "error")
        return redirect("/ventas")

    for d in carrito.detalles:
        producto = Producto.query.get(d.producto_id)
        producto.stock -= d.cantidad
        d.margen = (d.precio - producto.costo) * d.cantidad

        mov = MovimientoStock(producto_id=producto.id, cantidad=d.cantidad, tipo="Salida", fecha=datetime.now())
        db.session.add(mov)

    carrito.estado = "finalizada"
    carrito.metodo_pago = metodo_pago
    carrito.cliente_id = cliente_id if cliente_id else None
    carrito.recalcular_total()
    db.session.commit()

    # Si es fiado, actualizar deuda
    if cliente_id and metodo_pago.lower() == "fiado":
        cliente = Cliente.query.get(cliente_id)
        cliente.saldo_deuda += carrito.total
        db.session.commit()

    flash(f"Venta confirmada vía {metodo_pago}")
    return redirect("/ventas")

@ventas_bp.route("/carrito/quitar/<int:id>", methods=["GET"])
def quitar_del_carrito(id):
    carrito = Venta.obtener_carrito()  # tu función para obtener carrito
    if not carrito:
        flash("No hay carrito activo", "error")
        return redirect(url_for("ventas.index"))

    # Buscamos el producto en el carrito
    detalle = next((d for d in carrito.detalles if d.producto_id == id), None)
    if detalle:
        carrito.detalles.remove(detalle)
        db.session.commit()
        flash(f"Se removió {detalle.nombre_producto} del carrito", "success")
    else:
        flash("Producto no encontrado en el carrito", "error")

    return redirect(url_for("ventas.index")) 

# -----------------------------
# Ticket PDF
# -----------------------------
@ventas_bp.route("/ticket/pdf/<int:id>")
def generar_ticket_pdf(id):
    venta = Venta.query.get_or_404(id)
    rendered = render_template("ticket.html", venta=venta)
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=ticket_{venta.id}.pdf'
    return response