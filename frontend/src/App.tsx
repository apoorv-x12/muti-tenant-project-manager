import { useQuery, useMutation } from "@apollo/client/react";
import { GET_PROJECTS, CREATE_PROJECT } from "./graphql/projects";
import { useState } from "react";

export default function App() {
  const { data, loading, error, refetch } = useQuery(GET_PROJECTS);
  const [createProject] = useMutation(CREATE_PROJECT);
  const [name, setName] = useState("");

  if (loading) return <p className="p-6">Loading...</p>;
  if (error) return <p className="p-6">Error loading projects</p>;

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-xl font-bold mb-4">Projects</h1>

      <ul className="space-y-2 mb-6">
        {data.projects.map((p: any) => (
          <li
            key={p.id}
            className="border p-3 rounded flex justify-between"
          >
            <span>{p.name}</span>
            <span className="text-sm">{p.status}</span>
          </li>
        ))}
      </ul>

      <form
        onSubmit={async (e) => {
          e.preventDefault();
          if (!name.trim()) return;

          await createProject({ variables: { name } });
          setName("");
          refetch();
        }}
        className="flex gap-2"
      >
        <input
          className="border p-2 flex-1"
          placeholder="Project name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button className="bg-black text-white px-4">
          Create
        </button>
      </form>
    </div>
  );
}
