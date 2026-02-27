#region Imports
from flask import Flask, flash, redirect, render_template, request, url_for
from flask import request, render_template,session
from flask_login import login_required, logout_user
from werkzeug.security import check_password_hash
from models.decoradores import permiso_requerido
from models.usuario import Usuario
from models import init_db
import sys, os
from extensions import db, login_manager
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
    
    with app.app_context():
        init_db()
        if not Usuario.query.filter_by(rol='admin').first():
            admin = Usuario(nombre='Julian', apellido='Mandaio', email='manuel.mandaio@gmail.com', empresa='Toti', rol='admin')
            admin.set_password('41323167')
            db.session.add(admin)
            db.session.commit()
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
    def dashboard():
        return render_template("dashboard.html")
    
    @app.route("/login_register")
    def login_register():
        return render_template("login_register.html")
    #endregion
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':

            email = request.form.get("email")
            password = request.form.get("password")

            # 🔎 Buscar usuario
            usuario = Usuario.query.filter_by(email=email).first()

            # 🔐 Validar usuario y contraseña
            if usuario and check_password_hash(usuario.password, password):

                # 🧠 Guardar sesión
                session["usuario_id"] = usuario.id
                session["usuario_nombre"] = usuario.nombre
                session["empresa"] = usuario.empresa
                if usuario.rol == 'admin':
                    return render_template('/dashboard.html')
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
            usuario = Usuario(nombre=nombre, apellido=apellido, email=email, password=password, empresa=empresa, rol=rol)
            db.session.add(usuario)
            db.session.commit()
        return render_template('login_register.html')
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Sesión cerrada correctamente")
        return render_template('login_register.html')
    
    return app
#endregion
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)    