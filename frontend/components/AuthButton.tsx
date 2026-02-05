'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface AuthButtonProps {
  children: React.ReactNode;
  type?: 'button' | 'submit' | 'reset';
  onClick?: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
  className?: string;
}

const AuthButton: React.FC<AuthButtonProps> = ({
  children,
  type = 'button',
  onClick,
  disabled = false,
  variant = 'primary',
  className = ''
}) => {
  const baseClasses = "flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all duration-300 transform hover:scale-105 disabled:opacity-50";

  const variantClasses = variant === 'primary'
    ? "text-white bg-cyan-600 hover:bg-cyan-500 focus:ring-cyan-500 shadow-[0_0_15px_rgba(6,182,212,0.3)]"
    : "text-cyan-400 bg-transparent border border-cyan-400 hover:bg-cyan-400 hover:text-white focus:ring-cyan-500";

  return (
    <motion.button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variantClasses} ${className}`}
      whileHover={{ scale: disabled ? 1 : 1.05 }}
      whileTap={{ scale: disabled ? 1 : 0.95 }}
    >
      {children}
    </motion.button>
  );
};

export default AuthButton;