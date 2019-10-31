from flask import Flask, render_template, send_from_directory
from server.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "my secret key"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/fe/<path:path>")
def send_fe(path):
    return send_from_directory("../front_end", path)

from server import models, auth, api