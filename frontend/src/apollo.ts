import { ApolloClient, InMemoryCache, HttpLink } from "@apollo/client";

const httpLink = new HttpLink({
  uri: "http://localhost:8000/graphql",
  headers: {
    "X-ORG": "org-one", // hardcoded intentionally
  },
});

export const client = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
});