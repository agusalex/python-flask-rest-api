from flask import Blueprint
from flask import request, jsonify

from app.models import Sprocket, Factory
from app.utils import validate_sprocket_data, validate_factory_data


def init_routes(app, db):
    v1_blueprint = Blueprint('v1', __name__, url_prefix='/v1')

    @v1_blueprint.route('/factories', methods=['GET'])
    def get_all_factories():
        factories = Factory.query.all()
        return jsonify({'factories': [factory.serialize() for factory in factories]})

    @v1_blueprint.route('/factories/<int:factory_id>', methods=['GET'])
    def get_factory(factory_id):
        factory = db.session.get(Factory, factory_id)
        if factory:
            return jsonify(factory.serialize())
        return jsonify({"message": "Factory not found"}), 404

    @v1_blueprint.route('/factories', methods=['POST'])
    def create_factory():
        data = request.get_json()

        is_valid, message = validate_factory_data(data)
        if not is_valid:
            return jsonify({"message": message}), 400

        new_factory = Factory(data['factory'])
        db.session.add(new_factory)
        db.session.commit()

        return jsonify({"message": "Factory created"}), 201

    @v1_blueprint.route('/sprockets', methods=['GET'])
    def get_all_sprockets():
        sprockets = Sprocket.query.all()
        return jsonify({"sprockets": [
            {
                "id": sprocket.id,
                "teeth": sprocket.teeth,
                "pitch_diameter": sprocket.pitch_diameter,
                "outside_diameter": sprocket.outside_diameter,
                "pitch": sprocket.pitch
            } for sprocket in sprockets
        ]})

    @v1_blueprint.route('/sprockets/<int:sprocket_id>', methods=['GET'])
    def get_sprocket(sprocket_id):
        sprocket = db.session.get(Sprocket, sprocket_id)
        if sprocket:
            return jsonify({
                "id": sprocket.id,
                "teeth": sprocket.teeth,
                "pitch_diameter": sprocket.pitch_diameter,
                "outside_diameter": sprocket.outside_diameter,
                "pitch": sprocket.pitch
            })
        return jsonify({"message": "Sprocket not found"}), 404

    @v1_blueprint.route('/sprockets', methods=['POST'])
    def create_sprocket():
        data = request.get_json()
        is_valid, message = validate_sprocket_data(data)
        if not is_valid:
            return jsonify({"message": message}), 400

        new_sprocket = Sprocket(**data)
        db.session.add(new_sprocket)
        db.session.commit()

        return jsonify({"message": "Sprocket created"}), 201

    @v1_blueprint.route('/sprockets/<int:sprocket_id>', methods=['PUT'])
    def update_sprocket(sprocket_id):
        sprocket = db.session.get(Sprocket, sprocket_id)
        if not sprocket:
            return jsonify({"message": "Sprocket not found"}), 404

        data = request.get_json()
        is_valid, message = validate_sprocket_data(data)
        if not is_valid:
            return jsonify({"message": message}), 400

        for key, value in data.items():
            setattr(sprocket, key, value)

        db.session.commit()

        return jsonify({"message": "Sprocket updated"}), 200

    app.register_blueprint(v1_blueprint)
