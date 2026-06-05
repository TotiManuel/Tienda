import psycopg2
import psycopg2.extras
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

# ==========================================
# CONEXION
# ==========================================

def conectar():

    conn = psycopg2.connect(DATABASE_URL)

    return conn

# ==========================================
# CREAR TABLAS
# ==========================================

def crear_tablas():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS productos (

        id SERIAL PRIMARY KEY,

        nombre TEXT NOT NULL,

        precio REAL NOT NULL,

        coleccion TEXT,

        genero TEXT,

        imagen TEXT

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS tallas (

        id SERIAL PRIMARY KEY,

        producto_id INTEGER REFERENCES productos(id),

        talla TEXT

    )

    """)

    conn.commit()

    conn.close()

# ==========================================
# OBTENER PRODUCTOS
# ==========================================

def obtener_productos():

    conn = conectar()

    cursor = conn.cursor(
        cursor_factory=
        psycopg2.extras.RealDictCursor
    )

    cursor.execute("""

    SELECT *
    FROM productos

    """)

    productos = cursor.fetchall()

    lista = []

    for p in productos:

        cursor.execute("""

        SELECT talla
        FROM tallas
        WHERE producto_id = %s

        """, (p["id"],))

        tallas = cursor.fetchall()

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

    cursor = conn.cursor(
        cursor_factory=
        psycopg2.extras.RealDictCursor
    )

    cursor.execute("""

    SELECT *
    FROM productos
    WHERE id = %s

    """, (id,))

    p = cursor.fetchone()

    if not p:

        return None

    cursor.execute("""

    SELECT talla
    FROM tallas
    WHERE producto_id = %s

    """, (id,))

    tallas = cursor.fetchall()

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

    VALUES (%s, %s, %s, %s, %s)

    RETURNING id

    """, (

        nombre,
        precio,
        coleccion,
        genero,
        imagen

    ))

    producto_id = cursor.fetchone()[0]

    for t in tallas:

        cursor.execute("""

        INSERT INTO tallas (

            producto_id,
            talla

        )

        VALUES (%s, %s)

        """, (

            producto_id,
            t.strip()

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
    WHERE producto_id = %s

    """, (id,))

    cursor.execute("""

    DELETE FROM productos
    WHERE id = %s

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

        nombre = %s,
        precio = %s,
        coleccion = %s,
        genero = %s,
        imagen = %s

    WHERE id = %s

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
    WHERE producto_id = %s

    """, (id,))

    for t in tallas:

        cursor.execute("""

        INSERT INTO tallas (

            producto_id,
            talla

        )

        VALUES (%s, %s)

        """, (

            id,
            t.strip()

        ))

    conn.commit()

    conn.close()