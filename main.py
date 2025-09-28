import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from config import system_prompt
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
cost_prompt = 0.35   # USD per 1M input tokens
cost_output = 0.70   # USD per 1M output tokens
verbose_flag = False
try:
    user_prompt = sys.argv[1]
except:
    raise Exception("Input a prompt")

try:
    if sys.argv[2] == "--verbose":
        verbose_flag = True
except:
    pass

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

messages = types.Content(role="user", parts=[types.Part(text=user_prompt)])

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash-001", 
    contents=messages, 
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
)

prompt_tokens = response.usage_metadata.prompt_token_count
output_tokens = response.usage_metadata.candidates_token_count
estimated_cost = (prompt_tokens / 1e6 * cost_prompt) + \
                 (output_tokens / 1e6 * cost_output)


if verbose_flag:
    print(f"User prompt: {user_prompt}")
    print("Prompt tokens:", prompt_tokens)
    print("Response tokens:", output_tokens)
    print(f"Estimated cost: ${estimated_cost:.6f}")
    print("------------------------------------")
    if response.function_calls:
        try:
            function_call_part = response.function_calls[0]
            function_call_result = call_function(function_call_part, verbose_flag)
            print(f"-> {function_call_result.parts[0].function_response.response}")
        except:
            raise Exception("Fatal error")
    else:
        print(response.text)
else:
    if response.function_calls:
        function_call_part = response.function_calls[0]
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)




