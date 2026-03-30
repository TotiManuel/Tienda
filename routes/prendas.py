from flask import Blueprint, render_template

prendas = Blueprint("prendas", __name__)

@prendas.route("/prendas")
def home():
    return render_template("index.html")
