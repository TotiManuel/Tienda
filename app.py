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
        "tallas": ["S", "M", "L", "XL"],
        "genero": "Unisex",
        "imagen": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab"
    },
    {
        "id": 2,
        "nombre": "Buzo Negro",
        "precio": 28000,
        "coleccion": "Urban",
        "tallas": ["M", "L", "XL"],
        "genero": "Hombre",
        "imagen": "https://images.unsplash.com/photo-1503341504253-dff4815485f1"
    },
    {
        "id": 3,
        "nombre": "Campera Denim",
        "precio": 42000,
        "coleccion": "Classic",
        "tallas": ["S", "M", "L"],
        "genero": "Unisex",
        "imagen": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f"
    },
    {
        "id": 4,
        "nombre": "Pantalón Cargo",
        "precio": 31000,
        "coleccion": "Streetwear",
        "tallas": ["M", "L", "XL"],
        "genero": "Hombre",
        "imagen": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f"
    },
    {
        "id": 5,
        "nombre": "Zapatillas Urban",
        "precio": 55000,
        "coleccion": "Urban",
        "tallas": [38, 39, 40, 41, 42],
        "genero": "Unisex",
        "imagen": "https://images.unsplash.com/photo-1542291026-7eec264c27ff"
    },
    {
        "id": 6,
        "nombre": "Camisa Blanca",
        "precio": 22000,
        "coleccion": "Elegance",
        "tallas": ["S", "M", "L"],
        "genero": "Hombre",
        "imagen": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b"
    },
    {
        "id": 7,
        "nombre": "Jogger Gris",
        "precio": 27000,
        "coleccion": "Sport",
        "tallas": ["M", "L", "XL"],
        "genero": "Unisex",
        "imagen": "https://images.unsplash.com/photo-1506629905607-d9b1c9f9c5d1"
    },
    {
        "id": 8,
        "nombre": "Bermuda Beige",
        "precio": 18000,
        "coleccion": "Summer",
        "tallas": ["S", "M", "L"],
        "genero": "Hombre",
        "imagen": "https://images.unsplash.com/photo-1509631179647-0177331693ae"
    },
    {
        "id": 9,
        "nombre": "Campera Puffer",
        "precio": 65000,
        "coleccion": "Invierno",
        "tallas": ["M", "L", "XL"],
        "genero": "Unisex",
        "imagen": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b"
    },
    {
        "id": 10,
        "nombre": "Remera Estampada",
        "precio": 17000,
        "coleccion": "Streetwear",
        "tallas": ["S", "M", "L", "XL"],
        "genero": "Unisex",
        "imagen": "https://images.unsplash.com/photo-1483985988355-763728e1935b"
    },
    {
        "id": 11,
        "nombre": "Sweater Lana",
        "precio": 34000,
        "coleccion": "Winter",
        "tallas": ["S", "M", "L"],
        "genero": "Mujer",
        "imagen": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1"
    },
    {
        "id": 12,
        "nombre": "Top Deportivo",
        "precio": 14000,
        "coleccion": "Sport",
        "tallas": ["XS", "S", "M"],
        "genero": "Mujer",
        "imagen": "https://images.unsplash.com/photo-1517841905240-472988babdf9"
    },
    {
        "id": 13,
        "nombre": "Jean Slim Fit",
        "precio": 36000,
        "coleccion": "Classic",
        "tallas": [38, 40, 42, 44],
        "genero": "Hombre",
        "imagen": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246"
    },
    {
        "id": 14,
        "nombre": "Hoodie Oversize",
        "precio": 39000,
        "coleccion": "Urban",
        "tallas": ["M", "L", "XL"],
        "genero": "Unisex",
        "imagen": "https://images.unsplash.com/photo-1523398002811-999ca8dec234"
    },
    {
        "id": 15,
        "nombre": "Vestido Casual",
        "precio": 33000,
        "coleccion": "Summer",
        "tallas": ["S", "M", "L"],
        "genero": "Mujer",
        "imagen": "https://images.unsplash.com/photo-1496747611176-843222e1e57c"
    },
    {
        "id": 16,
        "nombre": "Blazer Negro",
        "precio": 58000,
        "coleccion": "Elegance",
        "tallas": ["S", "M", "L"],
        "genero": "Hombre",
        "imagen": "https://images.unsplash.com/photo-1507679799987-c73779587ccf"
    },
    {
        "id": 17,
        "nombre": "Pollera Tableada",
        "precio": 24000,
        "coleccion": "Classic",
        "tallas": ["XS", "S", "M"],
        "genero": "Mujer",
        "imagen": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f"
    },
    {
        "id": 18,
        "nombre": "Chaleco Puff",
        "precio": 37000,
        "coleccion": "Winter",
        "tallas": ["M", "L"],
        "genero": "Unisex",
        "imagen": "https://images.unsplash.com/photo-1495121605193-b116b5b9c5fe"
    },
    {
        "id": 19,
        "nombre": "Conjunto Deportivo",
        "precio": 49000,
        "coleccion": "Sport",
        "tallas": ["S", "M", "L", "XL"],
        "genero": "Unisex",
        "imagen": "https://images.unsplash.com/photo-1514996937319-344454492b37"
    },
    {
        "id": 20,
        "nombre": "Campera Cuero",
        "precio": 72000,
        "coleccion": "Luxury",
        "tallas": ["M", "L", "XL"],
        "genero": "Hombre",
        "imagen": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b"
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
    
@app.route("/atencion_cliente")
def atencion_cliente():

    return render_template(
        "atencion_cliente.html"
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
                p for p in productos
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
        productos_tienda=productos
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
        producto["precio"] = int(
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