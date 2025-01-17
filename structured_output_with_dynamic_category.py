from openai import OpenAI
from dotenv import load_dotenv

from enums_dynamic import ProcessedFeedback

load_dotenv(override=True)


def main():
    client = OpenAI()

    # Extract structured data from natural language
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=ProcessedFeedback,
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
#
# {
#   "response_format": {
#     "type": "json_schema",
#     "json_schema": {
#       "schema": {
#         "$defs": {
#           "Category": {
#             "enum": [
#               "App Feature - Pairing & Setup",
#               "App Feature - User Onboarding",
#               "App Feature - Device Management"
#             ],
#             "title": "Category",
#             "type": "string"
#           }
#         },
#         "properties": {
#           "feedback": {
#             "title": "Feedback",
#             "type": "string"
#           },
#           "sentiment": {
#             "title": "Sentiment",
#             "type": "integer"
#           },
#           "category": {
#             "$ref": "#/$defs/Category"
#           }
#         },
#         "required": [
#           "feedback",
#           "sentiment",
#           "category"
#         ],
#         "title": "ProcessedFeedback",
#         "type": "object",
#         "additionalProperties": false
#       },
#       "name": "ProcessedFeedback",
#       "strict": true
#     }
#   }
# }

if __name__ == "__main__":
    main()
