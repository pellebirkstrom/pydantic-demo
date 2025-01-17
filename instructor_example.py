import instructor
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)


# Define your desired output structure
class UserInfo(BaseModel):
    name: str
    age: int


def main():
    # Patch the OpenAI client
    client = instructor.from_openai(OpenAI())

    # Extract structured data from natural language
    user_info = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=UserInfo,
        messages=[{"role": "user", "content": "John Doe is 30 years old."}],
    )

    print(user_info.name)
    # > John Doe
    print(user_info.age)
    # > 30


if __name__ == "__main__":
    main()
