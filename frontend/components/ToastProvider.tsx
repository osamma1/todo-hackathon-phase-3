'use client';

import React from 'react';
import { Toaster } from 'react-hot-toast';

const ToastProvider = () => {
  return (
    <Toaster
      position="top-right"
      toastOptions={{
        // Define custom styles for different toast types
        style: {
          background: 'rgba(0, 0, 0, 0.8)',
          color: '#fff',
          border: '1px solid rgba(6, 182, 212, 0.5)', // cyan-500 with transparency
          backdropFilter: 'blur(10px)',
          WebkitBackdropFilter: 'blur(10px)',
          borderRadius: '0.5rem',
          boxShadow: '0 0 15px rgba(6, 182, 212, 0.5)', // neon glow effect
        },
        success: {
          style: {
            border: '1px solid rgba(34, 211, 238, 0.5)', // cyan-400 with transparency
            boxShadow: '0 0 15px rgba(34, 211, 238, 0.5)', // cyan neon glow
          },
        },
        error: {
          style: {
            border: '1px solid rgba(239, 68, 68, 0.5)', // red-500 with transparency
            boxShadow: '0 0 15px rgba(239, 68, 68, 0.5)', // red neon glow
          },
        },
      }}
    />
  );
};

export default ToastProvider;