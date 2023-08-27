from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import DevelopmentConfig, ProductionConfig, TestingConfig

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name="production"):
    app = Flask(__name__)

    if config_name == "production":
        print("Running on prod")
        app.config.from_object(ProductionConfig)
    elif config_name == "development2":
        print("Running on dev")
        app.config.from_object(DevelopmentConfig)
    elif config_name == "testing2":
        print("Running on test")
        app.config.from_object(TestingConfig)
    else:
        raise ValueError(f"Unknown config: {config_name}")

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # important for sqlalchemy to have context of models
        from . import models
        db.create_all()

    from .routes import init_routes
    init_routes(app, db)

    return app
