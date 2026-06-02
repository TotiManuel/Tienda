from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)

import os

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "clave_super_secreta"
)

ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin123"

# ====================================
# BASE TEMPORAL EN MEMORIA
# ====================================

productos = [
    {
        "id": 1,
        "nombre": "Remera Oversize",
        "precio": 15000,
        "coleccion": "Invierno",
        "imagen": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab"
    },
    {
        "id": 2,
        "nombre": "Buzo Negro",
        "precio": 28000,
        "coleccion": "Urban",
        "imagen": "https://images.unsplash.com/photo-1503341504253-dff4815485f1"
    }
]

# ====================================
# HOME
# ====================================

@app.route("/")
def index():

    return render_template(
        "index.html",
        productos=productos
    )

@app.route("/catalogo")
def catalogo():

    return render_template(
        "catalogo.html",
        productos=productos
    )
    
@app.route("/producto/<int:id>")
def detalle_producto(id):

    producto = next(
        (
            p for p in productos
            if p["id"] == id
        ),
        None
    )

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

# ====================================
# CARRITO
# ====================================

@app.route("/agregar/<int:id>")
def agregar(id):

    carrito = session.get("carrito", [])

    carrito.append(id)

    session["carrito"] = carrito

    return redirect("/")

@app.route("/carrito")
def carrito():

    carrito_ids = session.get("carrito", [])

    productos_carrito = []

    for producto in productos:

        if producto["id"] in carrito_ids:
            productos_carrito.append(producto)

    total = sum(
        p["precio"]
        for p in productos_carrito
    )

    return render_template(
        "carrito.html",
        productos=productos_carrito,
        total=total
    )

@app.route("/quitar/<int:index>")
def quitar(index):

    carrito = session.get("carrito", [])

    if 0 <= index < len(carrito):
        carrito.pop(index)

    session["carrito"] = carrito

    return redirect("/carrito")

# ====================================
# LOGIN
# ====================================

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

# ====================================
# PANEL ADMIN
# ====================================

@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/panel-privado")

    return render_template(
        "admin.html",
        productos=productos
    )

# ====================================
# CREAR
# ====================================

@app.route("/crear", methods=["POST"])
def crear():

    if not session.get("admin"):
        return redirect("/")

    nuevo = {
        "id": len(productos) + 1,
        "nombre": request.form["nombre"],
        "precio": float(request.form["precio"]),
        "coleccion": request.form["coleccion"],
        "imagen": request.form["imagen"]
    }

    productos.append(nuevo)

    return redirect("/admin")

# ====================================
# ELIMINAR
# ====================================

@app.route("/eliminar/<int:id>")
def eliminar(id):

    if not session.get("admin"):
        return redirect("/")

    global productos

    productos = [
        p for p in productos
        if p["id"] != id
    ]

    return redirect("/admin")

# ====================================
# EDITAR
# ====================================

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    if not session.get("admin"):
        return redirect("/")

    producto = next(
        (
            p for p in productos
            if p["id"] == id
        ),
        None
    )

    if not producto:
        return redirect("/admin")

    if request.method == "POST":

        producto["nombre"] = request.form["nombre"]
        producto["precio"] = float(
            request.form["precio"]
        )
        producto["coleccion"] = request.form["coleccion"]
        producto["imagen"] = request.form["imagen"]

        return redirect("/admin")

    return render_template(
        "editar.html",
        producto=producto
    )

# ====================================
# LOGOUT
# ====================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# ====================================

if __name__ == "__main__":
    app.run(debug=True)