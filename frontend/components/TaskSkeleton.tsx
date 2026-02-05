'use client';

import React from 'react';
import { motion } from 'framer-motion';
import GlassCard from './GlassCard';

const TaskSkeleton = () => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="h-full"
    >
      <GlassCard className="h-full flex flex-col">
        <div className="flex items-center mb-4">
          <div className="h-5 w-5 rounded bg-gray-700 animate-pulse"></div>
          <div className="ml-3 h-5 w-3/4 bg-gray-700 rounded animate-pulse"></div>
        </div>
        
        <div className="h-4 bg-gray-700 rounded w-full mb-2 animate-pulse"></div>
        <div className="h-4 bg-gray-700 rounded w-5/6 mb-2 animate-pulse"></div>
        <div className="h-4 bg-gray-700 rounded w-4/6 animate-pulse"></div>
        
        <div className="mt-auto pt-4 flex justify-end space-x-2">
          <div className="h-8 w-8 bg-gray-700 rounded animate-pulse"></div>
          <div className="h-8 w-8 bg-gray-700 rounded animate-pulse"></div>
        </div>
      </GlassCard>
    </motion.div>
  );
};

export default TaskSkeleton;