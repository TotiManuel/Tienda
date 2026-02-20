from flask import Blueprint, flash, render_template, request, redirect, url_for
from sqlalchemy import func
from decimal import Decimal, InvalidOperation
from app.models.pago_cliente import Pago
from app import db
from app.models import Venta
from app.models.cliente import Cliente


clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


# ==============================
# 📌 LISTADO DE CLIENTES
# ==============================
@clientes_bp.route("/")
def index():
    try:
        clientes = Cliente.query.order_by(Cliente.nombre).all()

        # Morosos
        clientes_morosos = Cliente.query.filter(
            Cliente.saldo_deuda > 50000
        ).order_by(Cliente.saldo_deuda.desc()).all()

        # Ranking mejores clientes
        ranking = (
            db.session.query(
                Cliente.id,
                Cliente.nombre,
                func.coalesce(func.sum(Venta.total), 0).label("total_compras")
            )
            .outerjoin(Venta)
            .group_by(Cliente.id)
            .order_by(func.sum(Venta.total).desc())
            .limit(10)
            .all()
        )
        total_deuda = db.session.query(func.sum(Cliente.saldo_deuda)).scalar() or 0

        return render_template(
            "clientes.html",
            clientes=clientes,
            clientes_morosos=clientes_morosos,
            ranking=ranking,
            total_deuda=total_deuda
        )

    except Exception as e:
        flash("Error cargando clientes", "error")
        return render_template("clientes.html", clientes=[], clientes_morosos=[], ranking=[])


# ==============================
# 📌 CREAR CLIENTE
# ==============================
@clientes_bp.route("/crear", methods=["POST"])
def crear_cliente():
    try:
        nombre = request.form.get("nombre", "").strip()

        if not nombre:
            flash("El nombre es obligatorio", "error")
            return redirect(url_for("clientes.index"))

        cliente = Cliente(
            nombre=nombre,
            telefono=request.form.get("telefono"),
            email=request.form.get("email"),
            direccion=request.form.get("direccion"),
        )

        db.session.add(cliente)
        db.session.commit()

        flash("Cliente creado correctamente", "success")

    except Exception:
        db.session.rollback()
        flash("Error al crear cliente", "error")

    return redirect(url_for("clientes.index"))


# ==============================
# 📌 DETALLE CLIENTE
# ==============================
@clientes_bp.route("/<int:id>")
def detalle_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    ventas = (
        Venta.query.filter_by(cliente_id=id)
        .order_by(Venta.fecha.desc())
        .all()
    )

    # Estadísticas
    total_compras = sum(v.total for v in ventas)
    cantidad = len(ventas)
    ticket_promedio = total_compras / cantidad if cantidad else 0
    ticket_promedio = round(ticket_promedio, 2)

    mensaje = (
        f"Hola {cliente.nombre}, tu deuda actual es de "
        f"${cliente.saldo_deuda}. ¿Podemos coordinar el pago?"
    )

    return render_template(
        "cliente_detalle.html",
        cliente=cliente,
        ventas=ventas,
        mensaje=mensaje,
        total_compras=total_compras,
        cantidad=cantidad,
        ticket_promedio=ticket_promedio
    )


# ==============================
# 📌 REGISTRAR PAGO
# ==============================
@clientes_bp.route("/pagar/<int:id>", methods=["POST"])
def pagar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    try:
        monto = Decimal(request.form.get("monto"))

        if monto <= 0:
            flash("El monto debe ser mayor a 0", "error")
            return redirect(url_for("clientes.detalle_cliente", id=id))

        if monto > cliente.saldo_deuda:
            flash("El monto supera la deuda", "error")
            return redirect(url_for("clientes.detalle_cliente", id=id))

        pago = Pago(cliente_id=id, monto=monto)

        db.session.add(pago)
        cliente.saldo_deuda -= float(monto)
        cliente.saldo_deuda = round(cliente.saldo_deuda, 2)

        db.session.commit()

        flash("Pago registrado correctamente", "success")

    except (InvalidOperation, TypeError):
        flash("Monto inválido", "error")

    except Exception:
        db.session.rollback()
        flash("Error al registrar pago", "error")

    return redirect(url_for("clientes.detalle_cliente", id=id))
   
