import os
import cohere
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
client = cohere.Client(api_key=api_key)

def test_tool_trigger(model, tools, message, tool_results=None):
    print(f"\n--- Testing Model: {model} ---")
    print(f"Message: {message}")
    print(f"Tool Results argument: {tool_results}")
    
    try:
        response = client.chat(
            model=model,
            message=message,
            tools=tools,
            tool_results=tool_results,
            preamble="You are a helpful task assistant. Use tools to manage the user's tasks."
        )
        print(f"Response Tool Calls: {response.tool_calls}")
        print(f"Response Text: {response.text}")
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

# Test 1: Using 'str' type (current)
tools_str = [
    {
        "name": "add_task",
        "description": "Add a new task",
        "parameter_definitions": {
            "title": {"type": "str", "description": "Title of the task", "required": True},
            "description": {"type": "str", "description": "Optional description"}
        }
    }
]

# Test 2: Using 'string' type (common in JSON schema)
tools_string = [
    {
        "name": "add_task",
        "description": "Add a new task",
        "parameter_definitions": {
            "title": {"type": "string", "description": "Title of the task", "required": True},
            "description": {"type": "string", "description": "Optional description"}
        }
    }
]

message = "Add a task to buy milk"

print("TEST 1: 'str' type, NO tool_results")
print(test_tool_trigger("command-r-08-2024", tools_str, message))

print("\nTEST 2: 'str' type, WITH tool_results=[]")
print(test_tool_trigger("command-r-08-2024", tools_str, message, tool_results=[]))

print("\nTEST 3: 'string' type, NO tool_results")
print(test_tool_trigger("command-r-08-2024", tools_string, message))

print("\nTEST 4: 'string' type, NO tool_results, newer model")
print(test_tool_trigger("command-r7b-12-2024", tools_string, message))
