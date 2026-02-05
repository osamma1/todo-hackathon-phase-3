'use client';

import React, { ReactNode } from 'react';
import { usePathname } from 'next/navigation';
import Navbar from '../components/Navbar';
import { useAuth } from '../hooks/useAuth';

interface LayoutProps {
  children: ReactNode;
}

const ClientLayout: React.FC<LayoutProps> = ({ children }) => {
  const pathname = usePathname();
  const { user } = useAuth();

  // Show navbar only on authenticated routes
  const showNavbar = pathname !== '/signin' && pathname !== '/signup' && user;

  return (
    <>
      {showNavbar && <Navbar />}
      <main>{children}</main>
    </>
  );
};

export default ClientLayout;