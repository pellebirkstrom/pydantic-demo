from enum import Enum
from typing import Generic, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


class WinterCategory(Enum):
    FOOBAR = "foobar"
    BAZ = "baz"
    QUX = "qux"


class SummerCategory(Enum):
    FOOTBALL = "football"
    SWIMMING = "swimming"
    PARTYING = "partying"


class ProcessedFeedback(BaseModel, Generic[T]):
    feedback: str
    sentiment: int
    category: T


def test_feedback_using_wintercategory():
    f = ProcessedFeedback[WinterCategory](
        feedback="I love this!", sentiment=1, category="foobar"
    )
    assert f.feedback == "I love this!"
    assert f.sentiment == 1
    assert f.category == WinterCategory.FOOBAR


def test_feedback_schema_using_wintercategory():
    f = ProcessedFeedback[WinterCategory](
        feedback="I love this!", sentiment=1, category="foobar"
    )

    schema = f.model_json_schema()

    expected_schema = {
        "$defs": {
            "WinterCategory": {
                "enum": ["foobar", "baz", "qux"],
                "title": "WinterCategory",
                "type": "string",
            }
        },
        "properties": {
            "feedback": {"title": "Feedback", "type": "string"},
            "sentiment": {"title": "Sentiment", "type": "integer"},
            "category": {"$ref": "#/$defs/WinterCategory"},
        },
        "required": ["feedback", "sentiment", "category"],
        "title": "ProcessedFeedback[WinterCategory]",
        "type": "object",
    }
    assert schema == expected_schema


def test_feedback_using_summercategory():
    f = ProcessedFeedback[SummerCategory](
        feedback="I love this!", sentiment=1, category="football"
    )
    assert f.feedback == "I love this!"
    assert f.sentiment == 1
    assert f.category == SummerCategory.FOOTBALL


def test_feedback_schema_using_summercategory():
    f = ProcessedFeedback[SummerCategory](
        feedback="I love this!", sentiment=1, category="football"
    )
    schema = f.model_json_schema()
    expected_schema = {
        "$defs": {
            "SummerCategory": {
                "enum": ["football", "swimming", "partying"],
                "title": "SummerCategory",
                "type": "string",
            }
        },
        "properties": {
            "feedback": {"title": "Feedback", "type": "string"},
            "sentiment": {"title": "Sentiment", "type": "integer"},
            "category": {"$ref": "#/$defs/SummerCategory"},
        },
        "required": ["feedback", "sentiment", "category"],
        "title": "ProcessedFeedback[SummerCategory]",
        "type": "object",
    }
    assert schema == expected_schema


def test_loading_data_with_category_type_from_string():
    type_name = TypeVar("WinterCategory")
    f = ProcessedFeedback[type_name](
        feedback="I love this!", sentiment=1, category="foobar"
    )
    assert f.feedback == "I love this!"
    assert f.sentiment == 1
    assert f.category == "foobar"


if __name__ == "__main__":
    test_feedback_schema_using_wintercategory()
    test_feedback_using_wintercategory()
    test_feedback_using_summercategory()
    test_feedback_schema_using_summercategory()
    test_loading_data_with_category_type_from_string()
