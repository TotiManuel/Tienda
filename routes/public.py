from flask import (
    Blueprint,
    render_template,
    redirect
)

from database.database import *

public_bp = Blueprint(
    "public",
    __name__
)

# ======================================
# HOME
# ======================================

@public_bp.route("/")
def index():

    return render_template(
        "index.html",
        productos=obtener_productos()
    )

# ======================================
# ATENCION CLIENTE
# ======================================

@public_bp.route("/atencion_cliente")
def atencion_cliente():

    return render_template(
        "atencion_cliente.html"
    )

# ======================================
# CATALOGO
# ======================================

@public_bp.route("/catalogo")
def catalogo():

    return render_template(
        "catalogo.html",
        productos=obtener_productos(),
        titulo="Catálogo",
        filtro_activo="todo"
    )

# ======================================
# CATEGORIA
# ======================================

@public_bp.route("/categoria/<filtro>")
def categoria(filtro):

    filtro = filtro.lower()

    productos_filtrados = []

    for p in obtener_productos():

        genero = (p["genero"] or "").lower()

        coleccion = (
            p["coleccion"] or ""
        ).lower()

        if (

            filtro in genero or
            filtro in coleccion

        ):

            productos_filtrados.append(p)

    return render_template(

        "catalogo.html",

        productos=productos_filtrados,

        titulo=filtro.capitalize(),

        filtro_activo=filtro

    )

# ======================================
# COLECCIONES
# ======================================

@public_bp.route("/colecciones")
def colecciones():

    return render_template(

        "colecciones.html",

        colecciones=obtener_colecciones()

    )

# ======================================
# DETALLE PRODUCTO
# ======================================

@public_bp.route("/producto/<int:id>")
def detalle_producto(id):

    producto = obtener_producto(id)

    if not producto:

        return redirect("/")

    producto["descripcion"] = (

        "Prenda premium minimalista "
        "con diseño urbano."

    )

    return render_template(

        "detalle_producto.html",

        producto=producto

    )