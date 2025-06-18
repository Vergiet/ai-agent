# main.py

from google.genai import types
from google import genai
import os
from dotenv import load_dotenv
import sys
from functions.call_function import call_function

if len(sys.argv) < 2:
    raise Exception("This script requires at most 1 input line")

VERBOSE = False

user_prompt = sys.argv[1]

if "--verbose" in sys.argv:
    VERBOSE = True


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model_name = "gemini-2.0-flash-001"  # free tier

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]


#
#
# schema_write_file


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to the specified file to update scripts. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write the specified content to, relative to the working directory. This parameter is required.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the specified file, relative to the working directory. This parameter is required.",
            ),
        },
    ),
)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python script, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python script to run. This parameter is required.",
            ),
        },
    ),
)


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get content from specified files listed by schema_get_files_info, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get the content from, relative to the working directory. This parameter is required.",
            ),
        },
    ),
)


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_file_content,
    ]
)


config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)


# if not function_call_result.parts[0].function_response.response:
#     raise Exception("invalid result")
# elif VERBOSE:
#     print(f"-> {function_call_result.parts[0].function_response.response}")


for i in range(200):

    response = client.models.generate_content(
        model=model_name, contents=messages, config=config
    )

    function_call_result = None
    function_call_part = None

    for each_candidate in response.candidates:
        messages.append(each_candidate.content)

    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, VERBOSE)
            messages.append(function_call_result)

        # function_call_part = [0]

    # if function_call_part:
    #     function_call_result = call_function(function_call_part, VERBOSE)

    # if function_call_result:
    #     messages.append(function_call_result)

    if not function_call_result:
        print(response.text)
        reaction = input()
        if reaction == "exit":
            break
        if reaction:
            messages.append(types.Content(role="user", parts=[types.Part(text=reaction)]))
