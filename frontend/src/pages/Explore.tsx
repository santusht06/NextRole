import React from 'react';
import { Container, Layout, PageHeader } from '../layouts/MainLayout';
import { useOpportunities } from '../hooks';
import { OpportunityCard } from '../components/OpportunityCard';
import { FilterBar } from '../components/FilterBar';
import { Pagination } from '../components/Pagination';
import { LoadingSpinner, EmptyState } from '../components/LoadingStates';

const OPPORTUNITY_TYPES = [
  { label: '💼 Internships', value: 'internship' },
  { label: '🚀 Hackathons', value: 'hackathon' },
  { label: '⚡ Contests', value: 'coding_contest' },
  { label: '🎓 Graduate Programs', value: 'graduate_program' },
  { label: '💻 Hiring Challenges', value: 'hiring_challenge' },
];

export const ExplorePage: React.FC = () => {
  const [currentPage, setCurrentPage] = React.useState(1);
  const [activeFilter, setActiveFilter] = React.useState<string | null>(null);
  const pageSize = 12;
  const skip = (currentPage - 1) * pageSize;

  const { data, isLoading } = useOpportunities(skip, pageSize, {
    opportunity_type: activeFilter || undefined,
  });

  const totalPages = data?.pagination?.total ? Math.ceil(data.pagination.total / pageSize) : 1;

  const handleFilterChange = (filter: string | null) => {
    setActiveFilter(filter);
    setCurrentPage(1);
  };

  return (
    <Layout>
      <PageHeader
        title="Explore Opportunities"
        subtitle="Browse all active opportunities across internships, hackathons, and more"
      />

      <div className="flex-1 bg-white dark:bg-slate-900">
        <Container>
          {/* Filters */}
          <div className="py-8">
            <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-4">
              Filter by Type
            </h3>
            <FilterBar
              filters={OPPORTUNITY_TYPES}
              activeFilter={activeFilter}
              onFilterChange={handleFilterChange}
            />
          </div>

          {/* Opportunities Grid */}
          {isLoading ? (
            <LoadingSpinner />
          ) : !data?.data || data.data.length === 0 ? (
            <EmptyState
              title="No opportunities found"
              description="Try adjusting your filters or check back later for new opportunities"
            />
          ) : (
            <>
              <div className="py-8">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {data.data.map((opportunity) => (
                    <OpportunityCard
                      key={opportunity.id}
                      opportunity={opportunity}
                    />
                  ))}
                </div>
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <Pagination
                  currentPage={currentPage}
                  totalPages={totalPages}
                  onPageChange={setCurrentPage}
                  isLoading={isLoading}
                />
              )}
            </>
          )}
        </Container>
      </div>
    </Layout>
  );
};
