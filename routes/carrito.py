from flask import (
    Blueprint,
    session,
    request,
    redirect,
    render_template
)

from database.database import *

carrito_bp = Blueprint(
    "carrito",
    __name__
)

# ======================================
# AGREGAR
# ======================================

@carrito_bp.route(
    "/agregar/<int:id>",
    methods=["POST"]
)
def agregar(id):

    talle = request.form.get(
        "talle"
    )

    carrito = session.get(
        "carrito",
        []
    )

    carrito.append({

        "id": id,
        "talle": talle

    })

    session["carrito"] = carrito

    return redirect("/carrito")

# ======================================
# CARRITO
# ======================================

@carrito_bp.route("/carrito")
def carrito():

    carrito = session.get(
        "carrito",
        []
    )

    productos_carrito = []

    for item in carrito:

        producto = next(

            (

                p for p in obtener_productos()

                if p["id"] == item["id"]

            ),

            None

        )

        if producto:

            producto_copia = (
                producto.copy()
            )

            producto_copia["talle"] = (
                item["talle"]
            )

            productos_carrito.append(
                producto_copia
            )

    total = sum(

        p["precio"]

        for p in productos_carrito

    )

    return render_template(

        "carrito.html",

        productos=productos_carrito,

        total=total,

        productos_tienda=obtener_productos()

    )

# ======================================
# QUITAR
# ======================================

@carrito_bp.route(
    "/quitar/<int:index>"
)
def quitar(index):

    carrito = session.get(
        "carrito",
        []
    )

    if 0 <= index < len(carrito):

        carrito.pop(index)

    session["carrito"] = carrito

    return redirect("/carrito")