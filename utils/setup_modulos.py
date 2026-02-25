from models.modulo import Modulo
from extensions import db
from models import init_db

from models import init_db
from models.modulo import Modulo
from extensions import db

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
            {
                "nombre": "Finanzas",
                "codigo": "finanzas",
                "descripcion": "Contabilidad y reportes",
                "categoria": "finanzas",
                "icono": "📊",
                "color": "#ef4444",
            },
            {
                "nombre": "Marketing",
                "codigo": "marketing",
                "descripcion": "Automatización y campañas",
                "categoria": "marketing",
                "icono": "📢",
                "color": "#8b5cf6",
            },
            {
                "nombre": "Turnos",
                "codigo": "turnos",
                "descripcion": "Agenda y reservas",
                "categoria": "operaciones",
                "icono": "📅",
                "color": "#06b6d4",
            },
            {
                "nombre": "RRHH",
                "codigo": "rrhh",
                "descripcion": "Gestión de empleados",
                "categoria": "empresa",
                "icono": "🧑‍💼",
                "color": "#6366f1",
            },
            {
                "nombre": "Documentos",
                "codigo": "documentos",
                "descripcion": "Gestión documental",
                "categoria": "empresa",
                "icono": "📂",
                "color": "#14b8a6",
            },
        ]
for m in modulos:
    if not Modulo.query.filter_by(codigo=m["codigo"]).first():
        db.session.add(Modulo(**m))
db.session.commit()