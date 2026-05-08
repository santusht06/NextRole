import React from 'react';
import clsx from 'clsx';

interface FilterChipProps {
  label: string;
  isActive: boolean;
  onClick: () => void;
}

export const FilterChip: React.FC<FilterChipProps> = ({ label, isActive, onClick }) => {
  return (
    <button
      onClick={onClick}
      className={clsx(
        "px-4 py-2 rounded-full font-medium transition-colors whitespace-nowrap",
        isActive
          ? "bg-accent text-white"
          : "bg-gray-100 dark:bg-slate-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-slate-700"
      )}
    >
      {label}
    </button>
  );
};

export const FilterBar: React.FC<{
  filters: Array<{ label: string; value: string }>;
  activeFilter: string | null;
  onFilterChange: (value: string | null) => void;
}> = ({ filters, activeFilter, onFilterChange }) => {
  return (
    <div className="flex gap-3 overflow-x-auto pb-4 scrollbar-hide">
      <FilterChip
        label="All"
        isActive={activeFilter === null}
        onClick={() => onFilterChange(null)}
      />
      {filters.map((filter) => (
        <FilterChip
          key={filter.value}
          label={filter.label}
          isActive={activeFilter === filter.value}
          onClick={() => onFilterChange(filter.value)}
        />
      ))}
    </div>
  );
};
