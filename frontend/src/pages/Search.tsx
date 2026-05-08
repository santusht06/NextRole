import React from 'react';
import { useSearchParams } from 'react-router-dom';
import { Search, Sparkles } from 'lucide-react';
import { Container, Layout } from '../layouts/MainLayout';
import { useSearchOpportunities, useSemanticSearch, useAIRecommendations } from '../hooks';
import { OpportunityCard } from '../components/OpportunityCard';
import { LoadingSpinner, EmptyState } from '../components/LoadingStates';

export const SearchPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const [searchInput, setSearchInput] = React.useState(searchParams.get('q') || '');
  const searchMode = (searchParams.get('mode') || 'semantic') as 'keyword' | 'semantic' | 'ai';

  // Fetch based on search mode
  const keywordSearch = useSearchOpportunities(searchInput);
  const semanticSearch = useSemanticSearch(searchInput);
  const aiRecommendations = useAIRecommendations(searchInput);

  const getCurrentData = () => {
    if (searchMode === 'keyword') return keywordSearch;
    if (searchMode === 'ai') return aiRecommendations;
    return semanticSearch;
  };

  const currentData = getCurrentData();
  const isLoading = currentData.isLoading;
  const opportunities = currentData.data?.data || [];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchInput.trim()) {
      window.location.search = `q=${encodeURIComponent(searchInput)}&mode=${searchMode}`;
    }
  };

  return (
    <Layout>
      <div className="bg-white dark:bg-slate-900 py-8">
        <Container>
          {/* Search Input */}
          <form onSubmit={handleSearch} className="mb-8">
            <div className="relative max-w-2xl">
              <input
                type="text"
                placeholder="Search opportunities..."
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                className="w-full px-6 py-4 bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-accent"
              />
              <button
                type="submit"
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                <Search className="w-5 h-5" />
              </button>
            </div>
          </form>

          {/* Search Mode Tabs */}
          {searchInput && (
            <div className="flex gap-4 mb-8 border-b border-gray-200 dark:border-slate-700">
              <button
                onClick={() => window.location.search = `q=${encodeURIComponent(searchInput)}&mode=keyword`}
                className={`pb-3 px-4 font-medium border-b-2 transition-colors ${
                  searchMode === 'keyword'
                    ? 'border-accent text-accent'
                    : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300'
                }`}
              >
                Keyword Search
              </button>
              <button
                onClick={() => window.location.search = `q=${encodeURIComponent(searchInput)}&mode=semantic`}
                className={`pb-3 px-4 font-medium border-b-2 transition-colors ${
                  searchMode === 'semantic'
                    ? 'border-accent text-accent'
                    : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300'
                }`}
              >
                Semantic Search
              </button>
              <button
                onClick={() => window.location.search = `q=${encodeURIComponent(searchInput)}&mode=ai`}
                className={`pb-3 px-4 font-medium border-b-2 transition-colors flex items-center gap-2 ${
                  searchMode === 'ai'
                    ? 'border-accent text-accent'
                    : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300'
                }`}
              >
                <Sparkles className="w-4 h-4" />
                AI Recommendations
              </button>
            </div>
          )}

          {/* Results */}
          {!searchInput ? (
            <EmptyState
              title="Start searching"
              description="Enter a query to find opportunities that match your interests"
            />
          ) : isLoading ? (
            <LoadingSpinner />
          ) : opportunities.length === 0 ? (
            <EmptyState
              title="No opportunities found"
              description={`Try different keywords or check our Explore page for more options`}
            />
          ) : (
            <>
              <div className="mb-6 text-sm text-gray-600 dark:text-gray-400">
                Found {opportunities.length} opportunity{opportunities.length !== 1 ? 'ies' : ''} for "{searchInput}"
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {opportunities.map((opportunity) => (
                  <OpportunityCard
                    key={opportunity.id}
                    opportunity={opportunity}
                  />
                ))}
              </div>
            </>
          )}
        </Container>
      </div>
    </Layout>
  );
};
