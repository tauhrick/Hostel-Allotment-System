from flask import Flask, render_template
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

from server import models, auth, api
