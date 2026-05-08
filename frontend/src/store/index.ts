import { create } from 'zustand';
import type { Opportunity } from '../types';

interface OpportunityStore {
  opportunities: Opportunity[];
  setOpportunities: (opportunities: Opportunity[]) => void;
  addOpportunity: (opportunity: Opportunity) => void;
  removeOpportunity: (id: number) => void;
}

export const useOpportunityStore = create<OpportunityStore>((set) => ({
  opportunities: [],
  setOpportunities: (opportunities) => set({ opportunities }),
  addOpportunity: (opportunity) =>
    set((state) => ({
      opportunities: [opportunity, ...state.opportunities],
    })),
  removeOpportunity: (id) =>
    set((state) => ({
      opportunities: state.opportunities.filter((opp) => opp.id !== id),
    })),
}));

interface UIStore {
  isDarkMode: boolean;
  toggleDarkMode: () => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export const useUIStore = create<UIStore>((set) => ({
  isDarkMode: localStorage.getItem('darkMode') === 'true',
  toggleDarkMode: () =>
    set((state) => {
      const newValue = !state.isDarkMode;
      localStorage.setItem('darkMode', String(newValue));
      return { isDarkMode: newValue };
    }),
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
}));

interface SavedStore {
  savedIds: Set<number>;
  setSavedIds: (ids: Set<number>) => void;
  addSavedId: (id: number) => void;
  removeSavedId: (id: number) => void;
  isSaved: (id: number) => boolean;
}

export const useSavedStore = create<SavedStore>((set, get) => ({
  savedIds: new Set(),
  setSavedIds: (ids) => set({ savedIds: ids }),
  addSavedId: (id) =>
    set((state) => {
      const newSet = new Set(state.savedIds);
      newSet.add(id);
      return { savedIds: newSet };
    }),
  removeSavedId: (id) =>
    set((state) => {
      const newSet = new Set(state.savedIds);
      newSet.delete(id);
      return { savedIds: newSet };
    }),
  isSaved: (id) => get().savedIds.has(id),
}));
