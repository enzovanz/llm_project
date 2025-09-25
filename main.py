import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from config import system_prompt

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

messages = types.Content(role="user", parts=[types.Part(text=user_prompt)])

client = genai.Client(api_key=api_key)

reponse = client.models.generate_content(
    model="gemini-2.0-flash-001", 
    contents=messages, 
    config=types.GenerateContentConfig(system_instruction=system_prompt)
)

prompt_tokens = reponse.usage_metadata.prompt_token_count
output_tokens = reponse.usage_metadata.candidates_token_count
estimated_cost = (prompt_tokens / 1e6 * cost_prompt) + \
                 (output_tokens / 1e6 * cost_output)

if verbose_flag:
    print(f"User prompt: {user_prompt}")
    print("Prompt tokens:", prompt_tokens)
    print("Response tokens:", output_tokens)
    print(f"Estimated cost: ${estimated_cost:.6f}")
    print("------------------------------------")
    print(reponse.text)
else:
    print(reponse.text)




