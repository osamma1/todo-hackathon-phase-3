'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../hooks/useAuth';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const router = useRouter();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading && !user) {
      // Redirect to signin if not authenticated
      router.push('/signin');
    }
  }, [user, loading, router]);

  // Show loading state while checking authentication
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-2xl font-bold gradient-text">Loading...</div>
      </div>
    );
  }

  // If user is authenticated, show the protected content
  if (user) {
    return <>{children}</>;
  }

  // If not authenticated and not loading, return null (redirect effect will happen via useEffect)
  return null;
};

export default ProtectedRoute;