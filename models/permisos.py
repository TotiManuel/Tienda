PERMISOS = {

    # 👑 SUPERADMIN (control total del sistema)
    "superadmin": [
        "ver_dashboard",

        # Inventario global
        "ver_inventario_global",
        "crear_producto_global",
        "eliminar_producto_global",
        "editar_producto_global",

        # Empresas
        "gestionar_empresas",

        # Usuarios
        "gestionar_usuarios",

        # Sistema
        "ver_reportes",
        "configuracion"
    ],

    # 🏢 EMPRESA (dueño del negocio)
    "empresa": [
        "ver_dashboard",

        # Inventario propio
        "ver_inventario",
        "crear_producto",
        "editar_producto",
        "eliminar_producto",

        # Módulos negocio
        "ver_ventas",
        "ver_clientes",
        "ver_reportes",

        # Gestión interna
        "gestionar_usuarios"
    ],

    # 👨‍💼 EMPLEADO (acceso limitado)
    "empleado": [
        "ver_dashboard",
        "ver_ventas",
        "ver_clientes"
    ],

    # 👤 CLIENTE (futuro portal)
    "cliente": [
        "ver_dashboard"
    ]
}