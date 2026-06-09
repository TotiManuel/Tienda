from flask import Flask
import os

from database.database import crear_tablas

# ======================================
# BLUEPRINTS
# ======================================

from routes.public import public_bp
from routes.carrito import carrito_bp
from routes.auth import auth_bp
from routes.admin import admin_bp

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "clave_super_secreta"
)

# ======================================
# CREAR TABLAS
# ======================================

crear_tablas()

# ======================================
# REGISTRAR BLUEPRINTS
# ======================================

app.register_blueprint(public_bp)

app.register_blueprint(carrito_bp)

app.register_blueprint(auth_bp)

app.register_blueprint(admin_bp)

# ======================================

if __name__ == "__main__":

    app.run(debug=True)