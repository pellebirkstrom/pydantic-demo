from enum import Enum
from pydantic import BaseModel


def generate_enums_from_yaml():
    return {
        "APP_FEATURE__PAIRING_SETUP": "App Feature - Pairing & Setup",
        "APP_FEATURE__USER_ONBOARDING": "App Feature - User Onboarding",
        "APP_FEATURE__DEVICE_MANAGEMENT": "App Feature - Device Management",
    }


# Create the enum dynamically in runtime
Category = Enum("Category", generate_enums_from_yaml())


class ProcessedFeedback(BaseModel):
    feedback: str
    sentiment: int
    category: Category


def test_feedback_access_data_by_fields():
    f = ProcessedFeedback(
        feedback="I love this!", sentiment=1, category="App Feature - Pairing & Setup"
    )
    assert f.feedback == "I love this!"
    assert f.sentiment == 1
    assert f.category == Category.APP_FEATURE__PAIRING_SETUP


def test_feedback_throws_on_loading_data_with_invalid_category():
    expected_error = "Input should be 'App Feature - Pairing & Setup', 'App Feature - User Onboarding' or 'App Feature - Device Management'"
    invalid = "invalid"
    try:
        ProcessedFeedback(feedback="I love this!", sentiment=1, category=invalid)
        assert False, "Expected ValueError not raised"
    except ValueError as e:
        assert expected_error in str(e)


def test_feedback_schema():
    f = ProcessedFeedback(
        feedback="I love this!", sentiment=1, category="App Feature - Pairing & Setup"
    )
    schema = f.model_json_schema()
    expected_schema = {
        "$defs": {
            "Category": {
                "enum": [
                    "App Feature - Pairing & Setup",
                    "App Feature - User Onboarding",
                    "App Feature - Device Management",
                ],
                "title": "Category",
                "type": "string",
            }
        },
        "properties": {
            "feedback": {"title": "Feedback", "type": "string"},
            "sentiment": {"title": "Sentiment", "type": "integer"},
            "category": {"$ref": "#/$defs/Category"},
        },
        "required": ["feedback", "sentiment", "category"],
        "title": "ProcessedFeedback",
        "type": "object",
    }
    assert schema == expected_schema


if __name__ == "__main__":
    test_feedback_access_data_by_fields()
    test_feedback_throws_on_loading_data_with_invalid_category()
    test_feedback_schema()
