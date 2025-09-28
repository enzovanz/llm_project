import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([working_directory, full_path]) != working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        
        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        process_object = subprocess.run(["python3", full_path] + args, capture_output=True, timeout=30, cwd=working_directory)
        
        if process_object.stdout == None and process_object.stderr == None:
            return f"No output produced."
        
        return_str = f"STDOUT: {process_object.stdout}, STDERR: {process_object.stderr}"

        if process_object.returncode != 0:
            return_str += f"Process exited with code {process_object.returncode}"
        
        return return_str

    except Exception as e:
        return f"Error: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file with given args",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required =["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="List of arguments passed when running the file",
            ),
        },
    ),
)