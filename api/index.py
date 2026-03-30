#region Imports
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash
import sys, os
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
    database_url = os.getenv("DATABASE_URL", "sqlite:///database.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")
    #endregion
    return app
#endregion
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)    
