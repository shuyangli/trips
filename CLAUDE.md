# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a full-stack trips management application with Google OAuth authentication via Firebase.

**Backend**: FastAPI + PostgreSQL + SQLAlchemy Core + Firebase Admin SDK
**Frontend**: React 19 + TypeScript + Vite + Ant Design + Firebase SDK

### Key Architectural Patterns

- **Authentication Flow**: Firebase handles OAuth → JWT tokens → Backend validates with Firebase Admin SDK
- **Database**: SQLAlchemy Core (not ORM) with timezone-aware timestamps and UUID primary keys
- **API**: RESTful endpoints under `/api/v1` with Bearer token authentication
- **State Management**: React Context for auth, custom hooks for Firebase integration

## Essential Commands

### Backend Development
```bash
# Start development environment (preferred)
cd backend/
docker compose up --build

# Database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1

# Run without Docker
uvicorn src.server:app --reload
```

### Frontend Development
```bash
cd frontend/
npm run dev          # Development server
npm run build        # Production build with TypeScript check
npm run lint         # ESLint validation
npm run preview      # Preview production build
```

## Database Schema

Core tables: `users`, `trips`, `trip_participants`, `trip_segments`, `itinerary_items`, `itinerary_participants`

**Important**: All datetime columns are timezone-aware (`TIMESTAMP(timezone=True)`). Use `gen_random_uuid()` for UUID primary keys.

## Environment Setup

**Backend** requires `DATABASE_URL` and `GOOGLE_APPLICATION_CREDENTIALS`
**Frontend** requires Firebase config variables (see `.env.example`)

Copy `.env.example` files and configure Firebase credentials before development.

## Code Conventions

### Backend
- Use SQLAlchemy Core, not ORM
- Pydantic schemas for validation
- Repository pattern in `/src/database/crud/`
- All API endpoints require Firebase token validation

### Frontend
- TypeScript strict mode enabled
- Ant Design components with form validation
- Custom hooks pattern for Firebase operations
- Axios instance with automatic token injection

## Authentication Integration

Users authenticate via Google OAuth through Firebase. Backend validates tokens using Firebase Admin SDK. First-time users are automatically created in the database during signin.

## Testing & Quality

Run `npm run lint` for frontend code quality. No testing framework currently configured - set up testing as needed for new features.