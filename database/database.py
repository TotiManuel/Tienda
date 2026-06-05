import sqlite3

DB = "database/base.db"

# ==========================================
# CONEXION
# ==========================================

def conectar():

    conn = sqlite3.connect(DB)

    conn.row_factory = sqlite3.Row

    return conn

# ==========================================
# CREAR TABLAS
# ==========================================

def crear_tablas():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS productos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT NOT NULL,

        precio REAL NOT NULL,

        coleccion TEXT,

        genero TEXT,

        imagen TEXT

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS tallas (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        producto_id INTEGER,

        talla TEXT,

        FOREIGN KEY(producto_id)
        REFERENCES productos(id)

    )

    """)

    conn.commit()

    conn.close()

# ==========================================
# OBTENER PRODUCTOS
# ==========================================

def obtener_productos():

    conn = conectar()

    cursor = conn.cursor()

    productos = cursor.execute("""

    SELECT *
    FROM productos

    """).fetchall()

    lista = []

    for p in productos:

        tallas = cursor.execute("""

        SELECT talla
        FROM tallas
        WHERE producto_id = ?

        """, (p["id"],)).fetchall()

        lista.append({

            "id": p["id"],

            "nombre": p["nombre"],

            "precio": p["precio"],

            "coleccion": p["coleccion"],

            "genero": p["genero"],

            "imagen": p["imagen"],

            "tallas": [
                t["talla"]
                for t in tallas
            ]
        })

    conn.close()

    return lista

# ==========================================
# OBTENER PRODUCTO
# ==========================================

def obtener_producto(id):

    conn = conectar()

    cursor = conn.cursor()

    p = cursor.execute("""

    SELECT *
    FROM productos
    WHERE id = ?

    """, (id,)).fetchone()

    if not p:

        return None

    tallas = cursor.execute("""

    SELECT talla
    FROM tallas
    WHERE producto_id = ?

    """, (id,)).fetchall()

    producto = {

        "id": p["id"],

        "nombre": p["nombre"],

        "precio": p["precio"],

        "coleccion": p["coleccion"],

        "genero": p["genero"],

        "imagen": p["imagen"],

        "tallas": [
            t["talla"]
            for t in tallas
        ]
    }

    conn.close()

    return producto

# ==========================================
# CREAR PRODUCTO
# ==========================================

def crear_producto(

    nombre,
    precio,
    coleccion,
    genero,
    imagen,
    tallas

):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO productos (

        nombre,
        precio,
        coleccion,
        genero,
        imagen

    )

    VALUES (?, ?, ?, ?, ?)

    """, (

        nombre,
        precio,
        coleccion,
        genero,
        imagen

    ))

    producto_id = cursor.lastrowid

    for t in tallas:

        cursor.execute("""

        INSERT INTO tallas (

            producto_id,
            talla

        )

        VALUES (?, ?)

        """, (

            producto_id,
            t

        ))

    conn.commit()

    conn.close()

# ==========================================
# ELIMINAR PRODUCTO
# ==========================================

def eliminar_producto(id):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM tallas
    WHERE producto_id = ?

    """, (id,))

    cursor.execute("""

    DELETE FROM productos
    WHERE id = ?

    """, (id,))

    conn.commit()

    conn.close()

# ==========================================
# EDITAR PRODUCTO
# ==========================================

def editar_producto(

    id,
    nombre,
    precio,
    coleccion,
    genero,
    imagen,
    tallas

):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE productos

    SET

        nombre = ?,
        precio = ?,
        coleccion = ?,
        genero = ?,
        imagen = ?

    WHERE id = ?

    """, (

        nombre,
        precio,
        coleccion,
        genero,
        imagen,
        id

    ))

    cursor.execute("""

    DELETE FROM tallas
    WHERE producto_id = ?

    """, (id,))

    for t in tallas:

        cursor.execute("""

        INSERT INTO tallas (

            producto_id,
            talla

        )

        VALUES (?, ?)

        """, (

            id,
            t

        ))

    conn.commit()

    conn.close()