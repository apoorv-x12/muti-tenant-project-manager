# Multi-Tenant Project Management System

A simplified multi-tenant project management application built to demonstrate clean backend architecture, GraphQL design, and a typed React frontend.

This project focuses on correct data modeling, organization isolation, and clear frontend–backend contracts.

---

## Tech Stack

Backend:
- Django 4.x
- Graphene (GraphQL)
- PostgreSQL
- Django ORM

Frontend:
- React 18
- TypeScript
- Apollo Client
- TailwindCSS

---

## Features

Backend:
- Organization, Project, Task, and TaskComment models
- Relational hierarchy:

Organization → Projects → Tasks → Comments

- GraphQL API for project, task, and comment management
- Organization-based data isolation using request context
- No organization IDs exposed in the API

Frontend:
- Project dashboard with status indicators
- Task list per project
- Task status updates
- Optimistic UI updates
- Typed GraphQL responses
- Loading and error handling
- Clean responsive UI

---

## Architecture

┌──────────────────────────┐
│        Frontend          │
│      React + TypeScript  │
│      Apollo Client       │
└─────────────┬────────────┘
              │ GraphQL
              ▼
┌──────────────────────────┐
│        Django API        │
│        Graphene          │
│                          │
│   Organization Middleware│
│   (X-ORG → context.org)  │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│        PostgreSQL        │
│   Organization           │
│     └── Project          │
│           └── Task       │
│                 └── Comment
└──────────────────────────┘

---

## Multi-Tenancy

Each request must include the header:

X-ORG: org-name

The organization is resolved via middleware and attached to the GraphQL context.  
All queries and mutations are automatically scoped to the active organization, ensuring strict data isolation.

---

## Setup Instructions

Backend:

cd backend  
python -m venv venv  

Activate virtual environment:

Windows  
venv\Scripts\activate  

Mac / Linux  
source venv/bin/activate  

Install dependencies:

pip install -r requirements.txt  

Run migrations:

python manage.py migrate  

Start server:

python manage.py runserver  

GraphQL endpoint:

http://localhost:8000/graphql/

---

Frontend:

cd frontend  
npm install  
npm run dev  

Frontend runs at:

http://localhost:5173

---

## Trade-offs

- Authentication intentionally omitted to focus on multi-tenant architecture
- Minimal frontend forms to keep scope aligned
- No real-time subscriptions
- Apollo default cache used for simplicity

---

## Future Improvements

- User authentication and roles
- Task comments UI
- Pagination and filtering
- Real-time updates
- Dockerized deployment
- CI/CD pipeline

---

Author: Apoorv Shrivastava
