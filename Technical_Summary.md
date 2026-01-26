# Technical Summary

## Key Decisions

- Implemented multi-tenancy using request-scoped organization context instead of passing organization IDs through APIs.
- Used GraphQL to maintain a clear contract between frontend and backend.
- Designed strict data hierarchy: Organization → Project → Task → Comment.
- Kept frontend intentionally thin and backend-driven.

## Trade-offs

- Authentication was excluded to focus on multi-tenant architecture.
- Frontend UI kept minimal to prioritize correctness and clarity.
- No real-time subscriptions to avoid unnecessary complexity.

## Future Improvements

- Add authentication and role-based access control.
- Implement project statistics and analytics.
- Add task comments UI.
- Introduce GraphQL subscriptions for real-time updates.
- Dockerized production deployment and CI/CD.
