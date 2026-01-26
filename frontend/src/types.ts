export interface Task {
  id: string;
  title: string;
  description?: string;
  status: "TODO" | "IN_PROGRESS" | "DONE";
  assignee_email?: string;
  due_date?: string;
  created_at?: string;
  last_updated_at?: string;
  comments?: TaskComment[];
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  status: "ACTIVE" | "COMPLETED" | "ON_HOLD";
  due_date?: string;
  created_at?: string;
  last_updated_at?: string;
  tasks?: Task[];
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  contact_email: string;
  created_at?: string;
  last_updated_at?: string;
  projects?: Project[];
}

export interface TaskComment {
  id: string;
  content: string;
  author_email: string;
  created_at?: string;
  last_updated_at?: string;
}
