export interface Opportunity {
  id: number;
  title: string;
  company: string;
  description: string;
  type: string;
  deadline: string | null;
  location: string | null;
  is_remote: boolean;
  eligibility: string[];
  skills: string[];
  summary: string | null;
  apply_link: string;
  source_url: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string | null;
  profile_picture_url: string | null;
  college: string | null;
  batch_year: number | null;
  is_verified_student: boolean;
  is_admin: boolean;
  created_at: string;
}

export interface SearchFilters {
  query?: string;
  type?: string;
  location?: string;
  is_remote?: boolean;
  skip?: number;
  limit?: number;
}

export interface PaginationData {
  skip: number;
  limit: number;
  total: number;
}

export interface ListResponse<T> {
  data: T[];
  pagination?: PaginationData;
}

export interface SearchResponse {
  query: string;
  data: Opportunity[];
  pagination?: PaginationData;
}

export type OpportunityType = 'internship' | 'hackathon' | 'coding_contest' | 'graduate_program' | 'hiring_challenge';
