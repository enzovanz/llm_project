import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, directory))

        if not full_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        str = ""
        contents = os.listdir(full_path)

        for file in contents:
            file_path = os.path.join(full_path, file)
            file_size = os.path.getsize(file_path)
            is_dir = "True"
            if os.path.isfile(file_path):
                is_dir = "False"
            str += f"- {file}: file_size={file_size} bytes, is_dir={is_dir}\n"
    except Exception as e:
        return f"Error: {e}"

    return str

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