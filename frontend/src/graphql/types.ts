import type { Project, Task } from "../types";

export interface GetProjectsResponse {
  projects: Project[];
}

export interface GetProjectResponse {
  project: Project & {
    tasks: Task[];
  };
}

export interface UpdateTaskResponse {
  updateTask: {
    task: {
      id: string;
      status: string;
    };
  };
}
