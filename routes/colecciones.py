from flask import Blueprint, render_template

colecciones = Blueprint("colecciones", __name__)

@colecciones.route("/colecciones")
def home():
    return render_template("colecciones.html")
