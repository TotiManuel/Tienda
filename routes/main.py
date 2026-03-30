from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/dashboard")
def dashboard():
    return render_template("index.html")

@main.route("/colecciones")
def colecciones():
    return render_template("index.html")

@main.route("/prendas")
def prendas():
    return render_template("index.html")