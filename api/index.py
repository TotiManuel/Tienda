#region Imports
from flask import Flask, render_template, request
from flask import request, render_template, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models.usuario import Usuario
from models import init_db
import sys, os
from extensions import db
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

    # 🔥 Crear tablas automáticamente
    with app.app_context():
        init_db()
    #endregion
    #region Landing
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

                return render_template('/index.html')

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
            usuario = Usuario(nombre=nombre, apellido=apellido, email=email, password=password, empresa=empresa)
            db.session.add(usuario)
            db.session.commit()
        return render_template('login_register.html')
    return app
#endregion
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)    