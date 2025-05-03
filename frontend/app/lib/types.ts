export interface User {
  id: number;
  name: string;
  email: string;
  points: number;
  level: number;
  created_at: string;
  last_login: string;
}

export interface SkillAssessment {
  id: number;
  user_id: number;
  communication: number;
  active_listening: number;
  conflict_resolution: number;
  teamwork: number;
  critical_thinking: number;
  time_management: number;
  assessment_date: string;
}

export interface Challenge {
  id: number;
  title: string;
  description: string;
  skill_type: string;
  challenge_type: string;
  content: string;
  points: number;
  created_at: string;
}

export interface ChallengeResult {
  id: number;
  user_id: number;
  challenge_id: number;
  completed: boolean;
  score: number;
  feedback: string;
  completed_at: string;
}

export interface UserBadge {
  id: number;
  name: string;
  description: string;
  image_url: string;
  requirement: string;
}

export interface ForumPost {
  id: number;
  user_id: number;
  title: string;
  content: string;
  created_at: string;
  user?: User;
  comments?: ForumComment[];
}

export interface ForumComment {
  id: number;
  post_id: number;
  user_id: number;
  content: string;
  created_at: string;
  user?: User;
}

export interface Certificate {
  id: number;
  user_id: number;
  title: string;
  description: string;
  issue_date: string;
}