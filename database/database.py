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

    # ======================================
    # TABLAS AUXILIARES
    # ======================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS colecciones (

        id SERIAL PRIMARY KEY,

        nombre TEXT NOT NULL

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS ofertas (

        id SERIAL PRIMARY KEY,

        nombre TEXT NOT NULL

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS promociones (

        id SERIAL PRIMARY KEY,

        nombre TEXT NOT NULL

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS descuentos (

        id SERIAL PRIMARY KEY,

        nombre TEXT NOT NULL,

        porcentaje REAL NOT NULL

    )

    """)

    # ======================================
    # PRODUCTOS
    # ======================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS productos (

        id SERIAL PRIMARY KEY,

        nombre TEXT NOT NULL,

        precio REAL NOT NULL,

        genero TEXT,

        imagen TEXT,

        coleccion_id INTEGER REFERENCES colecciones(id),

        oferta_id INTEGER REFERENCES ofertas(id),

        promocion_id INTEGER REFERENCES promociones(id),

        descuento_id INTEGER REFERENCES descuentos(id)

    )

    """)

    # ======================================
    # TALLAS
    # ======================================

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
# OBTENER LISTAS
# ==========================================

def obtener_colecciones():

    conn = conectar()

    cursor = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cursor.execute("SELECT * FROM colecciones")

    datos = cursor.fetchall()

    conn.close()

    return datos

def obtener_ofertas():

    conn = conectar()

    cursor = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cursor.execute("SELECT * FROM ofertas")

    datos = cursor.fetchall()

    conn.close()

    return datos

def obtener_promociones():

    conn = conectar()

    cursor = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cursor.execute("SELECT * FROM promociones")

    datos = cursor.fetchall()

    conn.close()

    return datos

def obtener_descuentos():

    conn = conectar()

    cursor = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cursor.execute("SELECT * FROM descuentos")

    datos = cursor.fetchall()

    conn.close()

    return datos

# ==========================================
# CRUD COLECCIONES
# ==========================================

def crear_coleccion(nombre):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO colecciones (nombre)
    VALUES (%s)

    """, (nombre,))

    conn.commit()

    conn.close()

def eliminar_coleccion(id):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM colecciones
    WHERE id = %s

    """, (id,))

    conn.commit()

    conn.close()

# ==========================================
# CRUD OFERTAS
# ==========================================

def crear_oferta(nombre):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO ofertas (nombre)
    VALUES (%s)

    """, (nombre,))

    conn.commit()

    conn.close()

def eliminar_oferta(id):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM ofertas
    WHERE id = %s

    """, (id,))

    conn.commit()

    conn.close()

# ==========================================
# CRUD PROMOCIONES
# ==========================================

def crear_promocion(nombre):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO promociones (nombre)
    VALUES (%s)

    """, (nombre,))

    conn.commit()

    conn.close()

def eliminar_promocion(id):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM promociones
    WHERE id = %s

    """, (id,))

    conn.commit()

    conn.close()

# ==========================================
# CRUD DESCUENTOS
# ==========================================

def crear_descuento(nombre, porcentaje):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO descuentos (
        nombre,
        porcentaje
    )

    VALUES (%s, %s)

    """, (

        nombre,
        porcentaje

    ))

    conn.commit()

    conn.close()

def eliminar_descuento(id):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM descuentos
    WHERE id = %s

    """, (id,))

    conn.commit()

    conn.close()

# ==========================================
# OBTENER PRODUCTOS
# ==========================================

def obtener_productos():

    conn = conectar()

    cursor = conn.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cursor.execute("""

    SELECT

        productos.*,

        colecciones.nombre AS coleccion,

        ofertas.nombre AS oferta,

        promociones.nombre AS promocion,

        descuentos.nombre AS descuento,

        descuentos.porcentaje AS porcentaje

    FROM productos

    LEFT JOIN colecciones
    ON productos.coleccion_id = colecciones.id

    LEFT JOIN ofertas
    ON productos.oferta_id = ofertas.id

    LEFT JOIN promociones
    ON productos.promocion_id = promociones.id

    LEFT JOIN descuentos
    ON productos.descuento_id = descuentos.id

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

            "genero": p["genero"],

            "imagen": p["imagen"],

            "coleccion": p["coleccion"],

            "oferta": p["oferta"],

            "promocion": p["promocion"],

            "descuento": p["descuento"],

            "porcentaje": p["porcentaje"],

            "tallas": [
                t["talla"]
                for t in tallas
            ]
        })

    conn.close()

    return lista

# ==========================================
# CREAR PRODUCTO
# ==========================================

def crear_producto(

    nombre,
    precio,
    genero,
    imagen,
    tallas,
    coleccion_id,
    oferta_id,
    promocion_id,
    descuento_id

):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO productos (

        nombre,
        precio,
        genero,
        imagen,
        coleccion_id,
        oferta_id,
        promocion_id,
        descuento_id

    )

    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

    RETURNING id

    """, (

        nombre,
        precio,
        genero,
        imagen,
        coleccion_id,
        oferta_id,
        promocion_id,
        descuento_id

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
# EDITAR PRODUCTO
# ==========================================

def editar_producto(

    id,
    nombre,
    precio,
    genero,
    imagen,
    tallas,
    coleccion_id,
    oferta_id,
    promocion_id,
    descuento_id

):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE productos

    SET

        nombre = %s,
        precio = %s,
        genero = %s,
        imagen = %s,
        coleccion_id = %s,
        oferta_id = %s,
        promocion_id = %s,
        descuento_id = %s

    WHERE id = %s

    """, (

        nombre,
        precio,
        genero,
        imagen,
        coleccion_id,
        oferta_id,
        promocion_id,
        descuento_id,
        id

    ))

    # ======================================
    # BORRAR TALLAS VIEJAS
    # ======================================

    cursor.execute("""

    DELETE FROM tallas
    WHERE producto_id = %s

    """, (id,))

    # ======================================
    # CREAR NUEVAS TALLAS
    # ======================================

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
    
# ==========================================
# ELIMINAR PRODUCTO
# ==========================================

def eliminar_producto(id):

    conn = conectar()

    cursor = conn.cursor()

    # ======================================
    # ELIMINAR TALLAS
    # ======================================

    cursor.execute("""

    DELETE FROM tallas
    WHERE producto_id = %s

    """, (id,))

    # ======================================
    # ELIMINAR PRODUCTO
    # ======================================

    cursor.execute("""

    DELETE FROM productos
    WHERE id = %s

    """, (id,))

    conn.commit()

    conn.close()