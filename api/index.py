#region Imports
from flask import Flask, flash, redirect, render_template, request, url_for
from flask import request, render_template,session
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from models.decoradores import permiso_requerido
from models.modulo import Modulo
from utils.setup_modulos import crear_modulos_base
from models.usuario import Usuario
from models import init_db
import sys, os
from extensions import db, login_manager
from models.inventario import Producto, Categoria
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
    from flask import render_template, request, redirect, url_for
    from flask_login import login_required, current_user
    from extensions import db
    from models.inventario import Producto, Empresa


    @app.route("/superadmin/inventario")
    @permiso_requerido('ver_inventario_admin')
    @login_required
    def superadmin_inventario():
        empresa_id = request.args.get("empresa")

        if empresa_id:
            productos = Producto.query.filter_by(
                empresa_id=empresa_id
            ).all()
        else:
            productos = Producto.query.all()

        empresas = Empresa.query.all()

        return render_template(
            "superadmin_inventario.html",
            productos=productos,
            empresas=empresas
        )
    
    @app.route("/superadmin/producto/crear", methods=["POST"])
    @permiso_requerido('crear_producto')
    @login_required
    def superadmin_crear_producto():

        if not current_user.es_superadmin:
            return "No autorizado", 403

        nuevo = Producto(
            empresa_id=request.form["empresa_id"],
            nombre=request.form["nombre"],
            codigo=request.form["codigo"],
            stock=request.form["stock"],
            precio=request.form["precio"]
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("superadmin_inventario"))
    @app.route("/superadmin/producto/eliminar/<int:id>")
    @permiso_requerido('eliminar_producto_admin')
    @login_required
    def superadmin_eliminar_producto(id):

        p = Producto.query.get_or_404(id)
        db.session.delete(p)
        db.session.commit()

        return redirect(url_for("superadmin_inventario"))
    #endregion
    #region Admin
    #endregion
    #region usuario
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