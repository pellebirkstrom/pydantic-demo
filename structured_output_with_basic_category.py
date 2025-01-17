from openai import OpenAI
from dotenv import load_dotenv

from enums import ProcessedFeedback

load_dotenv(override=True)


def main():
    client = OpenAI()

    # Extract structured data from natural language
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=ProcessedFeedback,
        messages=[
            {"role": "user", "content": "Give me some detailed feedback on this."}
        ],
    )

    response = completion.choices[0].message.parsed

    print(response.feedback)
    print(response.sentiment)
    print(response.category)


if __name__ == "__main__":
    main()
