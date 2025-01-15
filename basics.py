from textwrap import dedent
from pydantic import BaseModel, field_validator


class ProcessedFeedback(BaseModel):
    feedback: str
    sentiment: int
    category: str

    @field_validator("sentiment")
    def validate_sentiment(cls, v):
        if v not in (-1, 0, 1):
            raise ValueError("Illegal sentiment value")
        return v


def test_feedback_access_data_by_fields():
    f = ProcessedFeedback(feedback="I love this!", sentiment=1, category="foobar")
    assert f.feedback == "I love this!"
    assert f.sentiment == 1
    assert f.category == "foobar"


def test_load_from_json():
    json_data = dedent(
        """
        {
            "feedback": "I love this!",
            "sentiment": 1,
            "category": "foobar"
        }
        """
    )

    f = ProcessedFeedback.model_validate_json(json_data)

    assert f.feedback == "I love this!"
    assert f.sentiment == 1
    assert f.category == "foobar"


def test_feedback_throws_on_failed_vaildation():
    try:
        ProcessedFeedback(feedback="I love this!", sentiment=2000, category="foobar")
        assert False, "Expected ValueError not raised"
    except ValueError as e:
        assert "Illegal sentiment value" in str(e)


def test_feedback_as_dict():
    f = ProcessedFeedback(feedback="I love this!", sentiment=1, category="foobar")

    dict_repr = f.model_dump()

    assert dict_repr["feedback"] == "I love this!"
    assert dict_repr["sentiment"] == 1
    assert dict_repr["category"] == "foobar"


def test_feedback_as_json():
    f = ProcessedFeedback(feedback="I love this!", sentiment=1, category="foobar")

    json_repr = f.model_dump_json()

    expected_repr = '{"feedback":"I love this!","sentiment":1,"category":"foobar"}'
    assert json_repr == expected_repr


def test_feedback_schema():
    f = ProcessedFeedback(feedback="I love this!", sentiment=1, category="foobar")
    schema = f.model_json_schema()
    expected_schema = {
        "properties": {
            "feedback": {"title": "Feedback", "type": "string"},
            "sentiment": {"title": "Sentiment", "type": "integer"},
            "category": {"title": "Category", "type": "string"},
        },
        "required": ["feedback", "sentiment", "category"],
        "title": "ProcessedFeedback",
        "type": "object",
    }
    assert schema == expected_schema


if __name__ == "__main__":
    test_feedback_access_data_by_fields()
    test_load_from_json()
    test_feedback_throws_on_failed_vaildation()
    test_feedback_as_dict()
    test_feedback_as_json()
    test_feedback_schema()
