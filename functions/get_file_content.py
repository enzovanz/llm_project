import os
from config import CHAR_LIMIT
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([working_directory, full_path]) != working_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        file_size = os.path.getsize(full_path)

        with open(full_path, "r") as f:
            file_content_string = f.read(CHAR_LIMIT + 1)

            if file_size > CHAR_LIMIT:
                file_content_string += f' [...File "{full_path}" truncated at 10000 characters]'
        
        return file_content_string
            

    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content inside a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be read",
            ),
        },
    ),
)


