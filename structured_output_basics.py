from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv(override=True)


# Define your desired output structure
class UserInfo(BaseModel):
    name: str
    age: int


def main():
    client = OpenAI()

    # Extract structured data from natural language
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=UserInfo,
        messages=[{"role": "user", "content": "John Doe is 30 years old."}],
    )

    user_info = completion.choices[0].message.parsed

    print(user_info.name)
    # > John Doe
    print(user_info.age)
    # > 30


if __name__ == "__main__":
    main()
