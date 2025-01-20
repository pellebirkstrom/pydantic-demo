from dotenv import load_dotenv
import instructor
import openai
import pydantic
from pprint import pprint

load_dotenv(override=True)


# The main retry loop is implemented in the instructor library here:
# https://github.com/instructor-ai/instructor/blob/f86df783bb2ea160f73b8dd37a318d6e448557ea/instructor/retry.py#L151
#
# The formatting of the retry call happens here:
# https://github.com/instructor-ai/instructor/blob/f86df783bb2ea160f73b8dd37a318d6e448557ea/instructor/reask.py#L195-L214


def log_completion_kwargs(**kwargs) -> None:
    print("## Completion kwargs:", "#" * 50)
    pprint(kwargs)
    print()


def log_completion_response(response) -> None:
    print("## Completion response:", "#" * 50)
    pprint(response.model_dump())
    print()


def log_completion_error(error) -> None:
    print("## Completion error:", "#" * 50)
    pprint({"error": error})
    print()


def log_parse_error(error) -> None:
    print("## Parse error:", "#" * 50)
    pprint(error)
    print()


def log_last_attempt(message) -> None:
    print("## Last attempt:", "#" * 50)
    pprint(message)
    print()


# Create an Instructor client
client = instructor.from_openai(openai.OpenAI())

client.on("completion:kwargs", log_completion_kwargs)
client.on("completion:response", log_completion_response)

client.on("completion:error", log_completion_error)
client.on("parse:error", log_parse_error)
client.on("completion:last_attempt", log_last_attempt)


# Define a model with a validator
class User(pydantic.BaseModel):
    name: str
    age: int

    @pydantic.field_validator("age")
    def check_age(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Age cannot be negative")
        return v


try:
    # Use the client to create a completion
    user = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Extract the user name and age from the following text: 'John is -1 years old'",  # This will trigger a validation error that will be retried
            }
        ],
        response_model=User,
        max_retries=3,
    )
except Exception as e:
    print(f"## Error in try/except: {e}")


print("## User:", user)
