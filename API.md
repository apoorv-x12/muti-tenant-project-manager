# GraphQL API

## Queries

### List Projects
Returns all projects scoped to the organization.

query {
  projects {
    id
    name
    status
  }
}

---

### Get Project

query GetProject($id: ID!) {
  project(id: $id) {
    id
    name
    tasks {
      id
      title
      status
    }
  }
}

---

## Mutations

### Create Project
mutation {
  createProject(name: "Test") {
    project {
      id
      name
    }
  }
}

### Update Task
mutation UpdateTask($id: ID!, $status: String!) {
  updateTask(id: $id, status: $status) {
    task {
      id
      status
    }
  }
}
