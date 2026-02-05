import sys
import os

# Add the backend directory to sys.path explicitly to simulate uvicorn's environment if run from root
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from agents.chatbot_agent import ChatbotAgent
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
