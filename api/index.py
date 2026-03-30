import os
from flask import Flask
from config import Config
from extensions import db
from routes.main import main

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static")
    )

    app.config.from_object(Config)

    # Inicializar DB
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(main)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)