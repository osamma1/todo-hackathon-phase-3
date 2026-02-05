'use client';

import React from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import GlassCard from '../../components/GlassCard';

const TermsAndConditionsPage = () => {
    return (
        <div className="min-h-screen bg-slate-950 py-20 px-4 relative overflow-hidden">
            {/* Subtle cyan background glow */}
            <div className="absolute inset-0 bg-cyan-900/10 blur-3xl"></div>

            <div className="container mx-auto max-w-4xl relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <GlassCard className="p-8 md:p-12">
                        <h1 className="text-4xl font-bold text-white mb-8 border-b border-white/10 pb-4">
                            Terms & <span className="text-cyan-400">Conditions</span>
                        </h1>

                        <div className="space-y-6 text-gray-300 leading-relaxed">
                            <section>
                                <h2 className="text-xl font-semibold text-white mb-3">1. Introduction</h2>
                                <p>
                                    Welcome to Todo App. By using our service, you agree to these terms. Please read them carefully.
                                    Our service allows you to manage tasks and stay organized efficiently using our modern interface.
                                </p>
                            </section>

                            <section>
                                <h2 className="text-xl font-semibold text-white mb-3">2. User Accounts</h2>
                                <p>
                                    To use certain features of the app, you must create an account. You are responsible for maintaining
                                    the confidentiality of your account information and for all activities that occur under your account.
                                </p>
                            </section>

                            <section>
                                <h2 className="text-xl font-semibold text-white mb-3">3. Data Privacy</h2>
                                <p>
                                    Your privacy is important to us. We use secure methods to store your task data and personal information.
                                    We do not share your personal data with third parties except as required to provide the service.
                                </p>
                            </section>

                            <section>
                                <h2 className="text-xl font-semibold text-white mb-3">4. Content</h2>
                                <p>
                                    You retain ownership of the content you create in the app. However, by using the app, you grant us
                                    a license to host and store your content for the purpose of providing the service to you.
                                </p>
                            </section>

                            <section>
                                <h2 className="text-xl font-semibold text-white mb-3">5. Termination</h2>
                                <p>
                                    We reserve the right to suspend or terminate your account if you violate these terms or use the
                                    service in a way that could harm other users or our infrastructure.
                                </p>
                            </section>
                        </div>

                        <div className="mt-12 pt-8 border-t border-white/10 flex justify-center">
                            <Link
                                href="/signup"
                                className="px-8 py-3 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-[0_0_15px_rgba(6,182,212,0.3)]"
                            >
                                Back to Sign Up
                            </Link>
                        </div>
                    </GlassCard>
                </motion.div>
            </div>
        </div>
    );
};

export default TermsAndConditionsPage;
