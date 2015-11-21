#!venv/bin/python


def create_flask_app():
    from prairiehub import create_app
    return create_app()

if __name__ == "__main__":
    create_flask_app().run(host='0.0.0.0')
