from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    name = function_call_part.name
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"
    
    if verbose:
        print(f"Calling function: {name}({args})")
    else:
        print(f" - Calling function: {name}")

    
    function_dict = {
        "get_file_content" : get_file_content,
        "get_files_info" : get_files_info,
        "run_python_file" : run_python_file,
        "write_file" : write_file,
    }

    if name not in function_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )

    result = function_dict[name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": result},
            )
        ],
    )