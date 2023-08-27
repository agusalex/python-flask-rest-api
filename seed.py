import os
from app import db, create_app
from app.models import Sprocket, Factory
import json

env = os.environ.get('ENV', 'development')
app = create_app(env)


def populate_sprockets(sprocket_data):
    for sprocket in sprocket_data:
        new_sprocket = Sprocket(
            teeth=sprocket["teeth"],
            pitch_diameter=sprocket["pitch_diameter"],
            outside_diameter=sprocket["outside_diameter"],
            pitch=sprocket["pitch"]
        )
        db.session.add(new_sprocket)


def populate_factories(factory_data):
    for factory in factory_data:
        new_factory = Factory(factory["factory"])
        db.session.add(new_factory)


if __name__ == "__main__":
    with app.app_context():
        with open("seed_data/seed_sprocket_types.json", "r") as f:
            sprocket_data = json.load(f)["sprockets"]
            populate_sprockets(sprocket_data)
        with open("seed_data/seed_factory_data.json", "r") as f:
            factory_data = json.load(f)["factories"]
            populate_factories(factory_data)
        db.session.commit()
        print("Seeding completed...")
