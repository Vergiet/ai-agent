import os
from os.path import abspath

def get_files_info(working_directory, directory=None):

    try:
        abs_wd = abspath(working_directory)
        join_path = os.path.join(abs_wd, directory)
        abs_dir = abspath(join_path)

        if not os.path.exists(abs_dir) and not os.path.isdir(abs_dir):
            return f'Error: "{directory}" is not a directory'

        if not abs_dir.startswith(abs_wd):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'


        return_strings = []
    
        dir_content = os.listdir(abs_dir)
        for entry in dir_content:
            full_path = os.path.join(abs_dir, entry)
            is_dir = os.path.isdir(full_path)
            if is_dir:
                size = sum(get_dir_size(full_path))
            else:
                size = os.path.getsize(full_path)

            return_strings.append(
                f"- {entry}: file_size={size} bytes, is_dir={is_dir}"
            )
    
        return "\n".join(return_strings)

    except Exception as e:
        return f"Error: {e}"


def get_dir_size(directory=None):

    abs_dir = abspath(directory)
    sizes = []
    dir_content = os.listdir(abs_dir)
    for entry in dir_content:
        full_path = os.path.join(abs_dir, entry)
        is_dir = os.path.isdir(full_path)
        if is_dir:
            sizes.extend(get_dir_size(full_path))
        else:
            sizes.append(os.path.getsize(full_path))

    return sizes






# print(get_files_info('/home/ubuntu/workspace/github.com/vergiet/ai-agent', '/home/ubuntu/workspace/github.com/vergiet'))
# print(get_files_info('/home/ubuntu/workspace/github.com/vergiet/ai-agent', 'asd'))
# print(get_files_info('/home/ubuntu/workspace/github.com/vergiet/ai-agent', 'get_files_info.py'))

# print(get_files_info('/home/ubuntu/workspace/github.com/vergiet/ai-agent', '.'))
