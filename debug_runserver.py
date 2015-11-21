#!venv/bin/python
from flask_failsafe import failsafe


# Failsafe catches various errors and automagically restarts our dev server automatically
@failsafe
def create_flask_app():
    from prairiehub import create_app
    return create_app()

if __name__ == "__main__":
    create_flask_app().run(host='0.0.0.0')
