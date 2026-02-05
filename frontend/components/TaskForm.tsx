'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import AuthButton from './AuthButton';
import InputField from './InputField';
import { Task } from '../lib/api';

interface TaskFormProps {
  task?: Task;
  onSubmit: (data: { title: string; description?: string }) => void;
  onCancel: () => void;
  loading?: boolean;
}

const TaskForm: React.FC<TaskFormProps> = ({ task, onSubmit, onCancel, loading = false }) => {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [titleError, setTitleError] = useState('');
  const [descriptionError, setDescriptionError] = useState('');

  const validateForm = () => {
    let isValid = true;

    // Validate title
    if (!title.trim()) {
      setTitleError('Title is required');
      isValid = false;
    } else if (title.trim().length < 1) {
      setTitleError('Title must be at least 1 character');
      isValid = false;
    } else if (title.trim().length > 200) {
      setTitleError('Title must be less than 200 characters');
      isValid = false;
    } else {
      setTitleError('');
    }

    // Validate description
    if (description && description.length > 1000) {
      setDescriptionError('Description must be less than 1000 characters');
      isValid = false;
    } else {
      setDescriptionError('');
    }

    return isValid;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      onSubmit({ title: title.trim(), description: description.trim() || undefined });
    }
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="space-y-6"
    >
      <InputField
        label="Task Title"
        id="task-title"
        type="text"
        value={title}
        onChange={(e) => {
          setTitle(e.target.value);
          if (titleError) setTitleError(''); // Clear error when user starts typing
        }}
        error={titleError}
        required={true}
        placeholder="Enter task title"
      />

      <InputField
        label="Description"
        id="task-description"
        value={description}
        onChange={(e) => {
          setDescription(e.target.value);
          if (descriptionError) setDescriptionError(''); // Clear error when user starts typing
        }}
        error={descriptionError}
        placeholder="Enter task description (optional)"
        textarea={true}
        rows={3}
      />

      <div className="flex justify-end space-x-3 pt-2">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
        >
          Cancel
        </button>
        <AuthButton
          type="submit"
          disabled={loading}
          className="px-6"
        >
          {loading ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {task ? 'Updating...' : 'Creating...'}
            </>
          ) : task ? 'Update Task' : 'Create Task'}
        </AuthButton>
      </div>
    </motion.form>
  );
};

export default TaskForm;