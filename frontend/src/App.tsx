import { useState } from "react";
import { useQuery, useMutation } from "@apollo/client/react";

import { GET_PROJECTS } from "./graphql/projects";
import { GET_PROJECT, UPDATE_TASK } from "./graphql/tasks";

import type { Project, Task } from "./types";
import type {
  GetProjectsResponse,
  GetProjectResponse,
} from "./graphql/types";

export default function App() {
  const [selectedProjectId, setSelectedProjectId] = useState<string | null>(null);

  // --------------------
  // Queries
  // --------------------
  const projectsQuery = useQuery<GetProjectsResponse>(GET_PROJECTS);

  const projectQuery = useQuery<GetProjectResponse>(GET_PROJECT, {
    variables: { id: selectedProjectId },
    skip: !selectedProjectId,
  });

  // --------------------
  // Mutations
  // --------------------
  const [updateTask] = useMutation(UPDATE_TASK);

  // --------------------
  // Loading / Error
  // --------------------
  if (projectsQuery.loading) {
    return <p className="p-6">Loading projects...</p>;
  }

  if (projectsQuery.error) {
    return <p className="p-6">Failed to load projects</p>;
  }

  const projects: Project[] = projectsQuery.data?.projects || [];

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-xl font-bold mb-4">Projects</h1>

      {/* --------------------
          PROJECT LIST
      -------------------- */}
      <ul className="space-y-2 mb-6">
        {projects.map((project: Project) => (
          <li
            key={project.id}
            onClick={() => setSelectedProjectId(project.id)}
            className="border p-3 rounded cursor-pointer hover:bg-gray-50 flex justify-between"
          >
            <span>{project.name}</span>
            <span className="text-sm">{project.status}</span>
          </li>
        ))}
      </ul>

      {/* --------------------
          TASK LIST
      -------------------- */}
      {selectedProjectId && projectQuery.data && (
        <div className="mt-8">
          <h2 className="font-semibold mb-3">
            Tasks — {(projectQuery.data as GetProjectResponse).project.name}
          </h2>

          <ul className="space-y-2">
            {(projectQuery.data as GetProjectResponse).project.tasks.map((task: Task) => (
              <li
                key={task.id}
                className="border p-2 rounded flex justify-between items-center"
              >
                <span>{task.title}</span>

                <button
                  className="text-sm border px-2 py-1"
                  onClick={() =>
                    updateTask({
                      variables: {
                        id: task.id,
                        status: "DONE",
                      },

                      // ****** OPTIMISTIC UPDATE
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
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
