import { apiClient } from './api';

interface ChatRequest {
  message: string;
  conversation_id?: number;
}

interface ChatResponse {
  response: string;
  conversation_id: number;
  tool_calls?: Array<{
    name: string;
    arguments: Record<string, any>;
    result: any;
  }>;
}

/**
 * Send a message to the chatbot API
 * @param message The user's message
 * @param conversationId Optional ID of an existing conversation
 * @returns The chatbot's response
 */
export async function sendChatMessage(
  message: string,
  conversationId?: number
): Promise<ChatResponse> {
  const requestBody: ChatRequest = {
    message,
    conversation_id: conversationId
  };

  try {
    return await apiClient.request<ChatResponse>('/chat', {
        method: 'POST',
        body: JSON.stringify(requestBody)
    });
  } catch (error: any) {
    console.error('Error sending chat message:', error);
    
    // Throw a more descriptive error
    if (error.response) {
      // Server responded with error status
      throw new Error(`Server error: ${error.response.status} - ${error.response.data?.detail || 'Unknown error'}`);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error: Unable to reach the server');
    } else {
      // Something else happened
      throw new Error(`Request error: ${error.message}`);
    }
  }
}