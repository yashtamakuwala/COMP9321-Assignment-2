from flask import Flask
from tahelka.blueprints import session
from tahelka.exceptions import BadRequestError, UnauthorizedError
from tahelka import error_handler

def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # Register blueprints
    app.register_blueprint(session.blueprint)

    # Register error handlers
    app.register_error_handler(BadRequestError,
                               error_handler.handle_bad_request)
    app.register_error_handler(UnauthorizedError,
                               error_handler.handle_unauthorized)


    return app
