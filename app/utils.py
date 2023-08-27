def validate_sprocket_data(data):
    required_fields = ['teeth', 'pitch_diameter', 'outside_diameter', 'pitch']

    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    return True, "Valid data"


def validate_factory_data(data):
    try:
        factory_data = data['factory']
        chart_data = factory_data['chart_data']
        actual_data = chart_data['sprocket_production_actual']
        goal_data = chart_data['sprocket_production_goal']
        time_data = chart_data['time']

        if len(actual_data) != len(goal_data) or len(actual_data) != len(time_data):
            return False, "Length of actual, goal, and time data must be the same."

        return True, "Data is valid"
    except KeyError:
        return False, "Invalid JSON structure."


