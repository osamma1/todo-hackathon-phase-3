import os
import cohere
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
client = cohere.Client(api_key=api_key)

tools = [
    {
        "name": "add_task",
        "description": "Add a new task",
        "parameter_definitions": {
            "title": {"type": "str", "description": "Title of the task", "required": True},
            "description": {"type": "str", "description": "Optional description"}
        }
    },
    {
        "name": "list_tasks",
        "description": "List tasks",
        "parameter_definitions": {
            "status": {"type": "str", "description": "status"}
        }
    }
]

print("Sending request to Cohere with multi tools...")
try:
    response = client.chat(
        model="command-r-08-2024",
        message="Add a task called 'Test Task'",
        tools=tools,
        tool_results=[], # Passing empty tool results
        preamble="You are a helpful assistant. You MUST use the provided tools."
    )
    
    print("\nResponse Received:")
    print(f"Tool Calls: {response.tool_calls}")
    print(f"Text Response: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
