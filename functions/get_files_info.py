import os

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