from openai import OpenAI
from dotenv import load_dotenv
import logging

from enums_with_generics import ProcessedFeedback, WinterCategory

load_dotenv(override=True)


def main():
    # Enable HTTP request logging
    logging.basicConfig(level=logging.DEBUG)

    client = OpenAI()

    # Extract structured data from natural language
    response_model = ProcessedFeedback[WinterCategory]
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=response_model,
        messages=[{"role": "user", "content": "John Doe is 30 years old."}],
    )

    feedback = completion.choices[0].message.parsed

    print(feedback)


# This is the response_format that the OpenAI SDK generates when sending the request
# to OpenAI:
#
# Can be debugged using:
#
# import logging
# logging.basicConfig(level=logging.DEBUG)
#
# {
#   "response_format": {
#     "type": "json_schema",
#     "json_schema": {
#       "schema": {
#         "$defs": {
#           "WinterCategory": {
#             "enum": [
#               "foobar",
#               "baz",
#               "qux"
#             ],
#             "title": "WinterCategory",
#             "type": "string"
#           }
#         },
#         "properties": {
#           "Feedback": {
#             "title": "Feedback",
#             "type": "string"
#           },
#           "Sentiment": {
#             "title": "Sentiment",
#             "type": "integer"
#           },
#           "Category": {
#             "$ref": "#/$defs/WinterCategory"
#           }
#         },
#         "required": [
#           "Feedback",
#           "Sentiment",
#           "Category"
#         ],
#         "title": "FOOBAR",
#         "type": "object",
#         "additionalProperties": "False"
#       },
#       "name": "ProcessedFeedback[WinterCategory]",
#       "strict": "True"
#     }
#   },
#   "stream": "False"
# }


if __name__ == "__main__":
    main()
