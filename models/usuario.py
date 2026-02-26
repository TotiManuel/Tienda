from datetime import datetime
from extensions import db
from models.modulo import Modulo, EmpresaModulo

# ==============================
# USUARIO
# ==============================

class Usuario(db.Model):
    __tablename__ = "usuarios"

    # 🔹 Identificación
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    # 🔹 Datos personales
    nombre = db.Column(db.String(120))
    apellido = db.Column(db.String(120))
    email = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(50))
    avatar = db.Column(db.String(300))

    # 🔹 Autenticación
    password = db.Column(db.String(255), nullable=False)
    verificado = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    bloqueado = db.Column(db.Boolean, default=False)
    motivo_bloqueo = db.Column(db.String(200))

    # 🔹 Seguridad avanzada
    doble_factor = db.Column(db.Boolean, default=False)
    secreto_2fa = db.Column(db.String(255))
    ultimo_login = db.Column(db.DateTime)
    ip_ultimo_login = db.Column(db.String(100))
    intentos_fallidos = db.Column(db.Integer, default=0)

    # 🔹 Tokens
    token_recuperacion = db.Column(db.String(255))
    expiracion_token = db.Column(db.DateTime)
    token_api = db.Column(db.String(255))

    # 🔹 Configuración
    idioma = db.Column(db.String(10))
    zona_horaria = db.Column(db.String(50))
    tema = db.Column(db.String(50))

    # 🔹 Datos internos SaaS
    origen_registro = db.Column(db.String(100))
    invitado_por = db.Column(db.Integer)

    # 🔹 Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # 🔹 Relaciones
    roles = db.relationship("UsuarioRol", back_populates="usuario", cascade="all, delete-orphan")

    # ==============================
    # 🔐 MÉTODOS PROFESIONALES
    # ==============================

    def obtener_roles(self):
        return [ur.rol for ur in self.roles]

    def obtener_permisos(self):
        permisos = set()
        for ur in self.roles:
            for rp in ur.rol.permisos:
                permisos.add(rp.permiso.nombre)
        return permisos

    def tiene_permiso(self, permiso_nombre):
        return permiso_nombre in self.obtener_permisos()

    def es_superadmin(self):
        for ur in self.roles:
            if ur.rol.nivel == 100:
                return True
        return False
    
    def obtener_modulos_disponibles(self):
        # 🔥 Superadmin ve todo
        if self.es_superadmin():
            return Modulo.query.filter_by(activo=True, visible=True).all()

        # 🔥 Empresas solo sus módulos activos
        modulos = (
            db.session.query(Modulo)
            .join(EmpresaModulo, EmpresaModulo.modulo_id == Modulo.id)
            .filter(
                EmpresaModulo.empresa_id == self.empresa_id,
                EmpresaModulo.activo == True,
                Modulo.visible == True
            )
            .all()
        )

        return modulos

# ==============================
# ROL
# ==============================

class Rol(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"))

    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))

    # 🔹 Jerarquía (más alto = más poder)
    nivel = db.Column(db.Integer)

    es_sistema = db.Column(db.Boolean, default=False)

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    usuarios = db.relationship("UsuarioRol", back_populates="rol")
    permisos = db.relationship("RolPermiso", back_populates="rol")


# ==============================
# PERMISO
# ==============================

class Permiso(db.Model):
    __tablename__ = "permisos"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(150), unique=True, nullable=False)
    modulo = db.Column(db.String(100))
    descripcion = db.Column(db.String(200))
    accion = db.Column(db.String(50))  # ver, crear, editar, eliminar

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    roles = db.relationship("RolPermiso", back_populates="permiso")


# ==============================
# USUARIO - ROL
# ==============================

class UsuarioRol(db.Model):
    __tablename__ = "usuarios_roles"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    rol_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship("Usuario", back_populates="roles")
    rol = db.relationship("Rol", back_populates="usuarios")


# ==============================
# ROL - PERMISO
# ==============================

class RolPermiso(db.Model):
    __tablename__ = "roles_permisos"

    id = db.Column(db.Integer, primary_key=True)
    rol_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    permiso_id = db.Column(db.Integer, db.ForeignKey("permisos.id"))

    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow)

    rol = db.relationship("Rol", back_populates="permisos")
    permiso = db.relationship("Permiso", back_populates="roles")