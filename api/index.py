#region Imports
from flask import Flask, render_template, request, redirect, url_for, session
from models.usuario import Rol, UsuarioRol
from models.modulo import EmpresaModulo, Modulo
from models import init_db, Usuario, Empresa
from models.permissions import permiso_requerido
from werkzeug.security import generate_password_hash, check_password_hash
import sys, os
from extensions import db
from utils.setup_empresa import crear_estructura_empresa
from utils.setup_modulos import crear_modulos_base
from utils.setup_superadmin import crear_superadmin_automatico
from werkzeug.security import generate_password_hash
from datetime import datetime
#endregion
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
#region app
def create_app():

    def crear_superadmin_automatico():

        # 🔹 1. Verificar si ya existe un rol nivel 100
        rol_superadmin = Rol.query.filter_by(nivel=100).first()

        if not rol_superadmin:
            rol_superadmin = Rol(
                nombre="SuperAdmin",
                descripcion="Acceso total al sistema",
                nivel=100
            )
            db.session.add(rol_superadmin)
            db.session.commit()

        # 🔹 2. Verificar si ya existe un usuario con ese rol
        existe = (
            db.session.query(Usuario)
            .join(UsuarioRol)
            .join(Rol)
            .filter(Rol.nivel == 100)
            .first()
        )

        if existe:
            return  # 🔥 Ya hay superadmin, no hacemos nada

        # 🔹 3. Crear empresa sistema si no existe
        empresa_sistema = Empresa.query.filter_by(nombre="Sistema").first()

        if not empresa_sistema:
            empresa_sistema = Empresa(
                nombre="Sistema",
                activa=True,
                fecha_creacion=datetime.utcnow()
            )
            db.session.add(empresa_sistema)
            db.session.commit()

        # 🔹 4. Crear usuario superadmin
        admin = Usuario(
            empresa_id=empresa_sistema.id,
            nombre="Super",
            apellido="Admin",
            email="admin@tusistema.com",
            password=generate_password_hash("Admin123!"),
            verificado=True,
            activo=True,
            fecha_creacion=datetime.utcnow()
        )

        db.session.add(admin)
        db.session.commit()

        # 🔹 5. Asignar rol
        usuario_rol = UsuarioRol(
            usuario_id=admin.id,
            rol_id=rol_superadmin.id
        )

        db.session.add(usuario_rol)
        db.session.commit()

        print("🔥 Superadmin creado automáticamente")
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )
    #region Database
    app.secret_key = "supersecretkey"

    # 🔥 DATABASE (Vercel o local)
    database_url = os.getenv("DATABASE_URL", "sqlite:///database.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # 🔥 Crear tablas automáticamente
    with app.app_context():
        init_db()
        crear_modulos_base()
        crear_superadmin_automatico()
    #endregion
    #region Landing
    @app.route("/")
    def home():
        return render_template("index.html")
    #endregion
    #region Registro
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":

            # 🔹 Usuario
            nombre = request.form["nombre"]
            email = request.form["email"]
            password = request.form["password"]

            # 🔹 Empresa
            empresa_nombre = request.form["empresa"]
            nombre_legal = request.form.get("nombre_legal")
            cuit_rut = request.form.get("cuit_rut")
            tipo_empresa = request.form.get("tipo_empresa")
            industria = request.form.get("industria")

            # 🔥 Crear empresa completa
            empresa = Empresa(
                nombre=empresa_nombre,
                nombre_legal=nombre_legal,
                cuit_rut=cuit_rut,
                tipo_empresa=tipo_empresa,
                industria=industria
            )

            db.session.add(empresa)
            db.session.flush()

            # 🔹 Crear usuario
            usuario = Usuario(
                nombre=nombre,
                email=email,
                password=generate_password_hash(password),
                empresa_id=empresa.id
            )

            db.session.add(usuario)
            db.session.flush()

            # 🔥 Crear estructura base SaaS
            crear_estructura_empresa(empresa, usuario)

            db.session.commit()

            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            usuario = Usuario.query.filter_by(email=email).first()

            if usuario and check_password_hash(usuario.password, password):
                session["usuario_id"] = usuario.id
                session["empresa_id"] = usuario.empresa_id
                session["usuario_nombre"] = usuario.nombre
                return redirect(url_for("empresa_home"))

            return "Usuario o contraseña incorrecta"

        return render_template("login.html")
        # ===== Logout =====
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))
    #endregion
    #region Dashboard 
    @app.route("/empresa")
    @permiso_requerido("home_empresa_ver")
    def empresa_home():

        if "usuario_id" not in session:
            return redirect(url_for("login"))

        empresa = Empresa.query.get(session["empresa_id"])
        usuario = Usuario.query.get(session["usuario_id"])

        modulos = usuario.obtener_modulos_disponibles()

        return render_template(
            "empresa_home.html",
            empresa_nombre=empresa.nombre if empresa else "",
            usuario_nombre=session["usuario_nombre"],
            modulos=modulos,
            empresa_id=session["empresa_id"]  # 🔥 clave
        )
    #endregion
    #region Admin
    @app.route("/admin/empresas")
    def admin_empresas():
        usuario = Usuario.query.get(session["usuario_id"])

        if not usuario.es_superadmin():
            return "No autorizado"

        empresas = Empresa.query.all()

        return render_template(
            "admin_empresas.html",
            empresas=empresas
        )
    
    @app.route("/admin/empresa/<int:empresa_id>/modulos")
    def admin_modulos_empresa(empresa_id):

        usuario = Usuario.query.get(session["usuario_id"])

        if not usuario.es_superadmin():
            return "No autorizado"

        modulos = Modulo.query.all()

        empresa_modulos = EmpresaModulo.query.filter_by(
            empresa_id=empresa_id
        ).all()

        # 🔥 Diccionario rápido
        estados = {em.modulo_id: em.activo for em in empresa_modulos}

        return render_template(
            "admin_modulos.html",
            modulos=modulos,
            estados=estados,
            empresa_id=empresa_id
        )
    
    @app.route("/admin/empresa/<int:empresa_id>/modulo/<int:modulo_id>/toggle")
    def toggle_modulo(empresa_id, modulo_id):

        usuario = Usuario.query.get(session["usuario_id"])

        if not usuario.es_superadmin():
            return "No autorizado"

        em = EmpresaModulo.query.filter_by(
            empresa_id=empresa_id,
            modulo_id=modulo_id
        ).first()

        # 🔥 Si no existe, crearlo
        if not em:
            em = EmpresaModulo(
                empresa_id=empresa_id,
                modulo_id=modulo_id,
                activo=True
            )
            db.session.add(em)
        else:
            em.activo = not em.activo

        db.session.commit()

        return redirect(request.referrer)
    #endregion
    return app
#endregion
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)    