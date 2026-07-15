# TeamFlow EPMS — Architecture

## Overview

TeamFlow follows a **layered architecture** with clear separation of concerns. The system is split into a Next.js frontend and a Django backend communicating via REST API. Authentication uses HttpOnly Secure cookies — the frontend never handles tokens directly.

---

## System Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                            │
│  Next.js 16 (App Router, TypeScript, Tailwind, shadcn/ui)   │
│  Axios with withCredentials: true (cookie-based auth)       │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST (JSON)
┌──────────────────────────▼──────────────────────────────────┐
│                     API LAYER                               │
│  Django Ninja — /api/v1/                                    │
│  Request validation (Pydantic), exception handling          │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                 AUTHORIZATION LAYER                         │
│  Custom RBAC — Role → Permission (M2M via RolePermission)   │
│  Decorators: @require_permission, @require_role             │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   SERVICE LAYER                             │
│  Business logic classes (one per domain)                    │
│  No direct model access from API layer                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     DATA LAYER                              │
│  Django ORM — Models, Managers, QuerySets                   │
│  PostgreSQL 16                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Authentication Flow (Cookie-Based JWT)

```
1. User submits credentials → POST /api/v1/auth/login
2. Backend validates → sets HttpOnly Secure cookies:
   - access_token (short-lived, e.g. 30 min)
   - refresh_token (long-lived, e.g. 7 days)
3. Frontend Axios sends cookies automatically (withCredentials: true)
4. Backend middleware reads cookie → validates JWT → attaches user to request
5. On 401 → frontend redirects to /login
6. Refresh flow: POST /api/v1/auth/refresh (cookie auto-sent)
```

**Why cookies over localStorage:**
- HttpOnly flag prevents JavaScript access → immune to XSS token theft
- Secure flag ensures cookies only sent over HTTPS
- SameSite=Lax prevents CSRF on cross-origin requests

---

## RBAC Model

```
User ──FK──→ Role ──M2M──→ Permission
                    ↕
              RolePermission
              (through table)
```

- **No Django PermissionsMixin** for app-level auth
- `is_staff` / `is_superuser` on User model for Django admin only
- Custom `has_permission(codename)` method on User → delegates to Role
- Decorators check permissions at the API layer

### System Roles (hierarchy 0=highest)

| Level | Role             | Description                          |
|-------|------------------|--------------------------------------|
| 0     | Administrator    | Full system access                   |
| 1     | Faculty          | Academic oversight, project approval |
| 2     | Project Manager  | Full project lifecycle management    |
| 3     | Team Lead        | Team and sprint management           |
| 4     | Developer        | Task execution, code contributions   |
| 5     | QA Engineer      | Testing, bug reporting               |
| 6     | Stakeholder      | View progress, provide feedback      |
| 7     | Viewer           | Read-only access                     |

---

## Backend App Boundaries

Each Django app owns a single domain and exposes its functionality through a service class:

| App             | Domain                          | Dependencies          |
|-----------------|---------------------------------|-----------------------|
| accounts        | Users, roles, permissions       | core                  |
| organizations   | Multi-tenant orgs               | accounts, core        |
| projects        | Project lifecycle               | organizations, core   |
| teams           | Team membership                 | accounts, projects    |
| tasks           | Work items, bugs, tickets       | projects, teams       |
| meetings        | Scheduling, minutes             | projects, teams       |
| reports         | Engineering report generation   | projects, tasks       |
| notifications   | In-app + email alerts           | accounts, all events  |
| audit           | Audit trail                     | all models            |

**Rules:**
- Apps communicate through service classes, never import models from other apps directly
- Circular dependencies are resolved through signals or the audit app
- The `core` module provides shared base classes (BaseModel, exceptions, pagination)

---

## Frontend Architecture

```
app/                  → Routes (App Router, route groups)
├── (auth)/           → Unauthenticated pages (login, register)
└── (dashboard)/      → Authenticated pages (sidebar layout)

components/           → Reusable UI pieces
├── ui/               → shadcn/ui primitives
├── layout/           → Page structure (sidebar, header)
├── shared/           → Cross-feature components
└── theme/            → Theme switching

features/             → Feature modules (colocated logic + UI)
hooks/                → Custom React hooks
lib/                  → Utilities, constants, validations
services/             → API client + endpoint definitions
providers/            → React context providers
types/                → TypeScript type definitions
```

---

## Infrastructure

| Service    | Technology       | Purpose                    |
|------------|------------------|----------------------------|
| Backend    | Django 5.2 LTS   | API server                 |
| Frontend   | Next.js 16       | SSR/CSR web application    |
| Database   | PostgreSQL 16    | Primary data store         |
| Cache      | Redis 7          | Caching, sessions          |
| Workers    | Celery (Phase 2) | Background job processing  |

All services are containerized via Docker Compose for development.
