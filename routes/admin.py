from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

from database.database import *

admin_bp = Blueprint(
    "admin",
    __name__
)

# ======================================
# PANEL ADMIN
# ======================================

@admin_bp.route("/admin")
def admin():

    if not session.get("admin"):

        return redirect(
            "/panel-privado"
        )

    return render_template(

        "admin.html",

        productos=obtener_productos(),

        colecciones=obtener_colecciones(),

        ofertas=obtener_ofertas(),

        promociones=obtener_promociones(),

        descuentos=obtener_descuentos()

    )

# ======================================
# CREAR PRODUCTO
# ======================================

@admin_bp.route(
    "/crear",
    methods=["POST"]
)
def crear():

    nombre = request.form["nombre"]

    precio = request.form["precio"]

    genero = request.form["genero"]

    imagen = request.form["imagen"]

    tallas = request.form[
        "tallas"
    ].split(",")

    coleccion_id = (
        request.form["coleccion_id"]
        or None
    )

    oferta_id = (
        request.form["oferta_id"]
        or None
    )

    promocion_id = (
        request.form["promocion_id"]
        or None
    )

    descuento_id = (
        request.form["descuento_id"]
        or None
    )

    imagenes_extra = request.form[
        "imagenes_extra"
    ].split(",")

    crear_producto(

        nombre,
        precio,
        genero,
        imagen,
        tallas,
        coleccion_id,
        oferta_id,
        promocion_id,
        descuento_id,
        imagenes_extra

    )

    return redirect("/admin")

# ======================================
# ELIMINAR
# ======================================

@admin_bp.route(
    "/eliminar/<int:id>"
)
def eliminar(id):

    eliminar_producto(id)

    return redirect("/admin")

# ======================================
# CREAR OFERTA
# ======================================

@admin_bp.route(
    "/crear_oferta",
    methods=["POST"]
)
def ruta_crear_oferta():

    if not session.get("admin"):

        return redirect("/")

    crear_oferta(

        request.form["nombre"]

    )

    return redirect("/admin")

# ======================================
# CREAR COLECCION
# ======================================

@admin_bp.route(
    "/crear_coleccion",
    methods=["POST"]
)
def ruta_crear_coleccion():

    if not session.get("admin"):

        return redirect("/")

    crear_coleccion(

        request.form["nombre"],

        request.form["imagen"]

    )

    return redirect("/admin")

# ======================================
# CREAR PROMOCION
# ======================================

@admin_bp.route(
    "/crear_promocion",
    methods=["POST"]
)
def ruta_crear_promocion():

    if not session.get("admin"):

        return redirect("/")

    crear_promocion(

        request.form["nombre"]

    )

    return redirect("/admin")

# ======================================
# CREAR DESCUENTO
# ======================================

@admin_bp.route(
    "/crear_descuento",
    methods=["POST"]
)
def ruta_crear_descuento():

    if not session.get("admin"):

        return redirect("/")

    crear_descuento(

        request.form["nombre"],

        request.form["porcentaje"]

    )

    return redirect("/admin")

# ======================================
# GUARDAR HERO
# ======================================

@admin_bp.route(
    "/guardar_hero",
    methods=["POST"]
)
def ruta_guardar_hero():

    guardar_hero(

        request.form["titulo"],

        request.form["subtitulo"],

        request.form["boton_texto"],

        request.form["imagen"]

    )

    return redirect("/admin")

# ======================================
# CREAR BENEFICIO
# ======================================

@admin_bp.route(
    "/crear_beneficio",
    methods=["POST"]
)
def ruta_crear_beneficio():

    crear_beneficio(

        request.form["icono"],

        request.form["titulo"],

        request.form["descripcion"]

    )

    return redirect("/admin")



