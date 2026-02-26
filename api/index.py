#region Imports
from flask import Flask, render_template
from models import init_db
import sys, os
from Prueba.extensions import db
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
    #endregion
    return app
#endregion
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)    