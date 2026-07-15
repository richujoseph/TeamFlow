# Contributing to TeamFlow EPMS

Thank you for contributing to TeamFlow! This document outlines the development workflow, conventions, and processes.

---

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd teamflow
   ```

2. **Copy environment variables:**
   ```bash
   cp .env.example .env
   ```

3. **Start infrastructure (PostgreSQL + Redis + Backend):**
   ```bash
   docker compose up -d
   ```

4. **Start the frontend:**
   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```

5. **Verify:**
   - Backend health: http://localhost:8000/api/v1/health
   - Frontend: http://localhost:3000
   - Django Admin: http://localhost:8000/admin

---

## Branch Naming

Use the following prefixes:

| Prefix      | Purpose                           | Example                       |
|-------------|-----------------------------------|-------------------------------|
| `feature/`  | New features                      | `feature/task-crud`           |
| `fix/`      | Bug fixes                         | `fix/login-redirect`          |
| `chore/`    | Maintenance, tooling, deps        | `chore/update-django`         |
| `docs/`     | Documentation only                | `docs/api-endpoints`          |
| `refactor/` | Code restructuring (no behavior)  | `refactor/service-layer`      |
| `test/`     | Adding or updating tests          | `test/accounts-unit`          |

---

## Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:** `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `ci`, `style`, `perf`

**Scopes:** `backend`, `frontend`, `accounts`, `projects`, `tasks`, `docker`, `ci`

**Examples:**
```
feat(accounts): implement custom User model with email auth
fix(frontend): resolve sidebar collapse on mobile
chore(docker): update postgres to 16.4
docs(api): add health endpoint documentation
```

---

## Code Style

### Backend (Python)
- **Formatter:** Black (line length 88)
- **Import sorter:** isort (black profile)
- **Linter:** Ruff
- Run all: `pre-commit run --all-files`

### Frontend (TypeScript)
- **Formatter:** Prettier (2-space indent, single quotes, trailing commas)
- **Linter:** ESLint (Next.js config)
- Run: `pnpm lint`

---

## Pull Request Process

1. Create a branch from `main` using the naming convention above.
2. Make your changes with clear, atomic commits.
3. Ensure all linters pass (`pre-commit run --all-files` + `pnpm lint`).
4. Push and open a PR against `main`.
5. Fill out the PR template completely.
6. Request review from at least one team member.
7. Address review feedback.
8. Squash-merge after approval.

---

## Project Structure Rules

- **Backend apps** must follow the standard structure (models, schemas, services, api, admin, tests).
- **Frontend components** go in `components/` — feature-specific logic goes in `features/`.
- **No cross-app model imports** — use service classes or signals.
- **No business logic in API handlers** — delegate to service classes.
- **No hardcoded values** — use constants files or environment variables.
