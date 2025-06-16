from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    kwargs = function_call_part.args

    function_name = function_call_part.name

    match function_name:
        case "get_file_content":
            function_result = get_file_content("./calculator", **kwargs)
        case "get_files_info":
            function_result = get_files_info("./calculator", **kwargs)
        case "run_python_file":
            function_result = run_python_file("./calculator", **kwargs)
        case "write_file":
            function_result = write_file("./calculator", **kwargs)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )

    if function_result:

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
