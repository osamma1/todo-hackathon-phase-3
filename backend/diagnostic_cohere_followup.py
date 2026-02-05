import os
import cohere
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
client = cohere.Client(api_key=api_key)

model = "command-r7b-12-2024"
message = "Add a task to buy milk"
tools = [
    {
        "name": "add_task",
        "description": "Add a new task",
        "parameter_definitions": {
            "title": {"type": "str", "description": "Title of the task", "required": True}
        }
    }
]

print(f"Step 1: Initial call to {model}")
response = client.chat(
    model=model,
    message=message,
    tools=tools,
    preamble="You are a helpful task assistant."
)

print(f"Tool Calls received: {response.tool_calls}")

if response.tool_calls:
    print("\nStep 2: Follow-up call with tool_results and force_single_step=True")
    try:
        tool_results = [{
            "call": {"name": tc.name, "parameters": tc.parameters},
            "outputs": [{"id": "123", "title": tc.parameters.get("title"), "status": "success"}]
        } for tc in response.tool_calls]
        
        final_response = client.chat(
            model=model,
            message=message,
            tools=tools,
            tool_results=tool_results,
            force_single_step=True,
            preamble="You are a helpful task assistant."
        )
        print("Success! Final Response received.")
        print(f"Text: {final_response.text}")
    except Exception as e:
        print(f"Follow-up failed: {e}")
else:
    print("No tool calls triggered in Step 1. Adjusting message...")
