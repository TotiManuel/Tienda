from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash
)

import sqlite3
import os

app = Flask(__name__)

# =========================
# CONFIG
# =========================

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "clave_super_secreta"
)

ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin123"

DATABASE = "database.db"

# =========================
# DATABASE
# =========================

def conectar():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn

def crear_tablas():

    conn = conectar()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        coleccion TEXT NOT NULL,
        imagen TEXT
    )
    """)

    conn.commit()

    conn.close()

crear_tablas()

# =========================
# HOME
# =========================

@app.route("/")
def index():

    conn = conectar()

    productos = conn.execute("""
        SELECT * FROM productos
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        productos=productos
    )

# =========================
# CARRITO
# =========================

@app.route("/agregar/<int:id>")
def agregar(id):

    carrito = session.get("carrito", [])

    carrito.append(id)

    session["carrito"] = carrito

    flash("Producto agregado")

    return redirect("/")

@app.route("/carrito")
def carrito():

    carrito_ids = session.get("carrito", [])

    productos = []

    conn = conectar()

    for producto_id in carrito_ids:

        producto = conn.execute(
            "SELECT * FROM productos WHERE id = ?",
            (producto_id,)
        ).fetchone()

        if producto:
            productos.append(producto)

    conn.close()

    total = sum(p["precio"] for p in productos)

    return render_template(
        "carrito.html",
        productos=productos,
        total=total
    )

@app.route("/quitar/<int:index>")
def quitar(index):

    carrito = session.get("carrito", [])

    if 0 <= index < len(carrito):
        carrito.pop(index)

    session["carrito"] = carrito

    return redirect("/carrito")

# =========================
# LOGIN ADMIN
# =========================

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

        flash("Datos incorrectos")

    return render_template("login.html")

# =========================
# PANEL ADMIN
# =========================

@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/panel-privado")

    conn = conectar()

    productos = conn.execute("""
        SELECT * FROM productos
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        productos=productos
    )

# =========================
# CREAR PRODUCTO
# =========================

@app.route("/crear", methods=["POST"])
def crear():

    if not session.get("admin"):
        return redirect("/")

    nombre = request.form["nombre"]
    precio = request.form["precio"]
    coleccion = request.form["coleccion"]
    imagen = request.form["imagen"]

    conn = conectar()

    conn.execute("""
        INSERT INTO productos
        (nombre, precio, coleccion, imagen)
        VALUES (?, ?, ?, ?)
    """, (
        nombre,
        precio,
        coleccion,
        imagen
    ))

    conn.commit()

    conn.close()

    flash("Producto creado")

    return redirect("/admin")

# =========================
# EDITAR
# =========================

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    if not session.get("admin"):
        return redirect("/")

    conn = conectar()

    producto = conn.execute(
        "SELECT * FROM productos WHERE id = ?",
        (id,)
    ).fetchone()

    if not producto:

        conn.close()

        return redirect("/admin")

    if request.method == "POST":

        nombre = request.form["nombre"]
        precio = request.form["precio"]
        coleccion = request.form["coleccion"]
        imagen = request.form["imagen"]

        conn.execute("""
            UPDATE productos
            SET nombre = ?,
                precio = ?,
                coleccion = ?,
                imagen = ?
            WHERE id = ?
        """, (
            nombre,
            precio,
            coleccion,
            imagen,
            id
        ))

        conn.commit()

        conn.close()

        flash("Producto actualizado")

        return redirect("/admin")

    conn.close()

    return render_template(
        "editar.html",
        producto=producto
    )

# =========================
# ELIMINAR
# =========================

@app.route("/eliminar/<int:id>")
def eliminar(id):

    if not session.get("admin"):
        return redirect("/")

    conn = conectar()

    conn.execute(
        "DELETE FROM productos WHERE id = ?",
        (id,)
    )

    conn.commit()

    conn.close()

    flash("Producto eliminado")

    return redirect("/admin")

# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# =========================

if __name__ == "__main__":
    app.run(debug=True)