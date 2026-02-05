'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { toggleTaskCompletion, deleteTask, updateTask, Task } from '../lib/api';
import toast from 'react-hot-toast';
import GlassCard from './GlassCard';
import Modal from './Modal';
import TaskForm from './TaskForm';

interface TaskCardProps {
  task: Task;
  onTaskUpdate?: (updatedTask: Task) => void;
  onTaskDelete?: (taskId: string | number) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ task, onTaskUpdate, onTaskDelete }) => {
  const [isCompleted, setIsCompleted] = useState(task.completed);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  const handleToggleCompletion = async () => {
    try {
      const updatedTask = await toggleTaskCompletion(String(task.id));
      setIsCompleted(!isCompleted);
      onTaskUpdate && onTaskUpdate(updatedTask);
      toast.success(isCompleted ? 'Task marked as pending' : 'Task marked as completed');
    } catch (error) {
      console.error('Error toggling task completion:', error);
      toast.error('Failed to update task status');
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    setIsDeleting(true);
    try {
      await deleteTask(String(task.id));
      onTaskDelete && onTaskDelete(task.id);
      toast.success('Task deleted successfully');
    } catch (error) {
      console.error('Error deleting task:', error);
      toast.error('Failed to delete task');
      setIsDeleting(false);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleUpdateTask = async (taskData: { title: string; description?: string }) => {
    try {
      const updatedTask = await updateTask(String(task.id), taskData);
      onTaskUpdate && onTaskUpdate(updatedTask);
      setIsEditing(false);
      toast.success('Task updated successfully');
    } catch (error) {
      console.error('Error updating task:', error);
      toast.error('Failed to update task');
    }
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      whileHover={{ y: -10, scale: 1.03 }}
      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
    >
      <GlassCard hoverEffect={false} className="h-full flex flex-col">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center">
            <motion.input
              type="checkbox"
              id={`task-checkbox-${task.id}`}
              checked={isCompleted}
              onChange={handleToggleCompletion}
              className="h-5 w-5 rounded border-gray-600 bg-black/30 text-cyan-600 focus:ring-cyan-500 focus:ring-offset-0 cursor-pointer"
              whileTap={{ scale: 1.2 }}
              aria-label={`Mark task "${task.title}" as ${isCompleted ? 'incomplete' : 'complete'}`}
            />
            <motion.label
              className={`ml-3 text-lg font-medium ${isCompleted ? 'line-through text-cyan-400/70' : 'text-white'}`}
              animate={{
                color: isCompleted ? '#22d3ee' : '#ffffff',
                textDecoration: isCompleted ? 'line-through' : 'none'
              }}
              transition={{ duration: 0.3 }}
              htmlFor={`task-checkbox-${task.id}`}
            >
              {task.title}
            </motion.label>
          </div>

          <div className="flex space-x-2">
            <button
              className="text-cyan-400 hover:text-cyan-300 transition-colors"
              onClick={handleEdit}
              aria-label="Edit task"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button
              className="text-red-500 hover:text-red-400 transition-colors"
              onClick={handleDelete}
              disabled={isDeleting}
              aria-label="Delete task"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>

        {task.description && (
          <div className="text-gray-300 mb-4 flex-grow">
            <p className="truncate max-w-full">{task.description}</p>
          </div>
        )}

        <div className="text-xs text-gray-400 mt-auto pt-2 border-t border-white/10">
          Created: {new Date(task.created_at).toLocaleDateString()}
        </div>
      </GlassCard>

      {/* Edit Task Modal */}
      <Modal
        isOpen={isEditing}
        onClose={() => setIsEditing(false)}
        title="Edit Task"
      >
        <TaskForm
          task={task}
          onSubmit={handleUpdateTask}
          onCancel={() => setIsEditing(false)}
        />
      </Modal>
    </motion.div>
  );
};

export default TaskCard;