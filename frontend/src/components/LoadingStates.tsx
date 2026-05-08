import React from 'react';

interface LoadingSkeletonProps {
  count?: number;
}

export const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({ count = 3 }) => {
  return (
    <div className="space-y-4">
      {Array.from({ length: count }).map((_, idx) => (
        <div key={idx} className="bg-white dark:bg-slate-800 rounded-lg p-5 animate-pulse">
          <div className="flex items-start justify-between gap-3 mb-3">
            <div className="flex-1">
              <div className="h-5 bg-gray-200 dark:bg-slate-700 rounded w-3/4 mb-2"></div>
              <div className="h-4 bg-gray-200 dark:bg-slate-700 rounded w-1/2"></div>
            </div>
            <div className="w-5 h-5 bg-gray-200 dark:bg-slate-700 rounded"></div>
          </div>
          <div className="h-4 bg-gray-200 dark:bg-slate-700 rounded w-2/3 mb-4"></div>
          <div className="space-y-2">
            <div className="h-3 bg-gray-200 dark:bg-slate-700 rounded w-full"></div>
            <div className="h-3 bg-gray-200 dark:bg-slate-700 rounded w-2/3"></div>
          </div>
        </div>
      ))}
    </div>
  );
};

export const LoadingSpinner: React.FC = () => {
  return (
    <div className="flex justify-center items-center py-8">
      <div className="w-8 h-8 border-4 border-gray-200 dark:border-slate-700 border-t-accent rounded-full animate-spin"></div>
    </div>
  );
};

export const EmptyState: React.FC<{ title: string; description?: string }> = ({
  title,
  description,
}) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="w-16 h-16 bg-gray-100 dark:bg-slate-800 rounded-full flex items-center justify-center mb-4">
        <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">{title}</h3>
      {description && (
        <p className="text-gray-600 dark:text-gray-400">{description}</p>
      )}
    </div>
  );
};
