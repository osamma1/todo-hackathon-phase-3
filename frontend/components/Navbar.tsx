'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../hooks/useAuth';
import { motion } from 'framer-motion';

const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <motion.nav
      className="
        fixed top-0 left-0 right-0 z-50
        bg-black/30 backdrop-blur-xl border-b border-white/20
        shadow-lg
      "
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
    >
      <div className="container mx-auto flex justify-between items-center py-3 px-4 md:px-8">
        {/* Logo / Brand */}
        <Link
          href="/dashboard"
          className="
            text-2xl md:text-3xl font-bold
            text-white hover:text-cyan-400
            transition-colors duration-300
          "
        >
          Todo
        </Link>

        {/* User Section */}
        {user && (
          <div className="flex items-center space-x-4">
            <span className="text-gray-300 text-sm md:text-base">
              Welcome,&nbsp;
              <span className="text-cyan-400 font-medium">
                {user.name || user.email}
              </span>
            </span>

            {/* Avatar with pulse effect */}
            <div className="relative">
              <div className="
                w-10 h-10 md:w-12 md:h-12 rounded-full
                bg-cyan-500 flex items-center justify-center
                text-white font-bold text-sm md:text-base
                border-2 border-cyan-400
                hover:scale-110 transition-transform duration-300
              ">
                {user.name
                  ? user.name.charAt(0).toUpperCase()
                  : user.email.charAt(0).toUpperCase()}
              </div>
              <div className="
                absolute inset-0 rounded-full border border-cyan-400
                animate-ping opacity-40
              "></div>
            </div>

            {/* Logout button */}
            <button
              onClick={logout}
              className="
                px-4 py-2 rounded-lg text-sm font-medium
                text-gray-300 hover:text-white hover:bg-cyan-500/20
                transition-colors duration-300
              "
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </motion.nav>
  );
};

export default Navbar;
