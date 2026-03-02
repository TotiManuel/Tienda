#region Imports
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask import request, render_template,session
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from models.decoradores import permiso_requerido, superadmin_required
from models.modulo import Modulo
from utils.setup_modulos import crear_modulos_base
from models.usuario import Usuario
from models import init_db
import sys, os
from extensions import db, login_manager
from flask_login import current_user
from models.inventario import Producto
#endregion

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

#region app
def create_app():
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
    login_manager.init_app(app)
    login_manager.login_view = "login_register"
    
    with app.app_context():
        init_db()
        if not Usuario.query.filter_by(rol='superadmin').first():
            superadmin = Usuario(nombre='Julian', apellido='Mandaio', email='manuel.mandaio@gmail.com', empresa='Toti', rol='superadmin')
            superadmin.set_password('41323167')
            db.session.add(superadmin)
            db.session.commit()
        crear_modulos_base()
    #endregion
    #region Landing
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    @app.route("/")
    def home():
        return render_template("index.html")
    @app.route("/funciones")
    def funciones():
        return render_template("index.html")
    @app.route("/precios")
    def precios():
        return render_template("index.html")
    @app.route("/contacto")
    def contacto():
        return render_template("index.html")

    @app.route("/dashboard")
    @permiso_requerido('ver_dashboard')
    @login_required
    def dashboard():
        modulos = Modulo.query.all()
        return render_template("dashboard.html", modulos=modulos)
    #endregion
    #region SuperAdmin
    @app.route("/inventario")
    @login_required
    @superadmin_required
    def inventario():

        empresa_id = request.args.get("empresa", type=int)

        empresas = Usuario.query.filter_by(rol="empresa").all()

        query = Producto.query

        # 🔥 CORRECCIÓN: filtrar por empresa_id (no usuario_id)
        if empresa_id:
            query = query.filter_by(empresa_id=empresa_id)

        productos = query.all()

        return render_template(
            "inventario.html",
            productos=productos,
            empresas=empresas
        )
    @app.route("/superadmin/producto/crear", methods=["POST"])
    @login_required
    @superadmin_required
    def superadmin_crear_producto():

        empresa_id = int(request.form["empresa_id"])

        nuevo = Producto(
            nombre=request.form["nombre"],
            codigo=request.form.get("codigo"),
            stock=int(request.form.get("stock", 0)),
            precio=float(request.form.get("precio", 0)),
            empresa_id=empresa_id,          # 🔥 CORRECCIÓN
            usuario_id=current_user.id      # opcional: quién lo creó
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("superadmin_inventario"))
    @app.route("/superadmin/producto/eliminar/<int:id>")
    @login_required
    @superadmin_required
    def superadmin_eliminar_producto(id):

        producto = Producto.query.get_or_404(id)

        db.session.delete(producto)
        db.session.commit()

        return redirect(url_for("superadmin_inventario"))    
    #endregion
    #region Empresa
    #endregion
    #region Empleado
    #region Login
    @app.route("/login_register")
    def login_register():
        return render_template("login_register.html")
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get("email")
            password = request.form.get("password")
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario and check_password_hash(usuario.password, password):
                login_user(usuario)
                return redirect(url_for("dashboard"))
            else:
                flash("Email o contraseña incorrectos")
        return render_template('login_register.html')
    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            password = request.form['password']
            empresa = request.form['empresa']
            rol = request.form.get("rol")
            if Usuario.query.filter_by(email=email).first():
                flash("El email ya existe")
                return redirect(url_for("login_register"))

            usuario = Usuario(
                nombre=nombre,
                apellido=apellido,
                email=email,
                empresa=empresa,
                rol=rol
            )

            # 🔐 HASH obligatorio
            usuario.set_password(password)

            db.session.add(usuario)
            db.session.commit()

            return redirect(url_for("login_register"))  # 🔥 redirigir
        return render_template('login_register.html')
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Sesión cerrada correctamente")
        return redirect(url_for("login_register"))
    #endregion
    return app
#endregion
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)    
    
#region permisosHTML
'''
                <!--{% if usuario.tiene_permiso("gestionar_usuarios") %}
                        <a href="/usuarios">Usuarios</a>
                    {% endif %} -->
'''
#endregion