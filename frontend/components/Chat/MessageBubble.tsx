import React from 'react';
import { motion } from 'framer-motion';

interface MessageBubbleProps {
  message: string;
  isUser: boolean;
  timestamp?: string;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, isUser, timestamp }) => {
  return (
    <motion.div
      className={`flex mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div
        className={`max-w-[75%] px-4 py-3 rounded-2xl shadow-xl transition-all ${isUser
            ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-br-none neon-glow'
            : 'bg-white/5 backdrop-blur-xl text-gray-100 rounded-bl-none'
          }`}
      >
        <p className="text-sm leading-relaxed">{message}</p>
        {timestamp && (
          <p className={`text-[10px] mt-1 uppercase tracking-wider ${isUser ? 'text-cyan-100/70' : 'text-gray-400'}`}>
            {timestamp}
          </p>
        )}
      </div>
    </motion.div>
  );
};

export default MessageBubble;