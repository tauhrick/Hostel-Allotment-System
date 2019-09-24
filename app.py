import time
import sqlite3
import click
import bcrypt
from flask import *
from flask.cli import with_appcontext
from functools import wraps

app = Flask(__name__)

app.secret_key = "secret!"

DATABASE = "db.sqlite"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def edit_db(query, args=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    conn.close()
    return True

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def hash_pwd(pwd):
	return bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())


def check_pwd(pwd, hash_):
	return bcrypt.checkpw(pwd.encode('utf-8'), hash_)


def make_error(status_code, message):
    response = jsonify({
        'status': status_code,
        'error': message,
    })
    # response.status_code = status_code
    return response


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
    	if 'username' in session and session['username'] != None:
    		return f(*args, **kws)
    	else:
            flash("You are not logged in!")
            return redirect("/")
    return decorated_function

def init_db():
	db = get_db()
	with current_app.open_resource("schema.sql") as f:
		db.executescript(f.read().decode("utf8"))
##############################################################################

@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session['username'] = None
    session['accesslevel'] = None
    flash("Logged out!")
    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    init_db()
    app.run(debug = True)