'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../hooks/useAuth';

const HomePage = () => {
  const router = useRouter();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading) {
      if (user) {
        router.push('/dashboard');
      } else {
        router.push('/signin');
      }
    }
  }, [user, loading, router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 relative overflow-hidden">
      {/* Subtle cyan background glow */}
      <div className="absolute inset-0 bg-cyan-900/20 blur-3xl"></div>

      <div className="relative z-10 text-center p-8 bg-white/5 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/10">
        <h1 className="text-5xl font-extrabold text-white mb-4 tracking-wide">
          Todo App
        </h1>
        <p className="text-gray-300 text-lg animate-pulse">
          Loading...
        </p>
      </div>
    </div>
  );
};

export default HomePage;
