from flask import Flask, render_template, request, redirect, url_for, session
from models import init_db, Usuario, Empresa
from models.permissions import permiso_requerido
from werkzeug.security import generate_password_hash, check_password_hash
import sys, os
from extensions import db
from utils.setup_empresa import crear_estructura_empresa
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    app.secret_key = "supersecretkey"

    # 🔥 DATABASE (Vercel o local)
    database_url = os.getenv("DATABASE_URL", "sqlite:///database.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # 🔥 Crear tablas automáticamente
    with app.app_context():
        init_db()

    # ===== Landing =====
    @app.route("/")
    def home():
        return render_template("index.html")

    # ===== Registro =====
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            nombre = request.form["nombre"]
            email = request.form["email"]
            password = request.form["password"]
            empresa_nombre = request.form["empresa"]

            # Crear empresa
            empresa = Empresa(nombre=empresa_nombre)
            db.session.add(empresa)
            db.session.flush()

            # Crear usuario
            usuario = Usuario(
                nombre=nombre,
                email=email,
                password=generate_password_hash(password),
                empresa_id=empresa.id
            )
            db.session.add(usuario)
            db.session.flush()

            # 🔥 Crear estructura base
            crear_estructura_empresa(empresa, usuario)

            return redirect(url_for("login"))

        return render_template("register.html")

    # ===== Login =====
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

    # ===== Dashboard =====
    @app.route("/empresa")
    @permiso_requerido("home_empresa_ver")
    def empresa_home():
        if "usuario_id" not in session:
            return redirect(url_for("login"))

        empresa = Empresa.query.get(session["empresa_id"])

        return render_template(
            "empresa_home.html",
            empresa_nombre=empresa.nombre if empresa else "",
            usuario_nombre=session["usuario_nombre"]
        )

    # ===== Logout =====
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))

    return app
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)    