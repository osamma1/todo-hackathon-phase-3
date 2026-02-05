import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import MessageBubble from './MessageBubble';
import { sendChatMessage } from '@/lib/chat';
import toast, { Toaster } from 'react-hot-toast';

interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: string;
}

interface ChatModalProps {
  onClose: () => void;
}

const ChatModal: React.FC<ChatModalProps> = ({ onClose }) => {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | undefined>(undefined);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load conversation from localStorage if available
  useEffect(() => {
    const savedConversation = localStorage.getItem('chat-conversation');
    if (savedConversation) {
      const { id, messages } = JSON.parse(savedConversation);
      setConversationId(id);
      setMessages(messages);
    }
  }, []);

  // Save conversation to localStorage whenever it changes
  useEffect(() => {
    if (conversationId !== undefined) {
      localStorage.setItem(
        'chat-conversation',
        JSON.stringify({ id: conversationId, messages })
      );
    }
  }, [messages, conversationId]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Handle "clear" command locally
    if (inputValue.trim().toLowerCase() === 'clear') {
      setMessages([]);
      setConversationId(undefined);
      setInputValue('');
      localStorage.removeItem('chat-conversation');
      toast.success('Chat history cleared');
      return;
    }

    // Add user message to the chat
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      isUser: true,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send message to backend
      const response = await sendChatMessage(inputValue, conversationId);

      // Update conversation ID if new conversation was created
      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add AI response to the chat
      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        content: response.response,
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Failed to send message. Please try again.');

      // Add error message to the chat
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <AnimatePresence>
      <motion.div
        key="chat-modal-overlay"
        className="fixed inset-0 bg-black/30 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      >
        <motion.div
          className="bg-white/5 backdrop-blur-2xl w-full max-w-lg h-[70vh] rounded-2xl flex flex-col overflow-hidden relative shadow-2xl"
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600/30 to-indigo-700/30 backdrop-blur-md p-4 flex justify-between items-center">
            <h2 className="text-xl gradient-text">AI Todo Assistant</h2>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 focus:outline-none"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto p-4 bg-black/10 backdrop-blur-sm">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-gray-400">
                <div className="mb-4 p-3 bg-gray-700/50 rounded-full">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-12 w-12"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                    />
                  </svg>
                </div>
                <p className="text-center">Start a conversation with your AI assistant</p>
                <p className="text-sm mt-2 text-center max-w-xs">
                  Try commands like "Add task to buy groceries" or "Show my pending tasks"
                </p>
              </div>
            ) : (
              <>
                {messages.map((message) => (
                  <MessageBubble
                    key={message.id}
                    message={message.content}
                    isUser={message.isUser}
                    timestamp={message.timestamp}
                  />
                ))}
                {isLoading && (
                  <MessageBubble
                    key="ai-thinking-bubble"
                    message="Thinking..."
                    isUser={false}
                    timestamp={new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  />
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          {/* Input Area */}
          <div className="p-4 border-t border-white/10 bg-white/5 backdrop-blur-lg">
            <div className="flex items-end space-x-2">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your message..."
                className="flex-1 bg-white/5 text-white rounded-xl px-4 py-3 focus:outline-none focus:ring-1 focus:ring-cyan-500/50 transition-all resize-none min-h-[60px] max-h-32 placeholder:text-gray-500"
                rows={1}
                disabled={isLoading}
              />
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleSend}
                disabled={!inputValue.trim() || isLoading}
                className={`p-3 rounded-xl flex items-center justify-center transition-all ${inputValue.trim() && !isLoading
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 neon-glow-hover text-white'
                  : 'bg-gray-700/50 text-gray-500 cursor-not-allowed'
                  }`}
              >
                {isLoading ? (
                  <svg
                    className="animate-spin h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                ) : (
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-5 w-5 text-white"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                      clipRule="evenodd"
                    />
                  </svg>
                )}
              </motion.button>
            </div>
            <p className="text-xs text-gray-400 mt-2 text-center">
              AI assistant can help manage your tasks with natural language
            </p>
          </div>
        </motion.div>
      </motion.div>
      <Toaster key="chat-toaster" position="bottom-right" />
    </AnimatePresence>
  );
};

export default ChatModal;