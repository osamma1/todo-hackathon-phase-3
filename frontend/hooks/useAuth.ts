'use client';

import { useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { getAuthUser } from '../lib/api';

interface AuthUser {
  user_id: string | number;
  email: string;
  name: string;
  is_authenticated: boolean;
}

export const useAuth = () => {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const router = useRouter();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const userData = await getAuthUser();
        if (userData && userData.is_authenticated) {
          setUser(userData);
        } else {
          setUser(null);
        }
      } catch (error) {
        console.error('Failed to fetch auth user:', error);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();

    // Listen for storage changes (for multiple tabs or login events)
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'auth_token') {
        fetchUser();
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const logout = () => {
    setUser(null);
    // Remove token from local storage if it exists
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
    router.push('/signin');
  };

  return { user, loading, logout };
};