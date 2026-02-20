from flask import Flask
from app.database import db
from app import models

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///toti.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    app.secret_key = "toti_super_secreto_1234"

    db.init_app(app)
    def formato_ars(valor):
        return f"{int(valor):,}".replace(",", ".")


    app.jinja_env.filters["ars"] = formato_ars


    from app.ventas import ventas_bp
    app.register_blueprint(ventas_bp)
    
    from app.clientes import clientes_bp
    app.register_blueprint(clientes_bp)


    @app.route("/")
    def home():
        from flask import render_template
        return render_template("home.html")

    return app
