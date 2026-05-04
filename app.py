"""
app.py - Flask application factory for Tales of Time (raw SQL version).

SQLAlchemy is no longer used. Database initialisation is handled by
models.init_db(), which runs the raw DDL schema script.
"""

import os
from flask import Flask
from models.models import init_db


def create_app(config_overrides: dict = None) -> Flask:
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="static",
    )

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "tales-of-time-dev-key")

    if config_overrides:
        app.config.update(config_overrides)

    #Initialise the database schema (safe to re-run - uses IF NOT EXISTS)
    init_db()

    from views.views import bp
    app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
