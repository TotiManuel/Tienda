import os
import sys
from flask import Flask

# 🔥 IMPORTANTE: agregar raíz al path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from routes.main import main  # importar blueprint
from routes.colecciones import colecciones
from routes.prendas import prendas
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# ✅ Registrar blueprint
app.register_blueprint(main)
app.register_blueprint(colecciones)
app.register_blueprint(prendas)