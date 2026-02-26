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
            "nombre": "Empresas",
            "codigo": "empresas",
            "descripcion": "Gestión de empresas",
            "categoria": "empresas",
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
            "nombre": "Usuarios",
            "codigo": "usuarios",
            "descripcion": "Control de usuarios",
            "categoria": "usuarios",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Seguridad",
            "codigo": "seguridad",
            "descripcion": "Control de seguridad",
            "categoria": "seguridad",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Planes y pagos",
            "codigo": "planesypagos",
            "descripcion": "Control de Planes y pagos",
            "categoria": "Planes y Pagos",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Modulos",
            "codigo": "admin_modulos.html",
            "descripcion": "Control de modulos",
            "categoria": "modulos",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Configuracion Empresas",
            "codigo": "configuracionEmpresas",
            "descripcion": "Control de configuracion de empresas",
            "categoria": "configuraciones",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Auditoria",
            "codigo": "auditoria",
            "descripcion": "Control de auditoria",
            "categoria": "auditoria",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Compras",
            "codigo": "compras",
            "descripcion": "Control de compras",
            "categoria": "compras",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Finanzas",
            "codigo": "finanzas",
            "descripcion": "Control de finanzas",
            "categoria": "finanzas",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Turnos y Calendarios",
            "codigo": "TurnosYCalendarios",
            "descripcion": "Control de turnos y calendarios",
            "categoria": "turnos y calendarios",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Documentos",
            "codigo": "documentos",
            "descripcion": "Control de documentos",
            "categoria": "documentacion",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Web y Ecommerce",
            "codigo": "webEcommerce",
            "descripcion": "Control de web y ecommerce",
            "categoria": "web y ecommerce",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Recursos Humanos",
            "codigo": "recursosHumanos",
            "descripcion": "Control de Recursos Humanos",
            "categoria": "recursos humanos",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Analiticas",
            "codigo": "analiticas",
            "descripcion": "Control de analiticas",
            "categoria": "analiticas",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "IA y Automatizacion",
            "codigo": "IAyAutomatizacion",
            "descripcion": "Control de Ia y automatizacion",
            "categoria": "Ia y Automatizacion",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Integraciones",
            "codigo": "integraciones",
            "descripcion": "Control de integraciones",
            "categoria": "integraciones",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Marketing",
            "codigo": "marketing",
            "descripcion": "Control de Marketing",
            "categoria": "marketing",
            "icono": "📦",
            "color": "#f59e0b",
        },
        {
            "nombre": "Ventajas Competitivas",
            "codigo": "ventajasCompetitivas",
            "descripcion": "Control de ventajas competitivas",
            "categoria": "ventajas Competitivas",
            "icono": "📦",
            "color": "#f59e0b",
        },
    ]

    for m in modulos:
        if not Modulo.query.filter_by(codigo=m["codigo"]).first():
            db.session.add(Modulo(**m))
    db.session.commit()












