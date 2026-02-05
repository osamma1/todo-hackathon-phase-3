import cohere
try:
    from cohere import CohereAPIError
except ImportError:
    from cohere.core.api_error import ApiError as CohereAPIError
from typing import Dict, Any, List
from core.cohere_client import cohere_client
from utils.conversation_helpers import get_conversation_history, create_new_conversation, save_message_to_conversation
from tools.mcp_tools import add_task, list_tasks, update_task, complete_task, delete_task, get_user_info


class ChatbotAgent:
    def __init__(self):
        self.tools = {
            "add_task": {
                "description": "Add a new task",
                "parameter_definitions": {
                    "title": {"type": "str", "description": "Title of the task", "required": True},
                    "description": {"type": "str", "description": "Optional description of the task"}
                }
            },
            "list_tasks": {
                "description": "List tasks with optional status filter",
                "parameter_definitions": {
                    "status": {"type": "str", "description": "Optional status filter (all, pending, completed)"}
                }
            },
            "update_task": {
                "description": "Update an existing task",
                "parameter_definitions": {
                    "task_id": {"type": "str", "description": "The numeric ID of the task to update (NOT your user ID)", "required": True},
                    "title": {"type": "str", "description": "Optional new title"},
                    "description": {"type": "str", "description": "Optional new description"}
                }
            },
            "complete_task": {
                "description": "Mark a task as completed",
                "parameter_definitions": {
                    "task_id": {"type": "str", "description": "The numeric ID of the task to complete (NOT your user ID)", "required": True}
                }
            },
            "delete_task": {
                "description": "Delete a task",
                "parameter_definitions": {
                    "task_id": {"type": "str", "description": "The numeric ID of the task to delete (NOT your user ID)", "required": True}
                }
            },
            "get_user_info": {
                "description": "Get current user information",
                "parameter_definitions": {}
            },
            "search_tasks": {
                "description": "Search for tasks by title",
                "parameter_definitions": {
                    "query": {"type": "str", "description": "The search query to match against task titles", "required": True}
                }
            }
        }

    def process_message(self, user_id: str, message: str, conversation_id: int = None):
        """
        Process a user message and return the AI response.
        
        Args:
            user_id: ID of the user sending the message
            message: The user's message
            conversation_id: Optional ID of an existing conversation
            
        Returns:
            Dictionary with response, conversation_id, and any tool calls
        """
        # Get or create conversation
        if conversation_id is None:
            from core.database import get_session
            with next(get_session()) as db:
                conversation = create_new_conversation(db, user_id)
                conversation_id = conversation.id
        else:
            # Verify conversation belongs to user
            from core.database import get_session
            with next(get_session()) as db:
                conversation_history = get_conversation_history(db, conversation_id, user_id)
                if conversation_history is None:
                    return {
                        "response": "Error: Conversation not found or access denied.",
                        "conversation_id": conversation_id,
                        "tool_calls": []
                    }

        # Save user message to conversation
        from core.database import get_session
        with next(get_session()) as db:
            save_message_to_conversation(db, conversation_id, user_id, "user", message)

        # Get conversation history for context
        with next(get_session()) as db:
            history = get_conversation_history(db, conversation_id, user_id)
            chat_history = []
            for msg in history:
                chat_history.append({
                    "role": "USER" if msg.role == "user" else "CHATBOT",
                    "message": msg.content
                })

        try:
            # Prepare the tools for Cohere
            tools = []
            for tool_name, tool_info in self.tools.items():
                tool_def = {
                    "name": tool_name,
                    "description": tool_info["description"],
                    "parameter_definitions": tool_info["parameter_definitions"]
                }
                tools.append(tool_def)

            # Call Cohere with tools - Let Cohere handle multi-step natively
            system_preamble = "You are an intelligent task assistant. You have access to tools to manage the user's todo list. You MUST use these tools whenever a user asks to add, list, search, update, or delete tasks. IMPORTANT: If a user refers to a task by name, you MUST FIRST use `search_tasks` or `list_tasks` to find the correct numeric 'id'. You CANNOT guess the ID. You CANNOT use the title as the ID. Once you have the ID from the search/list result, use that ID in `update_task`, `complete_task`, or `delete_task`. If you don't find a task with search, tell the user you couldn't find it. Be concise and professional."
            
            all_tool_calls = []
            ai_response = ""
            
            # Initial call - Cohere will handle multi-step internally
            response = cohere_client.chat(
                model="command-r-08-2024",
                message=message,
                chat_history=chat_history[:-1],  # Exclude current message
                tools=tools,
                preamble=system_preamble
                # Note: No force_single_step, allowing multi-step reasoning
            )

            # If tool calls were made, execute them and get final response
            if response.tool_calls:
                tool_results_for_cohere = []
                
                for tool_call in response.tool_calls:
                    tool_name = tool_call.name
                    tool_parameters = tool_call.parameters

                    # Execute the tool
                    tool_result = self.execute_tool(tool_name, tool_parameters, user_id)
                    
                    tool_results_for_cohere.append({
                        "call": tool_call,
                        "outputs": [tool_result]
                    })
                    
                    all_tool_calls.append({
                        "name": tool_name,
                        "arguments": tool_parameters,
                        "result": tool_result
                    })

                # Get final response with tool results
                final_response = cohere_client.chat(
                    model="command-r-08-2024",
                    message=message,
                    chat_history=chat_history[:-1],
                    tools=tools,
                    tool_results=tool_results_for_cohere,
                    preamble=system_preamble
                )
                
                # Check if there are more tool calls (multi-turn scenario)
                if final_response.tool_calls:
                    # Execute second round of tool calls
                    for tool_call in final_response.tool_calls:
                        tool_name = tool_call.name
                        tool_parameters = tool_call.parameters
                        tool_result = self.execute_tool(tool_name, tool_parameters, user_id)
                        
                        tool_results_for_cohere.append({
                            "call": tool_call,
                            "outputs": [tool_result]
                        })
                        
                        all_tool_calls.append({
                            "name": tool_name,
                            "arguments": tool_parameters,
                            "result": tool_result
                        })
                    
                    # Get truly final response
                    final_response = cohere_client.chat(
                        model="command-r-08-2024",
                        message="",  # Empty message for continuation
                        chat_history=chat_history[:-1],
                        tools=tools,
                        tool_results=tool_results_for_cohere,
                        force_single_step=True,  # Force final answer
                        preamble=system_preamble
                    )
                
                ai_response = final_response.text
            else:
                # No tool calls, direct response
                ai_response = response.text

            # Save assistant response to conversation
            with next(get_session()) as db:
                save_message_to_conversation(db, conversation_id, user_id, "assistant", ai_response or "")

            return {
                "response": ai_response,
                "conversation_id": conversation_id,
                "tool_calls": all_tool_calls
            }

        except CohereAPIError as e:
            # Handle specific Cohere API errors
            print(f"DEBUG: Cohere API Error: {e}")
            import traceback
            traceback.print_exc()
            error_response = f"Sorry, I encountered an API error: {str(e)}"
            try:
                from core.database import get_session
                with next(get_session()) as db:
                    save_message_to_conversation(db, conversation_id, user_id, "assistant", error_response)
            except:
                pass
            return {
                "response": error_response,
                "conversation_id": conversation_id,
                "tool_calls": []
            }
        except Exception as e:
            # Handle other errors
            error_response = f"Sorry, I encountered an unexpected error: {str(e)}"
            print(f"CRITICAL ERROR in process_message: {str(e)}")
            import traceback
            traceback.print_exc()
            try:
                from core.database import get_session
                with next(get_session()) as db:
                    save_message_to_conversation(db, conversation_id, user_id, "assistant", error_response)
            except:
                pass
            return {
                "response": error_response,
                "conversation_id": conversation_id,
                "tool_calls": []
            }


    def execute_tool(self, tool_name: str, parameters: Dict[str, Any], user_id: str) -> Any:
        # Add user_id to parameters for all tools
        parameters["user_id"] = user_id
        
        """
        Execute a tool with the given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool
            user_id: ID of the user executing the tool
            
        Returns:
            Result of the tool execution
        """
        if tool_name == "add_task":
            return add_task(**parameters)
        elif tool_name == "list_tasks":
            return list_tasks(**parameters)
        elif tool_name == "update_task":
            return update_task(**parameters)
        elif tool_name == "complete_task":
            return complete_task(**parameters)
        elif tool_name == "delete_task":
            return delete_task(**parameters)
        elif tool_name == "get_user_info":
            return get_user_info(**parameters)
        elif tool_name == "search_tasks":
            from tools.mcp_tools import search_tasks
            return search_tasks(**parameters)
        else:
            return {"error": f"Unknown tool: {tool_name}"}