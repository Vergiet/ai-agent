from google.genai import types
from google import genai
import os
from dotenv import load_dotenv
import sys

if len(sys.argv) < 2:
    raise Exception("This script requires at most 1 input line")

VERBOSE = False

user_prompt = sys.argv[1]

if "--verbose" in sys.argv:
    VERBOSE = True

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = "gemini-2.0-flash-001"  # free tier
# contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."


messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# try:
generate_content_response = client.models.generate_content(
    model=model, contents=messages)
print(generate_content_response.text)
if VERBOSE:
    print(f"User prompt: {user_prompt}")
    print(
        f"Prompt tokens: {generate_content_response.usage_metadata.prompt_token_count}")
    print(
        f"Response tokens: {generate_content_response.usage_metadata.candidates_token_count}")
# except Exception as e:
#     print(e)
