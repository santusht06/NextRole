import React from 'react';
import { Container, Layout, PageHeader } from '../layouts/MainLayout';
import { useSavedOpportunities } from '../hooks';
import { OpportunityCard } from '../components/OpportunityCard';
import { LoadingSpinner, EmptyState } from '../components/LoadingStates';

export const SavedPage: React.FC = () => {
  const [currentPage, setCurrentPage] = React.useState(1);
  const pageSize = 12;
  const skip = (currentPage - 1) * pageSize;

  const { data, isLoading } = useSavedOpportunities(skip, pageSize);

  return (
    <Layout>
      <PageHeader
        title="Saved Opportunities"
        subtitle="Opportunities you've bookmarked for later"
      />

      <div className="flex-1 bg-white dark:bg-slate-900 py-12">
        <Container>
          {isLoading ? (
            <LoadingSpinner />
          ) : !data?.data || data.data.length === 0 ? (
            <EmptyState
              title="No saved opportunities yet"
              description="Bookmark opportunities while exploring to save them for later"
            />
          ) : (
            <>
              <div className="mb-6 text-sm text-gray-600 dark:text-gray-400">
                {data.total} opportunity{data.total !== 1 ? 'ies' : ''} saved
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {data.data.map((opportunity) => (
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
