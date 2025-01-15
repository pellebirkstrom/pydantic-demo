from enum import Enum
from pydantic import BaseModel


class Category(Enum):
    foobar = "foobar"
    baz = "baz"
    qux = "qux"


class ProcessedFeedback(BaseModel):
    feedback: str
    sentiment: int
    category: Category


def test_feedback_access_data_by_fields():
    f = ProcessedFeedback(feedback="I love this!", sentiment=1, category="foobar")
    assert f.feedback == "I love this!"
    assert f.sentiment == 1
    assert f.category == Category.foobar


def test_feedback_throws_on_loading_data_with_invalid_category():
    invalid = "invalid"
    try:
        ProcessedFeedback(feedback="I love this!", sentiment=1, category=invalid)
        assert False, "Expected ValueError not raised"
    except ValueError as e:
        assert "should be 'foobar', 'baz' or 'qux'" in str(e)


def test_feedback_schema():
    f = ProcessedFeedback(feedback="I love this!", sentiment=1, category="foobar")
    schema = f.model_json_schema()
    expected_schema = {
        "$defs": {
            "Category": {
                "enum": ["foobar", "baz", "qux"],
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
