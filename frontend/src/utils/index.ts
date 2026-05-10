/**
 * Utility functions for the application
 */

/**
 * Format date to readable string
 */
export const formatDate = (dateString: string | null): string => {
  if (!dateString) return 'No deadline';
  
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  } catch {
    return 'Invalid date';
  }
};

/**
 * Get days until deadline
 */
export const getDaysUntilDeadline = (deadline: string | null): number => {
  if (!deadline) return -1;
  
  try {
    const deadlineDate = new Date(deadline);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    deadlineDate.setHours(0, 0, 0, 0);
    
    const diffTime = deadlineDate.getTime() - today.getTime();
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  } catch {
    return -1;
  }
};

/**
 * Get opportunity type color
 */
export const getOpportunityTypeColor = (type: string): string => {
  const colors: Record<string, string> = {
    internship: 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200',
    hackathon: 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200',
    coding_contest: 'bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-200',
    graduate_program: 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200',
    hiring_challenge: 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200',
  };
  return colors[type] || 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200';
};

/**
 * Get opportunity type label
 */
export const getOpportunityTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    internship: 'Internship',
    hackathon: 'Hackathon',
    coding_contest: 'Coding Contest',
    graduate_program: 'Graduate Program',
    hiring_challenge: 'Hiring Challenge',
  };
  return labels[type] || type;
};

/**
 * Truncate text to specified length
 */
export const truncateText = (text: string, length: number = 100): string => {
  if (text.length <= length) return text;
  return text.substring(0, length) + '...';
};

/**
 * Capitalize string
 */
export const capitalize = (str: string): string => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

/**
 * Format number with commas
 */
export const formatNumber = (num: number): string => {
  return num.toLocaleString('en-US');
};

/**
 * Debounce function
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout;
  
  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

/**
 * Throttle function
 */
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean;
  
  return function (...args: Parameters<T>) {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
};

/**
 * Get freshness label for opportunity
 */
export const getFreshnessLabel = (createdAt: string): string => {
  try {
    const created = new Date(createdAt);
    const now = new Date();
    const diffMs = now.getTime() - created.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return `${Math.floor(diffDays / 30)} months ago`;
  } catch {
    return 'Recently added';
  }
};

/**
 * Check if opportunity is fresh (added within last 7 days)
 */
export const isFresh = (createdAt: string): boolean => {
  try {
    const created = new Date(createdAt);
    const now = new Date();
    const diffMs = now.getTime() - created.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    return diffDays <= 7;
  } catch {
    return false;
  }
};

/**
 * Build query string from object
 */
export const buildQueryString = (params: Record<string, any>): string => {
  const filtered = Object.entries(params).filter(([, value]) => value !== undefined && value !== null && value !== '');
  return filtered.map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`).join('&');
};

/**
 * Parse query string to object
 */
export const parseQueryString = (queryString: string): Record<string, string> => {
  const params = new URLSearchParams(queryString);
  const obj: Record<string, string> = {};
  params.forEach((value, key) => {
    obj[key] = value;
  });
  return obj;
};
