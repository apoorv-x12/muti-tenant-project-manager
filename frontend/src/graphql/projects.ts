import { gql } from "@apollo/client";

export const GET_PROJECTS = gql`
  query {
    projects {
      id
      name
      status
    }
  }
`;

export const CREATE_PROJECT = gql`
  mutation CreateProject($name: String!) {
    createProject(name: $name) {
      project {
        id
        name
        status
      }
    }
  }
`;
