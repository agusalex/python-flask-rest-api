import unittest
from app.utils import validate_sprocket_data


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
