from flask import Flask, render_template, request, redirect, url_for, session
from models import init_db, SessionLocal, Usuario, Empresa
from werkzeug.security import generate_password_hash, check_password_hash
import sys, os
from extensions import db

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )
    
    app.secret_key = "supersecretkey"

    # 🔥 Si no existe DATABASE_URL (local), usar SQLite
    database_url = os.getenv("DATABASE_URL", "sqlite:///database.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # ===== Landing Page =====
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

            db = SessionLocal()
            empresa = Empresa(nombre=empresa_nombre)
            db.add(empresa)
            db.commit()

            usuario = Usuario(
                nombre=nombre,
                email=email,
                password=generate_password_hash(password),
                empresa_id=empresa.id
            )
            db.add(usuario)
            db.commit()
            db.close()

            return redirect(url_for("login"))

        return render_template("register.html")

    # ===== Login =====
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            db = SessionLocal()
            usuario = db.query(Usuario).filter_by(email=email).first()
            db.close()

            if usuario and check_password_hash(usuario.password, password):
                session["usuario_id"] = usuario.id
                session["empresa_id"] = usuario.empresa_id
                session["usuario_nombre"] = usuario.nombre
                return redirect(url_for("empresa_home"))
            else:
                return "Usuario o contraseña incorrecta"

        return render_template("login.html")

    # ===== Dashboard de empresa =====
    @app.route("/empresa")
    def empresa_home():
        if "usuario_id" not in session:
            return redirect(url_for("login"))

        nombre_empresa = None
        db = SessionLocal()
        empresa = db.query(Empresa).filter_by(id=session["empresa_id"]).first()
        if empresa:
            nombre_empresa = empresa.nombre
        db.close()

        return render_template("empresa_home.html", empresa_nombre=nombre_empresa, usuario_nombre=session["usuario_nombre"])

    # ===== Logout =====
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    