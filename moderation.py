from enum import Enum
from typing import Optional
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

# This example is from:
# https://platform.openai.com/docs/guides/structured-outputs?context=ex4
#
# Interesting: How a loosely defined prompt works together with structured output response format


class Category(str, Enum):
    violence = "violence"
    sexual = "sexual"
    self_harm = "self_harm"


class ContentCompliance(BaseModel):
    is_violating: bool
    category: Optional[Category]
    explanation_if_violating: Optional[str]


def main():
    client = OpenAI()

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": "Determine if the user input violates specific guidelines and explain if they do.",
            },
            {"role": "user", "content": "How do I prepare for a job interview?"},
        ],
        response_format=ContentCompliance,
    )

    compliance = completion.choices[0].message.parsed
    print(compliance)


if __name__ == "__main__":
    main()
