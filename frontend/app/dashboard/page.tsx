'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../../hooks/useAuth';
import { getTasks, createTask, Task } from '../../lib/api';
import ProtectedRoute from '../../components/ProtectedRoute';
import Navbar from '../../components/Navbar';
import TaskCard from '../../components/TaskCard';
import GlassCard from '../../components/GlassCard';
import Modal from '../../components/Modal';
import TaskForm from '../../components/TaskForm';
import ChatIcon from '../../components/Chat/ChatIcon';
import toast from 'react-hot-toast';

const DashboardPage = () => {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const tasksData = await getTasks();
        setTasks(tasksData);
      } catch (error) {
        console.error('Failed to fetch tasks:', error);
      } finally {
        setLoading(false);
      }
    };

    if (user) fetchTasks();
  }, [user]);

  const handleCreateTask = async (taskData: { title: string; description?: string }) => {
    try {
      const newTask = await createTask(taskData);
      setTasks([newTask, ...tasks]);
      toast.success('Task created successfully!');
      setIsModalOpen(false);
    } catch (error) {
      console.error('Failed to create task:', error);
      toast.error('Failed to create task');
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-slate-950 pt-28 pb-12 relative">
        <Navbar />

        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="container mx-auto px-4 mb-12 text-center"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-2">
            Your Tasks
          </h1>
          <p className="text-gray-400 text-lg">
            Manage your tasks efficiently
          </p>
        </motion.div>

        <div className="container mx-auto px-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {loading ? (
            Array.from({ length: 3 }).map((_, idx) => (
              <GlassCard key={idx} className="h-44 animate-pulse">
                <div className="h-full flex flex-col justify-center items-center">
                  <div className="bg-gray-700 rounded-full w-12 h-12 mb-4"></div>
                  <div className="h-4 bg-gray-700 rounded w-3/4 mb-2"></div>
                  <div className="h-3 bg-gray-700 rounded w-1/2"></div>
                </div>
              </GlassCard>
            ))
          ) : tasks.length > 0 ? (
            tasks.map((task) => (
              <motion.div
                key={task.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <TaskCard
                  task={task}
                  onTaskUpdate={(updatedTask) =>
                    setTasks((prev) =>
                      prev.map((t) =>
                        String(t.id) === String(updatedTask.id) ? updatedTask : t
                      )
                    )
                  }
                  onTaskDelete={(taskId) =>
                    setTasks((prev) => prev.filter((t) => String(t.id) !== String(taskId)))
                  }
                />
              </motion.div>
            ))
          ) : (
            <div className="col-span-full text-center py-12">
              <GlassCard className="inline-block p-8">
                <h3 className="text-xl font-semibold text-gray-300 mb-2">
                  No tasks yet
                </h3>
                <p className="text-gray-400">
                  Create your first task to get started
                </p>
              </GlassCard>
            </div>
          )}
        </div>

        {/* Floating Add Button */}
        <motion.button
          className="fixed bottom-8 right-8 w-16 h-16 rounded-full bg-cyan-600 flex items-center justify-center text-white shadow-lg z-40 hover:bg-cyan-500"
          whileHover={{ scale: 1.1, boxShadow: "0 0 25px rgba(6, 182, 212, 0.6)" }}
          whileTap={{ scale: 0.95 }}
          animate={{
            boxShadow: [
              "0 0 10px rgba(6, 182, 212, 0.4)",
              "0 0 20px rgba(6, 182, 212, 0.7)",
              "0 0 10px rgba(6, 182, 212, 0.4)"
            ]
          }}
          transition={{ boxShadow: { duration: 2, repeat: Infinity, ease: "easeInOut" } }}
          onClick={() => setIsModalOpen(true)}
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        </motion.button>

        {/* Task Creation Modal */}
        <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Create New Task">
          <TaskForm onSubmit={handleCreateTask} onCancel={() => setIsModalOpen(false)} />
        </Modal>

        {/* Chat Icon */}
        <ChatIcon />
      </div>
    </ProtectedRoute>
  );
};

export default DashboardPage;
