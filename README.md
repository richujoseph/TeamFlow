<div align="center">
  <img src="./frontend/public/next.svg" alt="TeamFlow Logo" width="120" />
  
  # TeamFlow EPMS
  **Enterprise Project Management & Engineering Collaboration Platform**

  <p align="center">
    The all-in-one platform that brings the power of Jira, GitLab Issues, and Confluence into one seamless, unified, and beautifully designed experience. Built specifically for modern software engineering teams.
  </p>

  <div>
    <img src="https://img.shields.io/badge/Status-In_Development-blue?style=for-the-badge" alt="Status" />
    <img src="https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
    <img src="https://img.shields.io/badge/Next.js-16-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js" />
    <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
    <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  </div>
</div>

<br />

---

## 🚀 Overview

**TeamFlow EPMS** is a final-year software engineering capstone project designed to solve the fragmentation of engineering tools. Instead of hopping between Jira for tasks, Confluence for docs, and external tools for reporting, TeamFlow unifies the entire engineering lifecycle into a single platform.

### ✨ Key Features
- **Agile Project Management**: Create, assign, and track engineering tasks across sprints and boards.
- **Enterprise RBAC**: Highly granular custom Role-Based Access Control system out-of-the-box.
- **Automated Engineering Reports**: Generate release notes, sprint retrospectives, and architectural decision records automatically.
- **Real-Time Collaboration**: Keep your team aligned with live updates and unified workspaces.
- **Premium User Experience**: Fast, reactive, and beautifully designed frontend using Next.js 16 and shadcn/ui.

---

## 🏗️ Architecture & Tech Stack

TeamFlow uses a decoupled, API-first architecture designed for enterprise scalability.

### **Frontend**
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui (New York style)
- **State & Data Fetching**: TanStack React Query + Axios
- **Animations**: Framer Motion

### **Backend**
- **Framework**: Django 5.2 + Django Ninja (Fast API routing)
- **Language**: Python 3.14
- **Database**: PostgreSQL 16
- **Caching & Queues**: Redis 7 + Celery (Phase 2)
- **Authentication**: Custom JWT Authentication with robust RBAC

### **Infrastructure**
- **Containerization**: Docker & Docker Compose
- **Package Managers**: `pnpm` (Frontend), `pip` (Backend)
- **Linting & Formatting**: Pre-commit, Ruff, Black, ESLint, Prettier

---

## 🚦 Getting Started (Local Development)

### Prerequisites
Make sure you have the following installed:
- [Docker](https://www.docker.com/) & Docker Compose
- [Node.js](https://nodejs.org/) (v22+)
- [pnpm](https://pnpm.io/)
- Python (3.14+)

### 1. Clone & Environment Setup
```bash
git clone https://github.com/richujoseph/TeamFlow.git
cd TeamFlow

# Set up the backend environment
cp .env.example .env
```

### 2. Start the Backend Infrastructure
We use Docker to spin up the PostgreSQL database, Redis, and the Django API server.

```bash
# Start all containers in detached mode
docker compose up -d

# Verify containers are running healthily
docker compose ps
```
> **Note:** The entrypoint script will automatically wait for the database and apply Django migrations.

### 3. Start the Frontend
For the best Developer Experience (HMR), the frontend is run natively outside of Docker during development.

```bash
cd frontend
pnpm install
pnpm dev
```

### 4. Access the Application
- **Frontend App**: [http://localhost:3000](http://localhost:3000)
- **Backend API Docs (Swagger)**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- **Django Admin**: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 🛡️ Role-Based Access Control (RBAC)

TeamFlow implements a fully custom RBAC system independent of Django's default permissions.

You can seed the database with the default system roles by running:
```bash
docker compose exec backend python manage.py seed_roles
```
*This command is idempotent and will safely provision the 8 core roles (Administrator, Project Manager, Team Lead, Developer, QA Engineer, etc.) along with their granular permissions.*

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](./docs/CONTRIBUTING.md) for details on our branching strategy, commit standards (Conventional Commits), and code quality requirements.

Please read the [Architecture Document](./docs/ARCHITECTURE.md) to understand the design philosophies before submitting PRs.

---

<div align="center">
  <i>Built with passion by software engineers, for software engineers.</i>
</div>
