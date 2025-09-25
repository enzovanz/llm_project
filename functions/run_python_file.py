import os
import subprocess

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