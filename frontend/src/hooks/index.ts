import { useQuery } from '@tanstack/react-query';
import { opportunitiesAPI, savedAPI } from '../services/api';

export const useOpportunities = (skip = 0, limit = 20, filters = {}) => {
  return useQuery({
    queryKey: ['opportunities', skip, limit, filters],
    queryFn: () => opportunitiesAPI.listOpportunities(skip, limit, filters),
  });
};

export const useTrendingOpportunities = (days = 7, limit = 10) => {
  return useQuery({
    queryKey: ['trending', days, limit],
    queryFn: () => opportunitiesAPI.getTrending(days, limit),
  });
};

export const useOpportunity = (id: number) => {
  return useQuery({
    queryKey: ['opportunity', id],
    queryFn: () => opportunitiesAPI.getOpportunity(id),
    enabled: !!id,
  });
};

export const useSearchOpportunities = (query: string, skip = 0, limit = 20) => {
  return useQuery({
    queryKey: ['search', query, skip, limit],
    queryFn: () => opportunitiesAPI.search(query, skip, limit),
    enabled: query.length > 0,
  });
};

export const useSemanticSearch = (query: string, limit = 20) => {
  return useQuery({
    queryKey: ['semantic-search', query, limit],
    queryFn: () => opportunitiesAPI.semanticSearch(query, limit),
    enabled: query.length > 0,
  });
};

export const useAIRecommendations = (query: string, limit = 5) => {
  return useQuery({
    queryKey: ['ai-recommendations', query, limit],
    queryFn: () => opportunitiesAPI.getAIRecommendations(query, limit),
    enabled: query.length > 0,
  });
};

export const useSavedOpportunities = (skip = 0, limit = 20) => {
  return useQuery({
    queryKey: ['saved', skip, limit],
    queryFn: () => savedAPI.getSaved(skip, limit),
  });
};

export const useCheckSaved = (opportunityId: number) => {
  return useQuery({
    queryKey: ['check-saved', opportunityId],
    queryFn: () => savedAPI.checkSaved(opportunityId),
    enabled: !!opportunityId,
  });
};
