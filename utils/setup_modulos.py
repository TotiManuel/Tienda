from models.modulo import Modulo
from extensions import db
def crear_modulos_base():
    modulos = [
        {
            "nombre": "Inventario",
            "codigo": "stock",
            "descripcion": "Control de stock",
            "categoria": "operaciones",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Usuarios",
            "codigo": "usuarios",
            "descripcion": "Control de usuarios",
            "categoria": "usuarios",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Modulos",
            "codigo": "admin_modulos",
            "descripcion": "Control de modulos",
            "categoria": "modulos",
            "icono": "📦",
            "color": "#f59e0b",
        },
    ]
    for m in modulos:
        if not Modulo.query.filter_by(codigo=m["codigo"]).first():
            db.session.add(Modulo(**m))
    db.session.commit()


