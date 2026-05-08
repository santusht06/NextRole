import React from 'react';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex flex-col min-h-screen">
      {children}
    </div>
  );
};

export const Container: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {children}
    </div>
  );
};

export const PageHeader: React.FC<{ title: string; subtitle?: string }> = ({
  title,
  subtitle,
}) => {
  return (
    <div className="py-8 bg-gradient-to-r from-slate-50 to-gray-50 dark:from-slate-900 dark:to-slate-800 border-b border-gray-200 dark:border-slate-800">
      <Container>
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          {title}
        </h1>
        {subtitle && (
          <p className="text-lg text-gray-600 dark:text-gray-400">
            {subtitle}
          </p>
        )}
      </Container>
    </div>
  );
};
