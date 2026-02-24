from flask import Flask, render_template
import sys
import os

# 🔹 Agregar raíz del proyecto al PATH (clave en Vercel)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

# 🔹 Importar modelos
from models import init_db


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    # 🔹 Rutas
    @app.route("/")
    def home():
        return render_template("index.html")

    return app


# 🔹 Crear app para Vercel
app = create_app()


# 🔹 Solo local (no en Vercel)
if __name__ == "__main__":
    init_db()  # solo en desarrollo
    app.run(debug=True)