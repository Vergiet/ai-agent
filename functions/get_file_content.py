import os
from os.path import abspath

MAX_CHARS = 10000
def get_file_content(working_directory, file_path):
    try:

        abs_wd = abspath(working_directory)
        join_path = os.path.join(abs_wd, file_path)
        abs_file = abspath(join_path)

        if not abs_file.startswith(abs_wd):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_file) and not os.path.isfile(abs_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file, "r") as file:
            content = file.read(MAX_CHARS)
        
        
        if len(content) == MAX_CHARS:
            content = content.splitlines()
            content.append(f"...File {file_path} truncated at {MAX_CHARS} characters")
            content = "\n".join(content)
            

        return content

    except Exception as e:
        return f"Error: {e}"
