# =============================================================================
# TeamFlow EPMS — Frontend Dockerfile
# =============================================================================
# Multi-stage build for the Next.js 16 frontend.
# Used for production builds. In Phase 1 dev, frontend runs natively via pnpm.
#
# Stage 1 (deps):    Install pnpm + dependencies
# Stage 2 (builder): Build the Next.js application
# Stage 3 (runner):  Production-optimized runtime
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Install dependencies
# ---------------------------------------------------------------------------
FROM node:22-alpine AS deps

RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Copy package files for dependency installation
COPY package.json pnpm-lock.yaml* ./

RUN pnpm install --frozen-lockfile

# ---------------------------------------------------------------------------
# Stage 2: Build the Next.js application
# ---------------------------------------------------------------------------
FROM node:22-alpine AS builder

RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build with standalone output for minimal Docker image
ENV NEXT_TELEMETRY_DISABLED=1
RUN pnpm build

# ---------------------------------------------------------------------------
# Stage 3: Production runtime
# ---------------------------------------------------------------------------
FROM node:22-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1

# Create non-root user
RUN addgroup --system --gid 1001 teamflow && \
    adduser --system --uid 1001 teamflow

# Copy built application from builder stage
COPY --from=builder /app/public ./public
COPY --from=builder --chown=teamflow:teamflow /app/.next/standalone ./
COPY --from=builder --chown=teamflow:teamflow /app/.next/static ./.next/static

USER teamflow

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
