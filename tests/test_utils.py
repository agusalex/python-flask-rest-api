import unittest
from app.utils import validate_sprocket_data, validate_factory_data


class TestValidateFactoryData(unittest.TestCase):

    def test_valid_data(self):
        valid_data = {
            "factory": {
                "chart_data": {
                    "sprocket_production_actual": [32, 29],
                    "sprocket_production_goal": [32, 30],
                    "time": [1611194818, 1611194878]
                }
            }
        }
        is_valid, message = validate_factory_data(valid_data)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Data is valid")

    def test_invalid_data_missing_fields(self):
        invalid_data = {
            "factory": {}
        }
        is_valid, message = validate_factory_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertEqual(message, "Invalid JSON structure.")

    def test_invalid_data_mismatched_length(self):
        invalid_data = {
            "factory": {
                "chart_data": {
                    "sprocket_production_actual": [32],
                    "sprocket_production_goal": [32, 30],
                    "time": [1611194818, 1611194878]
                }
            }
        }
        is_valid, message = validate_factory_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertEqual(message, "Length of actual, goal, and time data must be the same.")

class TestValidateSprocketData(unittest.TestCase):

    def test_valid_data(self):
        data = {
            'teeth': 20,
            'pitch_diameter': 10.0,
            'outside_diameter': 11.0,
            'pitch': 2.0
        }
        is_valid, message = validate_sprocket_data(data)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid data")

    def test_missing_fields(self):
        required_fields = ['teeth', 'pitch_diameter', 'outside_diameter', 'pitch']
        for field in required_fields:
            data = {
                'teeth': 20,
                'pitch_diameter': 10.0,
                'outside_diameter': 11.0,
                'pitch': 2.0
            }
            del data[field]
            is_valid, message = validate_sprocket_data(data)
            self.assertFalse(is_valid)
            self.assertEqual(message, f"Missing required field: {field}")


if __name__ == "__main__":
    unittest.main()
