import { gql } from "@apollo/client";

export const GET_PROJECT = gql`
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
`;

export const UPDATE_TASK = gql`
  mutation UpdateTask($id: ID!, $status: String!) {
    updateTask(id: $id, status: $status) {
      task {
        id
        status
      }
    }
  }
`;
