import React from 'react';
import { Search, Sparkles, Zap } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Container, Layout, PageHeader } from '../layouts/MainLayout';
import { useTrendingOpportunities } from '../hooks';
import { OpportunityCard } from '../components/OpportunityCard';
import { LoadingSpinner, EmptyState } from '../components/LoadingStates';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = React.useState('');
  const { data: trendingData, isLoading } = useTrendingOpportunities(7, 6);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}&mode=ai`);
    }
  };

  return (
    <Layout>
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
        <Container>
          <div className="py-20 text-center">
            <div className="mb-6 inline-block">
              <div className="w-16 h-16 bg-gradient-to-br from-accent to-blue-600 rounded-2xl flex items-center justify-center">
                <Sparkles className="w-8 h-8" />
              </div>
            </div>

            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Discover Real Student Opportunities
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              AI-powered platform for finding genuine internships, hackathons, contests, and more.
              Only active opportunities. Always fresh.
            </p>

            {/* Search Bar */}
            <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
              <div className="relative">
                <input
                  type="text"
                  placeholder="What are you looking for? (e.g., React internships, AI hackathons)"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-6 py-4 bg-white text-gray-900 rounded-xl shadow-lg focus:outline-none focus:ring-2 focus:ring-accent"
                />
                <button
                  type="submit"
                  className="absolute right-3 top-1/2 -translate-y-1/2 bg-accent hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors"
                >
                  <Search className="w-5 h-5" />
                </button>
              </div>
            </form>

            <div className="mt-8 flex justify-center gap-4 flex-wrap">
              <button
                onClick={() => navigate('/explore')}
                className="px-6 py-3 bg-accent hover:bg-blue-600 text-white rounded-lg font-medium transition-colors"
              >
                Explore All
              </button>
              <button
                onClick={() => navigate('/search?mode=ai')}
                className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
              >
                <Zap className="w-5 h-5" />
                AI Search
              </button>
            </div>
          </div>
        </Container>
      </div>

      {/* Trending Section */}
      <div className="py-16 bg-white dark:bg-slate-900">
        <Container>
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              🔥 Trending This Week
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Fresh opportunities trending among students
            </p>
          </div>

          {isLoading ? (
            <LoadingSpinner />
          ) : !trendingData?.data || trendingData.data.length === 0 ? (
            <EmptyState title="No trending opportunities yet" />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {trendingData.data.map((opportunity) => (
                <OpportunityCard key={opportunity.id} opportunity={opportunity} />
              ))}
            </div>
          )}
        </Container>
      </div>

      {/* Stats Section */}
      <div className="py-16 bg-gray-50 dark:bg-slate-800">
        <Container>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-accent mb-2">1000+</div>
              <p className="text-gray-600 dark:text-gray-400">Active Opportunities</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-500 mb-2">100% Fresh</div>
              <p className="text-gray-600 dark:text-gray-400">Never Expired Listings</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-500 mb-2">AI Powered</div>
              <p className="text-gray-600 dark:text-gray-400">Semantic Search</p>
            </div>
          </div>
        </Container>
      </div>

      {/* CTA Section */}
      <div className="py-16 bg-accent">
        <Container>
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white mb-4">
              Start Your Journey Today
            </h2>
            <p className="text-blue-100 mb-8 max-w-2xl mx-auto">
              Find opportunities that match your skills and interests. Bookmark, compare, and apply.
            </p>
            <button
              onClick={() => navigate('/explore')}
              className="px-8 py-3 bg-white text-accent hover:bg-gray-50 font-bold rounded-lg transition-colors"
            >
              Explore Opportunities →
            </button>
          </div>
        </Container>
      </div>
    </Layout>
  );
};
