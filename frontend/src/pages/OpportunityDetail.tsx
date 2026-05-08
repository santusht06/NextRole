import React from 'react';
import { useParams } from 'react-router-dom';
import { MapPin, Calendar, Link as LinkIcon, Bookmark, BookmarkCheck, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Container, Layout } from '../layouts/MainLayout';
import { useOpportunity, useCheckSaved } from '../hooks';
import { LoadingSpinner, EmptyState } from '../components/LoadingStates';
import { formatDate, getDaysUntilDeadline, getOpportunityTypeColor, getOpportunityTypeLabel } from '../utils';
import { savedAPI } from '../services/api';
import { useSavedStore } from '../store';

export const OpportunityDetailPage: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const opportunityId = id ? parseInt(id) : 0;

  const { data, isLoading, error } = useOpportunity(opportunityId);
  const opportunity = data?.data;

  const { isSaved, addSavedId, removeSavedId } = useSavedStore();
  const [isBookmarked, setIsBookmarked] = React.useState(isSaved(opportunityId));
  const [isBookmarkLoading, setIsBookmarkLoading] = React.useState(false);

  React.useEffect(() => {
    setIsBookmarked(isSaved(opportunityId));
  }, [opportunityId, isSaved]);

  const handleBookmarkToggle = async () => {
    setIsBookmarkLoading(true);
    try {
      if (isBookmarked) {
        await savedAPI.unsave(opportunityId);
        setIsBookmarked(false);
        removeSavedId(opportunityId);
      } else {
        await savedAPI.save(opportunityId);
        setIsBookmarked(true);
        addSavedId(opportunityId);
      }
    } catch (error) {
      console.error('Error toggling bookmark:', error);
    } finally {
      setIsBookmarkLoading(false);
    }
  };

  if (isLoading) return <LoadingSpinner />;
  
  if (error || !opportunity) {
    return (
      <Layout>
        <Container>
          <div className="py-16">
            <EmptyState title="Opportunity not found" />
            <button
              onClick={() => navigate('/explore')}
              className="mt-8 px-6 py-2 bg-accent text-white rounded-lg hover:bg-blue-600 transition-colors flex items-center gap-2 mx-auto"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Explore
            </button>
          </div>
        </Container>
      </Layout>
    );
  }

  const daysLeft = getDaysUntilDeadline(opportunity.deadline);
  const isClosingSoon = daysLeft >= 0 && daysLeft <= 7;
  const isExpired = daysLeft < 0;

  return (
    <Layout>
      <div className="bg-white dark:bg-slate-900 py-8">
        <Container>
          {/* Back Button */}
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-8 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back
          </button>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2">
              {/* Header */}
              <div className="mb-8">
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div>
                    <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
                      {opportunity.title}
                    </h1>
                    <p className="text-xl text-gray-600 dark:text-gray-400">
                      {opportunity.company}
                    </p>
                  </div>
                  <button
                    onClick={handleBookmarkToggle}
                    disabled={isBookmarkLoading}
                    className="flex-shrink-0 p-3 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
                  >
                    {isBookmarked ? (
                      <BookmarkCheck className="w-6 h-6 text-accent" />
                    ) : (
                      <Bookmark className="w-6 h-6 text-gray-400" />
                    )}
                  </button>
                </div>

                <span className={`inline-block px-4 py-2 rounded-full font-semibold text-white ${
                  opportunity.type === 'internship' ? 'bg-blue-600' :
                  opportunity.type === 'hackathon' ? 'bg-purple-600' :
                  opportunity.type === 'coding_contest' ? 'bg-green-600' :
                  opportunity.type === 'graduate_program' ? 'bg-orange-600' :
                  'bg-red-600'
                }`}>
                  {getOpportunityTypeLabel(opportunity.type)}
                </span>
              </div>

              {/* Key Details */}
              <div className="bg-gray-50 dark:bg-slate-800 rounded-lg p-6 mb-8 space-y-4">
                {opportunity.location && (
                  <div className="flex items-center gap-3">
                    <MapPin className="w-5 h-5 text-accent" />
                    <span className="text-gray-600 dark:text-gray-300">
                      {opportunity.location}
                      {opportunity.is_remote && " (Remote)"}
                    </span>
                  </div>
                )}

                {opportunity.deadline && (
                  <div className="flex items-center gap-3">
                    <Calendar className="w-5 h-5 text-accent" />
                    <span className={`font-semibold ${
                      isExpired ? 'text-gray-400 line-through' :
                      isClosingSoon ? 'text-red-600 dark:text-red-400' :
                      'text-gray-600 dark:text-gray-300'
                    }`}>
                      {isExpired ? 'Expired' : formatDate(opportunity.deadline)}
                      {daysLeft >= 0 && ` (${daysLeft} days left)`}
                    </span>
                  </div>
                )}

                {opportunity.source_url && (
                  <div className="flex items-center gap-3">
                    <LinkIcon className="w-5 h-5 text-accent" />
                    <a
                      href={opportunity.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-accent hover:underline"
                    >
                      View on original site
                    </a>
                  </div>
                )}
              </div>

              {/* Summary */}
              {opportunity.summary && (
                <div className="mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                    Overview
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                    {opportunity.summary}
                  </p>
                </div>
              )}

              {/* Description */}
              {opportunity.description && (
                <div className="mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                    About This Opportunity
                  </h2>
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                    <p className="text-gray-600 dark:text-gray-400 leading-relaxed whitespace-pre-line">
                      {opportunity.description}
                    </p>
                  </div>
                </div>
              )}

              {/* Eligibility */}
              {opportunity.eligibility && opportunity.eligibility.length > 0 && (
                <div className="mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                    Eligibility
                  </h2>
                  <ul className="space-y-2">
                    {opportunity.eligibility.map((item, idx) => (
                      <li key={idx} className="flex items-start gap-3 text-gray-600 dark:text-gray-400">
                        <span className="text-accent font-bold">✓</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Skills */}
              {opportunity.skills && opportunity.skills.length > 0 && (
                <div className="mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                    Required Skills
                  </h2>
                  <div className="flex flex-wrap gap-3">
                    {opportunity.skills.map((skill, idx) => (
                      <span
                        key={idx}
                        className="px-4 py-2 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm font-medium"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <div className="bg-gray-50 dark:bg-slate-800 rounded-lg p-6 sticky top-24">
                {isExpired ? (
                  <div className="text-center py-8">
                    <div className="text-4xl mb-3">📅</div>
                    <p className="text-gray-600 dark:text-gray-400 font-semibold">
                      This opportunity has expired
                    </p>
                  </div>
                ) : (
                  <>
                    <button
                      onClick={() => window.open(opportunity.apply_link, '_blank')}
                      className="w-full bg-accent hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-lg transition-colors mb-4"
                    >
                      Apply Now
                    </button>

                    {isClosingSoon && (
                      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-4">
                        <p className="text-sm text-red-700 dark:text-red-400 font-semibold">
                          ⚠️ Deadline closing soon! Apply now.
                        </p>
                      </div>
                    )}

                    <button
                      onClick={handleBookmarkToggle}
                      disabled={isBookmarkLoading}
                      className="w-full border-2 border-accent text-accent hover:bg-accent/10 font-bold py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
                    >
                      {isBookmarked ? (
                        <>
                          <BookmarkCheck className="w-5 h-5" />
                          Saved
                        </>
                      ) : (
                        <>
                          <Bookmark className="w-5 h-5" />
                          Save for Later
                        </>
                      )}
                    </button>
                  </>
                )}

                {/* Info Card */}
                <div className="mt-6 p-4 bg-white dark:bg-slate-900 rounded-lg space-y-3 text-sm">
                  <div>
                    <p className="text-gray-500 dark:text-gray-400">Posted On</p>
                    <p className="font-semibold text-gray-900 dark:text-white">
                      {formatDate(opportunity.created_at)}
                    </p>
                  </div>
                  {opportunity.source_url && (
                    <div>
                      <p className="text-gray-500 dark:text-gray-400">Source</p>
                      <p className="font-semibold text-gray-900 dark:text-white capitalize">
                        {opportunity.source_url.split('/')[2]}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </Container>
      </div>
    </Layout>
  );
};
