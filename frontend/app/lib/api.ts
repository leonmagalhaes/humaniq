import { User, SkillAssessment, Challenge, ChallengeResult, UserBadge, ForumPost, ForumComment, Certificate } from './types';

const API_BASE_URL = 'http://localhost:5000/api';

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const token = localStorage.getItem('token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'An error occurred');
  }

  return response.json();
}

// Auth API
export const auth = {
  login: async (email: string, password: string) => {
    const response = await fetchWithAuth('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    localStorage.setItem('token', response.token);
    return response.user;
  },

  register: async (name: string, email: string, password: string) => {
    const response = await fetchWithAuth('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password }),
    });
    localStorage.setItem('token', response.token);
    return response.user;
  },

  logout: () => {
    localStorage.removeItem('token');
  },
};

// User API
export const users = {
  getProfile: async (): Promise<User> => {
    return fetchWithAuth('/users/profile');
  },

  updateProfile: async (data: Partial<User>): Promise<User> => {
    return fetchWithAuth('/users/profile', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },
};

// Skills API
export const skills = {
  submitAssessment: async (assessment: Partial<SkillAssessment>): Promise<SkillAssessment> => {
    return fetchWithAuth('/skills/assessment', {
      method: 'POST',
      body: JSON.stringify(assessment),
    });
  },

  getAssessment: async (): Promise<SkillAssessment> => {
    return fetchWithAuth('/skills/assessment');
  },
};

// Challenges API
export const challenges = {
  getAll: async (): Promise<Challenge[]> => {
    return fetchWithAuth('/challenges');
  },

  getById: async (id: number): Promise<Challenge> => {
    return fetchWithAuth(`/challenges/${id}`);
  },

  startChallenge: async (challengeId: number): Promise<ChallengeResult> => {
    return fetchWithAuth(`/challenges/${challengeId}/start`, {
      method: 'POST',
    });
  },

  submitChallenge: async (challengeId: number, data: Partial<ChallengeResult>): Promise<ChallengeResult> => {
    return fetchWithAuth(`/challenges/${challengeId}/submit`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};

// Badges API
export const badges = {
  getAll: async (): Promise<UserBadge[]> => {
    return fetchWithAuth('/badges');
  },

  getUserBadges: async (): Promise<UserBadge[]> => {
    return fetchWithAuth('/badges/user');
  },
};

// Forum API
export const forum = {
  getPosts: async (): Promise<ForumPost[]> => {
    return fetchWithAuth('/forum/posts');
  },

  getPost: async (id: number): Promise<ForumPost> => {
    return fetchWithAuth(`/forum/posts/${id}`);
  },

  createPost: async (data: Partial<ForumPost>): Promise<ForumPost> => {
    return fetchWithAuth('/forum/posts', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  createComment: async (postId: number, content: string): Promise<ForumComment> => {
    return fetchWithAuth(`/forum/posts/${postId}/comments`, {
      method: 'POST',
      body: JSON.stringify({ content }),
    });
  },
};

// Certificates API
export const certificates = {
  getAll: async (): Promise<Certificate[]> => {
    return fetchWithAuth('/certificates');
  },

  getById: async (id: number): Promise<Certificate> => {
    return fetchWithAuth(`/certificates/${id}`);
  },
};