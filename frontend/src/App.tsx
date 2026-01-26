import { useState } from "react";
import { useQuery, useMutation } from "@apollo/client/react";

import { GET_PROJECTS } from "./graphql/projects";
import { GET_PROJECT, UPDATE_TASK } from "./graphql/tasks";

import type { Project, Task } from "./types";
import type {
  GetProjectsResponse,
  GetProjectResponse,
  UpdateTaskResponse,
} from "./graphql/types";

export default function App() {
  const [selectedProjectId, setSelectedProjectId] = useState<string | null>(null);

  const projectsQuery = useQuery<GetProjectsResponse>(GET_PROJECTS);

  const projectQuery = useQuery<GetProjectResponse>(GET_PROJECT, {
    variables: { id: selectedProjectId },
    skip: !selectedProjectId,
  });

  const [updateTask] = useMutation<UpdateTaskResponse>(UPDATE_TASK);

  if (projectsQuery.loading)
    return <p className="p-6 text-gray-500">Loading projects...</p>;

  if (projectsQuery.error)
    return <p className="p-6 text-red-500">Failed to load projects</p>;

  const projects = projectsQuery.data?.projects ?? [];

  const statusBadge = (status: string) => {
    const base = "text-xs px-2 py-1 rounded font-medium";

    switch (status) {
      case "ACTIVE":
        return `${base} bg-blue-100 text-blue-700`;
      case "COMPLETED":
        return `${base} bg-green-100 text-green-700`;
      case "ON_HOLD":
        return `${base} bg-yellow-100 text-yellow-700`;
      default:
        return `${base} bg-gray-100 text-gray-700`;
    }
  };

  const taskStatus = (status: string) => {
    switch (status) {
      case "DONE":
        return "text-green-600 line-through";
      case "IN_PROGRESS":
        return "text-blue-600";
      default:
        return "text-gray-700";
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-semibold mb-6">Project Dashboard</h1>

        {/* PROJECT LIST */}
        <ul className="space-y-3">
          {projects.map((project: Project) => (
            <li
              key={project.id}
              onClick={() => setSelectedProjectId(project.id)}
              className={`p-4 border rounded cursor-pointer transition
                ${
                  selectedProjectId === project.id
                    ? "border-blue-500 bg-blue-50"
                    : "hover:bg-gray-50"
                }`}
            >
              <div className="flex justify-between items-center">
                <span className="font-medium">{project.name}</span>
                <span className={statusBadge(project.status)}>
                  {project.status}
                </span>
              </div>
            </li>
          ))}
        </ul>

        {/* TASK LIST */}
        {selectedProjectId && projectQuery.data && (
          <div className="mt-8">
            <h2 className="text-lg font-semibold mb-4">
              Tasks — {projectQuery.data.project.name}
            </h2>

            <ul className="space-y-3">
              {projectQuery.data.project.tasks.map((task: Task) => (
                <li
                  key={task.id}
                  className="border rounded p-3 flex justify-between items-center"
                >
                  <span className={taskStatus(task.status)}>
                    {task.title}
                  </span>

                  {task.status !== "DONE" && (
                    <button
                      className="text-sm px-3 py-1 border rounded hover:bg-green-50 hover:border-green-400 transition"
                      onClick={() =>
                        updateTask({
                          variables: {
                            id: task.id,
                            status: "DONE",
                          },
                          optimisticResponse: {
                            updateTask: {
                              __typename: "UpdateTask",
                              task: {
                                __typename: "Task",
                                id: task.id,
                                status: "DONE",
                              },
                            },
                          },
                        })
                      }
                    >
                      Mark Done
                    </button>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
