'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  hoverEffect?: boolean;
  onClick?: () => void;
}

const GlassCard: React.FC<GlassCardProps> = ({ 
  children, 
  className = '', 
  hoverEffect = false,
  onClick 
}) => {
  const cardClasses = `glass-card rounded-xl p-6 ${className}`;
  
  if (hoverEffect) {
    return (
      <motion.div
        whileHover={{ y: -10, scale: 1.03 }}
        whileTap={{ scale: 0.98 }}
        className={cardClasses}
        onClick={onClick}
        style={{ cursor: onClick ? 'pointer' : 'default' }}
      >
        {children}
      </motion.div>
    );
  }

  return (
    <div className={cardClasses} onClick={onClick}>
      {children}
    </div>
  );
};

export default GlassCard;