import os
from app import create_app, db


env = os.environ.get('ENV','development')
app = create_app(env)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run()
