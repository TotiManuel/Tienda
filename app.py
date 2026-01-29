from flask import Flask, redirect, url_for
from config import Config
from models import db
from blueprints.web import web_bp
from blueprints.admin import admin_bp
from blueprints.vendedor import vendedor_bp
from blueprints.auth import auth_bp   # 👈 NUEVO
from blueprints.cliente import cliente_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar base de datos
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(web_bp, url_prefix="/home")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(vendedor_bp, url_prefix="/vendedor")
    app.register_blueprint(cliente_bp)
    app.register_blueprint(auth_bp)  # 👈 /login y /logout

    # Ruta raíz
    @app.route("/")
    def index():
        return redirect(url_for("web.home"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
