import '../styles/globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import ToastProvider from '../components/ToastProvider';
import ClientLayout from '../components/ClientLayout';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A beautiful and modern todo application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className + ' bg-slate-950 text-gray-100'}>
        <ToastProvider />
        <ClientLayout>{children}</ClientLayout>
      </body>
    </html>
  );
}