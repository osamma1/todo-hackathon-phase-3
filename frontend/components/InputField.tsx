'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface InputFieldProps {
  label: string;
  id: string;
  type?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
  error?: string;
  required?: boolean;
  placeholder?: string;
  textarea?: boolean;
  rows?: number;
}

const InputField: React.FC<InputFieldProps> = ({
  label,
  id,
  type = 'text',
  value,
  onChange,
  error,
  required = false,
  placeholder = '',
  textarea = false,
  rows = 3
}) => {
  const [isFocused, setIsFocused] = useState(false);

  const inputClasses = `w-full px-4 py-3 bg-black/30 border ${error
    ? 'border-red-500 focus:ring-red-500'
    : isFocused
      ? 'border-cyan-400 focus:ring-cyan-400'
      : 'border-white/10 focus:ring-cyan-500'
    } rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:border-transparent transition-all duration-300`;

  return (
    <motion.div
      animate={error ? { x: [-5, 5, -5, 5, 0] } : {}}
      transition={{ duration: 0.5 }}
      className="relative"
    >
      {textarea ? (
        <>
          <textarea
            id={id}
            value={value}
            onChange={onChange}
            required={required}
            rows={rows}
            placeholder=" "
            className={`${inputClasses} resize-none`}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
          />
          <label
            className={`absolute left-4 transition-all duration-300 pointer-events-none ${value || isFocused
              ? '-top-2 text-xs text-cyan-400 font-medium bg-[#080a0f] px-1'
              : 'top-3 text-sm text-gray-400'
              }`}
          >
            {label} {required && <span className="text-red-500">*</span>}
          </label>
        </>
      ) : (
        <>
          <input
            type={type}
            id={id}
            value={value}
            onChange={onChange}
            required={required}
            placeholder=" "
            className={inputClasses}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
          />
          <label
            className={`absolute left-4 transition-all duration-300 pointer-events-none ${value || isFocused
              ? '-top-2 text-xs text-cyan-400 font-medium bg-[#080a0f] px-1'
              : 'top-3 text-sm text-gray-400'
              }`}
          >
            {label} {required && <span className="text-red-500">*</span>}
          </label>
        </>
      )}

      {error && (
        <p className="mt-2 text-sm text-red-500 flex items-center">
          <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          {error}
        </p>
      )}
    </motion.div>
  );
};

export default InputField;