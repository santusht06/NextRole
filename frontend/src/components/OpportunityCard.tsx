import React from 'react';
import { Bookmark, BookmarkCheck, MapPin, Calendar, Zap } from 'lucide-react';
import clsx from 'clsx';
import { Opportunity } from '../types';
import { formatDate, getDaysUntilDeadline, getOpportunityTypeColor, getOpportunityTypeLabel } from '../utils';
import { useSavedStore } from '../store';
import { savedAPI } from '../services/api';

interface OpportunityCardProps {
  opportunity: Opportunity;
  onSaveToggle?: () => void;
}

export const OpportunityCard: React.FC<OpportunityCardProps> = ({ opportunity, onSaveToggle }) => {
  const { isSaved, addSavedId, removeSavedId } = useSavedStore();
  const [isBookmarked, setIsBookmarked] = React.useState(isSaved(opportunity.id));
  const [isLoading, setIsLoading] = React.useState(false);

  const daysLeft = getDaysUntilDeadline(opportunity.deadline);
  const isClosingSoon = daysLeft >= 0 && daysLeft <= 7;
  const isExpired = daysLeft < 0;

  const handleBookmarkToggle = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    setIsLoading(true);
    try {
      if (isBookmarked) {
        await savedAPI.unsave(opportunity.id);
        setIsBookmarked(false);
        removeSavedId(opportunity.id);
      } else {
        await savedAPI.save(opportunity.id);
        setIsBookmarked(true);
        addSavedId(opportunity.id);
      }
      onSaveToggle?.();
    } catch (error) {
      console.error('Error toggling bookmark:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <a href={`/opportunity/${opportunity.id}`}>
      <div className={clsx(
        "bg-white dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700",
        "hover:border-accent dark:hover:border-accent hover:shadow-lg dark:hover:shadow-md",
        "transition-all duration-200 p-5 cursor-pointer h-full flex flex-col",
        isExpired && "opacity-60"
      )}>
        {/* Header */}
        <div className="flex items-start justify-between mb-3 gap-3">
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white truncate">
              {opportunity.title}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 truncate">
              {opportunity.company}
            </p>
          </div>
          <button
            onClick={handleBookmarkToggle}
            disabled={isLoading}
            className="flex-shrink-0 p-2 hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
          >
            {isBookmarked ? (
              <BookmarkCheck className="w-5 h-5 text-accent" />
            ) : (
              <Bookmark className="w-5 h-5 text-gray-400" />
            )}
          </button>
        </div>

        {/* Type Badge */}
        <div className="mb-3">
          <span className={clsx("inline-block px-3 py-1 rounded-full text-xs font-medium", getOpportunityTypeColor(opportunity.type))}>
            {getOpportunityTypeLabel(opportunity.type)}
          </span>
        </div>

        {/* Summary */}
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2 flex-grow">
          {opportunity.summary || opportunity.description.substring(0, 100)}
        </p>

        {/* Metadata */}
        <div className="space-y-2 mb-4 text-sm">
          {opportunity.location && (
            <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
              <MapPin className="w-4 h-4" />
              <span>{opportunity.location}</span>
              {opportunity.is_remote && <span className="text-xs bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-2 py-0.5 rounded">Remote</span>}
            </div>
          )}
          
          {opportunity.deadline && (
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              <span className={clsx(
                isClosingSoon && "text-red-600 dark:text-red-400 font-semibold",
                isExpired && "text-gray-400 line-through"
              )}>
                {isExpired ? "Expired" : formatDate(opportunity.deadline)}
              </span>
              {daysLeft >= 0 && (
                <span className={clsx(
                  "text-xs px-2 py-0.5 rounded",
                  isClosingSoon
                    ? "bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200"
                    : "bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200"
                )}>
                  {daysLeft} days left
                </span>
              )}
            </div>
          )}
        </div>

        {/* Skills Tags */}
        {opportunity.skills && opportunity.skills.length > 0 && (
          <div className="mb-4">
            <div className="flex items-center gap-1 flex-wrap">
              <Zap className="w-3 h-3 text-accent" />
              {opportunity.skills.slice(0, 3).map((skill, idx) => (
                <span key={idx} className="text-xs bg-gray-100 dark:bg-slate-700 text-gray-700 dark:text-gray-300 px-2 py-1 rounded">
                  {skill}
                </span>
              ))}
              {opportunity.skills.length > 3 && (
                <span className="text-xs text-gray-500">+{opportunity.skills.length - 3}</span>
              )}
            </div>
          </div>
        )}

        {/* CTA */}
        <button
          onClick={(e) => {
            e.preventDefault();
            window.open(opportunity.apply_link, '_blank');
          }}
          className="w-full bg-accent hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-lg transition-colors"
        >
          View & Apply
        </button>
      </div>
    </a>
  );
};
