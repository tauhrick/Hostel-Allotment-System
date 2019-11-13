from server import app, db

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = True
    db.create_all()
    app.run("127.0.0.1", 8000, debug = True)
