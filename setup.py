from server import create_app

if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.jinja_env.auto_reload = True
    app.run("0.0.0.0", 8080)