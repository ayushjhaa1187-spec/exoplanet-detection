import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Navbar from '@/components/layout/Navbar';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });

export const metadata: Metadata = {
  title: "ExoAstro | AI Exoplanet Detection",
  description: "End-to-end ML pipeline for Kepler exoplanet candidates",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans antialiased`}>
        <div className="flex flex-col min-h-screen">
          <Navbar />
          <main className="flex-1 px-4 py-8 max-w-7xl mx-auto w-full">
            {children}
          </main>
          <footer className="border-t border-slate-800/50 py-6 text-center text-xs text-slate-600">
            ExoAstro Pipeline &mdash; AstroNet CNN + PyTransit + Lightkurve &mdash; v1.0-beta
          </footer>
        </div>
      </body>
    </html>
  );
}
