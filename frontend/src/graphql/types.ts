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
    __typename: "UpdateTask";
    task: {
      __typename: "Task";
      id: string;
      status: string;
    };
  };
}
