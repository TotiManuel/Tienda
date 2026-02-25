from models.modulo import Modulo
from extensions import db

def crear_modulos_base():
    modulos = [
        {
            "nombre": "Ventas",
            "codigo": "ventas",
            "descripcion": "Gestión de ventas y facturación",
            "categoria": "ventas",
            "icono": "💰",
            "color": "#10b981",
        },
        {
            "nombre": "CRM",
            "codigo": "crm",
            "descripcion": "Gestión de clientes",
            "categoria": "marketing",
            "icono": "👥",
            "color": "#3b82f6",
        },
        {
            "nombre": "Inventario",
            "codigo": "stock",
            "descripcion": "Control de stock",
            "categoria": "operaciones",
            "icono": "📦",
            "color": "#f59e0b",
        },
    ]

    for m in modulos:
        if not Modulo.query.filter_by(codigo=m["codigo"]).first():
            db.session.add(Modulo(**m))

    db.session.commit()