import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.DEBUG)


# Configure db access for the Flask application using Flask-SQLAlchemy
def initialize_db_client(app: Flask) -> SQLAlchemy:
    db = SQLAlchemy(app)
    return db


def initialize_routes(app: Flask) -> None:
    import service.api.persons  # noqa 401
    import service.api.addresses  # noqa 401


def initialize_error_handlers(app: Flask) -> None:

    # Return validation errors as JSON
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_422_error(err):
        messages = err.data.get("messages", ["Invalid request."])
        return jsonify({"errors": messages}), err.code

    # Return 404 errors as JSON
    @app.errorhandler(404)
    def handle_404_error(err):
        return (
            jsonify(
                {"error": getattr(err, "description", "resource does not exit")}
            ),  # noqa 501
            404,
        )


def init_flask_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("service.config.Configuration")

    app.logger.info("Service Startup: Finished configuring application")

    return app


app: Flask = init_flask_app()
db: SQLAlchemy = initialize_db_client(app)

initialize_error_handlers(app)
initialize_routes(app)
