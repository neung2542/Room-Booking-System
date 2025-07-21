"""Initialize Flask app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models import db


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    # Initialize Database Plugin
    db.init_app(app)

    with app.app_context():
        import api  # Import routes

        db.create_all()  # Create database tables for our data models

        return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)