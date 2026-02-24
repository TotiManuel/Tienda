from flask import Flask, render_template
from models import init_db

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# Crear base de datos
# init_db()


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)