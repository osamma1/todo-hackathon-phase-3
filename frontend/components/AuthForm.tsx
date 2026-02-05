'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';

interface AuthFormProps {
  type: 'signin' | 'signup';
  onSubmit: (data: any) => void;
  loading?: boolean;
}

const AuthForm: React.FC<AuthFormProps> = ({ type, onSubmit, loading = false }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      {type === 'signup' && (
        <div className="relative">
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 bg-black/30 border border-white/10 rounded-lg text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all duration-300 peer"
            placeholder=" "
          />
          <label
            className="absolute left-4 top-3 text-sm text-gray-400 transition-all duration-300 pointer-events-none peer-placeholder-shown:top-3 peer-placeholder-shown:text-sm peer-focus:-top-2 peer-focus:text-xs peer-focus:bg-[#080a0f] peer-focus:px-1 peer-focus:text-cyan-400 peer-focus:font-medium peer-[:not(:placeholder-shown)]:-top-2 peer-[:not(:placeholder-shown)]:text-xs peer-[:not(:placeholder-shown)]:bg-[#080a0f] peer-[:not(:placeholder-shown)]:px-1 peer-[:not(:placeholder-shown)]:text-cyan-400"
          >
            Full Name
          </label>
        </div>
      )}

      <div className="relative">
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          className="w-full px-4 py-3 bg-black/30 border border-white/10 rounded-lg text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all duration-300 peer"
          placeholder=" "
        />
        <label
          className="absolute left-4 top-3 text-sm text-gray-400 transition-all duration-300 pointer-events-none peer-placeholder-shown:top-3 peer-placeholder-shown:text-sm peer-focus:-top-2 peer-focus:text-xs peer-focus:bg-[#080a0f] peer-focus:px-1 peer-focus:text-cyan-400 peer-focus:font-medium peer-[:not(:placeholder-shown)]:-top-2 peer-[:not(:placeholder-shown)]:text-xs peer-[:not(:placeholder-shown)]:bg-[#080a0f] peer-[:not(:placeholder-shown)]:px-1 peer-[:not(:placeholder-shown)]:text-cyan-400"
        >
          Email
        </label>
      </div>

      <div className="relative">
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          minLength={8}
          className="w-full px-4 py-3 bg-black/30 border border-white/10 rounded-lg text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all duration-300 peer"
          placeholder=" "
        />
        <label
          className="absolute left-4 top-3 text-sm text-gray-400 transition-all duration-300 pointer-events-none peer-placeholder-shown:top-3 peer-placeholder-shown:text-sm peer-focus:-top-2 peer-focus:text-xs peer-focus:bg-[#080a0f] peer-focus:px-1 peer-focus:text-cyan-400 peer-focus:font-medium peer-[:not(:placeholder-shown)]:-top-2 peer-[:not(:placeholder-shown)]:text-xs peer-[:not(:placeholder-shown)]:bg-[#080a0f] peer-[:not(:placeholder-shown)]:px-1 peer-[:not(:placeholder-shown)]:text-cyan-400"
        >
          Password
        </label>
      </div>

      {type === 'signup' && (
        <div className="relative">
          <input
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 bg-black/30 border border-white/10 rounded-lg text-white placeholder-transparent focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all duration-300 peer"
            placeholder=" "
          />
          <label
            className="absolute left-4 top-3 text-sm text-gray-400 transition-all duration-300 pointer-events-none peer-placeholder-shown:top-3 peer-placeholder-shown:text-sm peer-focus:-top-2 peer-focus:text-xs peer-focus:bg-[#080a0f] peer-focus:px-1 peer-focus:text-cyan-400 peer-focus:font-medium peer-[:not(:placeholder-shown)]:-top-2 peer-[:not(:placeholder-shown)]:text-xs peer-[:not(:placeholder-shown)]:bg-[#080a0f] peer-[:not(:placeholder-shown)]:px-1 peer-[:not(:placeholder-shown)]:text-cyan-400"
          >
            Confirm Password
          </label>
        </div>
      )}
      {type === 'signup' && (
        <div className="flex items-start">
          <div className="flex items-center h-5">
            <input
              id="terms"
              name="terms"
              type="checkbox"
              required
              className="h-4 w-4 text-cyan-600 focus:ring-cyan-500 border-gray-600 rounded bg-black/30 cursor-pointer"
            />
          </div>
          <div className="ml-3 text-sm">
            <label htmlFor="terms" className="text-gray-300">
              I agree to the{' '}
              <Link
                href="/terms-and-conditions"
                target="_blank"
                className="text-cyan-400 hover:text-cyan-300 font-medium transition-colors"
                onClick={(e: React.MouseEvent) => e.stopPropagation()}
              >
                Terms & Conditions
              </Link>
            </label>
          </div>
        </div>
      )}

      <div className="flex items-center justify-between">
        {type === 'signin' && (
          <div className="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              className="h-4 w-4 text-cyan-600 focus:ring-cyan-500 border-gray-600 rounded bg-black/30"
            />
            <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-300">
              Remember me
            </label>
          </div>
        )}

        {type === 'signin' && (
          <div className="text-sm">
            <a href="#" className="font-medium text-cyan-400 hover:text-cyan-300 transition-colors">
              Forgot password?
            </a>
          </div>
        )}
      </div>

      <div>
        <button
          type="submit"
          disabled={loading}
          className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-cyan-600 hover:bg-cyan-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500 transition-all duration-300 transform hover:scale-105 disabled:opacity-50 shadow-[0_0_15px_rgba(6,182,212,0.3)]"
        >
          {loading ? (
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : null}
          {loading ? (type === 'signin' ? 'Signing in...' : 'Creating account...') : (type === 'signin' ? 'Sign in' : 'Create Account')}
        </button>
      </div>
    </motion.form>
  );
};

export default AuthForm;