import os
from os.path import abspath

def write_file(working_directory, file_path, content):
    try:

        abs_wd = abspath(working_directory)
        join_path = os.path.join(abs_wd, file_path)
        abs_file = abspath(join_path)

        if not abs_file.startswith(abs_wd):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # if not os.path.exists(abs_file):
        #     return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file, 'w') as file:
            # Write content to the file
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"


