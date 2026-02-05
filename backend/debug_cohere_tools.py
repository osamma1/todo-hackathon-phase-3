import os
import cohere
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
client = cohere.Client(api_key=api_key)

tools = [
    {
        "name": "test_tool",
        "description": "A test tool that does nothing but confirm tool usage.",
        "parameter_definitions": {
            "param1": {
                "description": "A test parameter",
                "type": "str",
                "required": True
            }
        }
    }
]

print("Sending request to Cohere with tool...")
try:
    response = client.chat(
        model="command-r-08-2024",
        message="Please use the test_tool with param1='hello'",
        tools=tools,
        preamble="You are a helpful assistant. You MUST use the provided tools."
    )
    
    print("\nResponse Received:")
    print(f"Tool Calls: {response.tool_calls}")
    print(f"Text Response: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
