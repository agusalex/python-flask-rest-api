import unittest
import json
from app import create_app, db


class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        # Clear the database before each test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

    def test_get_all_factories(self):
        response = self.client.get('/factories')
        self.assertEqual(response.status_code, 200)

    def test_get_factory_fail(self):
        response = self.client.get('/factories/1')
        # Assuming factory with id 1 doesn't exist
        self.assertEqual(response.status_code, 404)

    def test_get_factory(self):
        valid_data = {
          "factory":  {
                "chart_data": {
                    "sprocket_production_actual": [32, 29],
                    "sprocket_production_goal": [32, 30],
                    "time": [1611194818, 1611194878]
                }
            }
        }
        _ = self.client.post('/factories', json=valid_data)
        response = self.client.get('/factories/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), valid_data)

    def test_create_factory_success(self):
        valid_data = {
            "factory": {
                "chart_data": {
                    "sprocket_production_actual": [32, 29],
                    "sprocket_production_goal": [32, 30],
                    "time": [1611194818, 1611194878]
                }
            }
        }

        response = self.client.post('/factories', json=valid_data)
        assert response.status_code == 201
        assert b'Factory created' in response.data

    def test_create_factory_failure(self):
        invalid_data = {
            "factory": {
                "chart_data": {
                    "sprocket_production_actual": [32],
                    "sprocket_production_goal": [32, 30],
                    "time": [1611194818, 1611194878]
                }
            }
        }

        response = self.client.post('/factories', json=invalid_data)
        assert response.status_code == 400
        assert b'Length of actual, goal, and time data must be the same.' in response.data

    def test_create_factory_invalid_json(self):
        invalid_data = {}

        response = self.client.post('/factories', json=invalid_data)
        assert response.status_code == 400
        assert b'Invalid JSON structure.' in response.data

    def test_get_all_sprockets(self):
        response = self.client.get('/sprockets')
        self.assertEqual(response.status_code, 200)

    def test_create_sprocket(self):
        data = {
            "teeth": 20,
            "pitch_diameter": 10.0,
            "outside_diameter": 11.0,
            "pitch": 2.0
        }
        response = self.client.post('/sprockets', json=data)
        self.assertEqual(response.status_code, 201)

    def test_update_sprocket(self):
        # create a sprocket to update
        initial_data = {
            "teeth": 20,
            "pitch_diameter": 10.0,
            "outside_diameter": 11.0,
            "pitch": 2.0
        }

        response = self.client.post('/sprockets', json=initial_data)
        self.assertEqual(response.status_code, 201)

        # Now, update the sprocket
        update_data = {
            "teeth": 25,
            "pitch_diameter": 12.0,
            "outside_diameter": 13.0,
            "pitch": 2.0
        }

        # Assuming the sprocket was the first one to be inserted and has id=1
        response = self.client.put('/sprockets/1', json=update_data)
        self.assertEqual(response.status_code, 200)

        # Fetch the sprocket and check if the updates were successful
        response = self.client.get('/sprockets/1')
        updated_sprocket_data = response.get_json()
        self.assertEqual(updated_sprocket_data['teeth'], 25)
        self.assertEqual(updated_sprocket_data['pitch_diameter'], 12.0)


if __name__ == "__main__":
    unittest.main()
