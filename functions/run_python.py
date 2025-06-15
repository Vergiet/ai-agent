import os
from os.path import abspath
import subprocess


def run_python_file(working_directory, file_path):
    try:
        abs_wd = abspath(working_directory)
        join_path = os.path.join(abs_wd, file_path)
        abs_file = abspath(join_path)

        if not abs_file.startswith(abs_wd):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_file) and not os.path.isfile(abs_file):
            return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        proc = subprocess.run(["/home/ubuntu/workspace/github.com/vergiet/ai-agent/venv/bin/python", abs_file], timeout=30, capture_output=True, cwd=abs_wd)
        proc.check_returncode()

        results = []
        if len(proc.stdout) == 0 and len(proc.stderr)==0:
            results.append("No output produced.")
            return results
        for line in proc.stdout.splitlines():
            results.append(f"STDOUT: {line.decode()}")

        for line in proc.stderr.splitlines():
            results.append(f"STDERR: {line.decode()}")
        if proc.returncode != 0:
            results.append(f"Process exited with code {proc.returncode}")

        return results


    except Exception as e:
        return f"Error: executing Python file: {e}"