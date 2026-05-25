import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    config_mode = os.getenv("CONFIG_MODE", "production").lower()

    database_url = (
        os.getenv(f"{config_mode.upper()}_DATABASE_URL")
        or os.getenv("DATABASE_URL")
        or os.getenv("PRODUCTION_DATABASE_URL")
    )

    if not database_url:
        raise RuntimeError(
            "Database URL not configured."
        )

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "devops-demo-secret"

    db.init_app(app)
    migrate.init_app(app, db)

    from routes import web_bp
    app.register_blueprint(web_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )