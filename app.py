from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)
from database.database import *
import os
app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "clave_super_secreta"
)

ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin123"

crear_tablas()

@app.route("/")
def index():

    return render_template(
        "index.html",
        productos=obtener_productos()
    )
    
@app.route("/atencion_cliente")
def atencion_cliente():

    return render_template(
        "atencion_cliente.html"
    )

@app.route("/catalogo")
def catalogo():

    return render_template(
        "catalogo.html",
        productos=obtener_productos(),
        titulo="Catálogo",
        filtro_activo="todo"
    )

@app.route("/categoria/<filtro>")
def categoria(filtro):

    filtro = filtro.lower()

    productos_filtrados = []

    for p in obtener_productos():

        genero = p["genero"].lower()
        coleccion = p["coleccion"].lower()

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

@app.route("/colecciones")
def colecciones():

    colecciones = [
        {
            "nombre": "Urban",
            "imagen":
            "https://images.unsplash.com/photo-1523398002811-999ca8dec234"
        },

        {
            "nombre": "Invierno",
            "imagen":
            "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f"
        },

        {
            "nombre": "Oversize",
            "imagen":
            "https://images.unsplash.com/photo-1496747611176-843222e1e57c"
        },

        {
            "nombre": "Minimal",
            "imagen":
            "https://images.unsplash.com/photo-1483985988355-763728e1935b"
        },

        {
            "nombre": "Verano",
            "imagen":
            "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c"
        },

        {
            "nombre": "Streetwear",
            "imagen":
            "https://images.unsplash.com/photo-1507679799987-c73779587ccf"
        }
    ]

    return render_template(
        "colecciones.html",
        colecciones=colecciones
    )
    
@app.route("/producto/<int:id>")
def detalle_producto(id):

    producto = obtener_productos(id)

    if not producto:
        return redirect("/")

    # imágenes extra temporales
    producto["imagenes_extra"] = [
        producto["imagen"],
        producto["imagen"],
        producto["imagen"]
    ]

    producto["descripcion"] = (
        "Prenda premium minimalista "
        "con diseño urbano."
    )

    return render_template(
        "detalle_producto.html",
        producto=producto
    )

@app.route("/agregar/<int:id>", methods=["POST"])
def agregar(id):

    talle = request.form.get("talle")

    carrito = session.get("carrito", [])

    carrito.append({
        "id": id,
        "talle": talle
    })

    session["carrito"] = carrito

    return redirect("/carrito")

@app.route("/carrito")
def carrito():

    carrito = session.get("carrito", [])

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

            producto_copia = producto.copy()

            producto_copia["talle"] = item["talle"]

            productos_carrito.append(producto_copia)

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

@app.route("/quitar/<int:index>")
def quitar(index):

    carrito = session.get("carrito", [])

    if 0 <= index < len(carrito):
        carrito.pop(index)

    session["carrito"] = carrito

    return redirect("/carrito")

@app.route("/panel-privado", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        if (
            usuario == ADMIN_USER and
            password == ADMIN_PASSWORD
        ):

            session["admin"] = True

            return redirect("/admin")

    return render_template("login.html")

@app.route("/admin")
def admin():

    if not session.get("admin"):

        return redirect("/panel-privado")

    productos = obtener_productos()

    colecciones = obtener_colecciones()

    ofertas = obtener_ofertas()

    promociones = obtener_promociones()

    descuentos = obtener_descuentos()

    return render_template(

        "admin.html",

        productos=productos,

        colecciones=colecciones,

        ofertas=ofertas,

        promociones=promociones,

        descuentos=descuentos

    )

@app.route("/eliminar/<int:id>")
def eliminar(id):

    if not session.get("admin"):

        return redirect("/")

    eliminar_producto(id)

    return redirect("/admin")

@app.route(

    "/editar/<int:id>",

    methods=["GET", "POST"]

)
def editar(id):

    if not session.get("admin"):

        return redirect("/")

    # =================================
    # GUARDAR CAMBIOS
    # =================================

    if request.method == "POST":

        editar_producto(

            id,

            request.form["nombre"],

            float(
                request.form["precio"]
            ),

            request.form["genero"],

            request.form["imagen"],

            request.form["tallas"].split(","),

            request.form["coleccion_id"] or None,

            request.form["oferta_id"] or None,

            request.form["promocion_id"] or None,

            request.form["descuento_id"] or None

        )

        return redirect("/admin")

    # =================================
    # MOSTRAR FORMULARIO
    # =================================

    producto = obtener_producto(id)

    colecciones = obtener_colecciones()

    ofertas = obtener_ofertas()

    promociones = obtener_promociones()

    descuentos = obtener_descuentos()

    return render_template(

        "editar.html",

        producto=producto,

        colecciones=colecciones,

        ofertas=ofertas,

        promociones=promociones,

        descuentos=descuentos

    )

@app.route("/crear", methods=["POST"])
def crear():

    nombre = request.form["nombre"]

    precio = request.form["precio"]

    genero = request.form["genero"]

    imagen = request.form["imagen"]

    tallas = request.form["tallas"].split(",")

    coleccion_id = request.form["coleccion_id"] or None

    oferta_id = request.form["oferta_id"] or None

    promocion_id = request.form["promocion_id"] or None

    descuento_id = request.form["descuento_id"] or None

    crear_producto(

        nombre,
        precio,
        genero,
        imagen,
        tallas,
        coleccion_id,
        oferta_id,
        promocion_id,
        descuento_id

    )

    return redirect("/admin")

@app.route("/crear_coleccion", methods=["POST"])
def ruta_crear_coleccion():

    crear_coleccion(
        request.form["nombre"]
    )

    return redirect("/admin")

@app.route("/crear_oferta", methods=["POST"])
def ruta_crear_oferta():

    crear_oferta(
        request.form["nombre"]
    )

    return redirect("/admin")

@app.route("/crear_promocion", methods=["POST"])
def ruta_crear_promocion():

    crear_promocion(
        request.form["nombre"]
    )

    return redirect("/admin")

@app.route("/crear_descuento", methods=["POST"])
def ruta_crear_descuento():

    crear_descuento(

        request.form["nombre"],
        request.form["porcentaje"]

    )

    return redirect("/admin")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)