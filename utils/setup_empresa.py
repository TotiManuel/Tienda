from extensions import db
from models.usuario import Rol, Permiso, RolPermiso, UsuarioRol


def crear_estructura_empresa(empresa, usuario):
    """
    🔥 Crea roles y permisos iniciales al registrar una empresa
    """

    # =========================
    # 1. Crear permisos base
    # =========================
    permisos_base = [
        {
            "nombre": "home_empresa_ver",
            "modulo": "dashboard",
            "accion": "ver",
            "descripcion": "Acceso al dashboard"
        }
    ]

    permisos_obj = []

    for p in permisos_base:
        permiso = Permiso.query.filter_by(nombre=p["nombre"]).first()

        if not permiso:
            permiso = Permiso(**p)
            db.session.add(permiso)

        permisos_obj.append(permiso)

    db.session.flush()

    # =========================
    # 2. Crear rol Admin
    # =========================
    rol_admin = Rol(
        empresa_id=empresa.id,
        nombre="Administrador",
        descripcion="Acceso total",
        nivel=100,
        es_sistema=True
    )

    db.session.add(rol_admin)
    db.session.flush()

    # =========================
    # 3. Asignar permisos al rol
    # =========================
    for permiso in permisos_obj:
        rp = RolPermiso(
            rol_id=rol_admin.id,
            permiso_id=permiso.id
        )
        db.session.add(rp)

    # =========================
    # 4. Asignar rol al usuario
    # =========================
    usuario_rol = UsuarioRol(
        usuario_id=usuario.id,
        rol_id=rol_admin.id
    )

    db.session.add(usuario_rol)

    db.session.commit()