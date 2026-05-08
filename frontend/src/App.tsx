import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Header } from './components/Header';
import { HomePage } from './pages/Home';
import { ExplorePage } from './pages/Explore';
import { SearchPage } from './pages/Search';
import { SavedPage } from './pages/Saved';
import { OpportunityDetailPage } from './pages/OpportunityDetail';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="bg-white dark:bg-slate-900 text-gray-900 dark:text-white">
          <Header />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/explore" element={<ExplorePage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/saved" element={<SavedPage />} />
            <Route path="/opportunity/:id" element={<OpportunityDetailPage />} />
          </Routes>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
