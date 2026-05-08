import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const opportunitiesAPI = {
  // List opportunities
  listOpportunities: (skip = 0, limit = 20, filters = {}) =>
    apiClient.get('/opportunities/', {
      params: { skip, limit, ...filters },
    }),

  // Get trending opportunities
  getTrending: (days = 7, limit = 10) =>
    apiClient.get('/opportunities/trending', {
      params: { days, limit },
    }),

  // Get single opportunity
  getOpportunity: (id) =>
    apiClient.get(`/opportunities/${id}`),

  // Get by type
  getByType: (type, skip = 0, limit = 20) =>
    apiClient.get(`/opportunities/type/${type}`, {
      params: { skip, limit },
    }),

  // Keyword search
  search: (query, skip = 0, limit = 20, opportunityType = null) =>
    apiClient.get('/search/', {
      params: { q: query, skip, limit, opportunity_type: opportunityType },
    }),

  // Semantic search
  semanticSearch: (query, limit = 20, opportunityType = null) =>
    apiClient.get('/search/semantic', {
      params: { q: query, limit, opportunity_type: opportunityType },
    }),

  // AI recommendations
  getAIRecommendations: (query, limit = 5) =>
    apiClient.get('/search/ai-recommendations', {
      params: { query, limit },
    }),
};

export const savedAPI = {
  // Get saved opportunities
  getSaved: (skip = 0, limit = 20) =>
    apiClient.get('/saved/', {
      params: { skip, limit },
    }),

  // Save opportunity
  save: (opportunityId) =>
    apiClient.post(`/saved/${opportunityId}`),

  // Unsave opportunity
  unsave: (opportunityId) =>
    apiClient.delete(`/saved/${opportunityId}`),

  // Check if saved
  checkSaved: (opportunityId) =>
    apiClient.get(`/saved/check/${opportunityId}`),
};

export default apiClient;
