import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ChatModal from './ChatModal';

const ChatIcon = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleModal = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {/* Floating Chat Icon */}
      <motion.div
        className="fixed bottom-28 right-8 z-50 cursor-pointer"
        onClick={toggleModal}
        whileHover={{ scale: 1.1, rotate: 5 }}
        whileTap={{ scale: 0.9 }}
      >
        <div className="relative group">
          {/* Greeting Tooltip Removed */}

          <div className="bg-cyan-600 hover:bg-cyan-500 transition-all duration-300 rounded-full w-16 h-16 flex items-center justify-center relative overflow-hidden">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-8 w-8 text-white relative z-10"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
              />
            </svg>
            <div className="absolute inset-0 bg-gradient-to-tr from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
          </div>
        </div>
      </motion.div>

      {/* Chat Modal */}
      {isOpen && <ChatModal onClose={toggleModal} />}
    </>
  );
};

export default ChatIcon;