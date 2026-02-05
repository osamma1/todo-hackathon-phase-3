'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { signup } from '../../lib/api';
import GlassCard from '../../components/GlassCard';
import toast from 'react-hot-toast';

const SignupPage = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false); // <-- Added
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await signup({ email, password, name });
      toast.success('Account created successfully!');
      router.push('/signin');
    } catch (error) {
      console.error('Signup error:', error);
      toast.error('Signup failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        <GlassCard className="p-8 rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl shadow-xl">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-semibold text-white mb-2">
              Create Account
            </h1>
            <p className="text-sm text-gray-400">
              Join us to get started
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Name */}
            <div>
              <label className="block text-sm text-gray-300 mb-2">
                Full Name
              </label>
              <div className="relative">
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Your Full Name"
                  className="
                    w-full px-10 py-3 rounded-xl
                    bg-white/5 border border-white/15
                    text-white placeholder-gray-400
                    focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400
                    transition
                  "
                />
                <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fillRule="evenodd"
                      d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
              </div>
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm text-gray-300 mb-2">
                Email
              </label>
              <div className="relative">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="your@email.com"
                  className="
                    w-full px-10 py-3 rounded-xl
                    bg-white/5 border border-white/15
                    text-white placeholder-gray-400
                    focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400
                    transition
                  "
                />
                <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                    <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm text-gray-300 mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'} // <-- Toggle here
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength={8}
                  placeholder="••••••••"
                  className="
                    w-full px-10 py-3 rounded-xl
                    bg-white/5 border border-white/15
                    text-white placeholder-gray-400
                    focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400
                    transition
                  "
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-cyan-400"
                >
                  {showPassword ? '🙈' : '👁️'}
                </button>
                <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fillRule="evenodd"
                      d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
              </div>
            </div>

            {/* Terms */}
            <label className="flex items-center text-sm text-gray-300">
              <input type="checkbox" required className="mr-2 accent-cyan-400" />
              I agree to the&nbsp;
              <a href="/terms-and-conditions" className="text-cyan-400 hover:text-cyan-300">
                Terms & Conditions
              </a>
            </label>

            {/* Button */}
            <button
              type="submit"
              disabled={loading}
              className="
                w-full py-3 rounded-xl
                bg-cyan-500 hover:bg-cyan-600
                text-black font-medium
                transition-all
                disabled:opacity-50 disabled:cursor-not-allowed
              "
            >
              {loading ? 'Creating account...' : 'Create Account'}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-400">
            Already have an account?{' '}
            <Link href="/signin" className="text-cyan-400 hover:text-cyan-300">
              Sign in
            </Link>
          </p>
        </GlassCard>
      </motion.div>
    </div>
  );
};

export default SignupPage;
