<!--
Sync Impact Report:
- Version change: 1.0.0 → 2.0.0
- Modified principles: All principles updated for Phase III
- Added sections: AI Integration, Cohere API usage
- Removed sections: Phase II specific constraints
- Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending
  - .specify/templates/spec-template.md ⚠ pending
  - .specify/templates/tasks-template.md ⚠ pending
  - .specify/templates/commands/*.md ⚠ pending
- Follow-up TODOs: Update templates to reflect Phase III changes
-->

# Todo Constitution

## Core Principles

### I. Code Quality & AI Integration
Every code contribution must follow established standards: Python (backend) requires PEP 8 compliance with type hints and clean functions; TypeScript (frontend) requires strict typing with no 'any' types; All functions must have single responsibility with meaningful names and proper error handling; AI integration must use Cohere API exclusively with proper SDK implementation.

### II. User Experience
The application must provide a responsive, mobile-first UI using Tailwind CSS; The dashboard must be intuitive with a clear task list, add button, and auth flow; All user interactions must provide clear feedback including loading states and toast notifications for success/error messages; Natural language interactions through the chatbot must feel conversational and helpful.

### III. Test-First (NON-NEGOTIABLE)
TDD is mandatory: Tests written → User approved → Tests fail → Then implement; The Red-Green-Refactor cycle must be strictly enforced; All features must have corresponding tests before being considered complete.

### IV. Security-First
All API endpoints must be JWT-protected; User isolation must be enforced at the database level; Authentication must use Better Auth on frontend with JWT verification on backend using a shared secret; All sensitive data must be properly encrypted; Chat endpoint must verify JWT and enforce user isolation for conversations.

### V. Persistence & Reliability
All data must persist in Neon PostgreSQL database; The application must maintain data integrity across restarts; Database operations must be atomic and consistent; Error handling must prevent data loss; Conversation and message state must persist in DB between requests (stateless architecture).

### VI. Multi-User Isolation
Each user must only see and modify their own tasks; User data must be properly isolated at the application and database level; Authentication and authorization must be verified for every request; User session management must be secure and reliable; Conversations must be isolated by user_id.

### VII. AI Integration & Tool Calling
Cohere API must be used exclusively for natural language understanding and tool calling; All task operations must be accessible through AI-powered tool calls; The system must handle natural language inputs and convert them to appropriate backend operations; Error handling must be graceful when tasks don't exist or inputs are invalid.

## Technical Constraints

Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
Backend: FastAPI, SQLModel ORM, Neon PostgreSQL
Auth: Better Auth (frontend) + JWT verification (backend, shared secret)
AI: Cohere API only (no OpenAI), official SDK with COHERE_API_KEY
API: RESTful, /api/tasks/* endpoints (existing), new /api/chat endpoint for AI
Database: tasks table (existing), plus conversation and message tables for chat state
Env Variables: COHERE_API_KEY, BETTER_AUTH_SECRET, DATABASE_URL
Chat Architecture: Stateless (no server-side memory), conversation state in DB

## Development Workflow

- Use Spec-Kit Plus workflow: Constitution → Specify → Plan → Tasks → Qwen code generation
- Qwen as ONLY model for code/spec generation (no Claude)
- Reference specs with @specs/... syntax
- Human must review & approve every generated code block
- Preserve full spec history
- Commit often with semantic messages
- No manual coding allowed for hackathon evaluation
- Adapt any OpenAI-style code to Cohere API implementation

## Success Definition (Phase III Exit Criteria)

☑ Chatbot handles all 5 task operations + user info via natural language
☑ Cohere API fully integrated (COHERE_API_KEY used correctly)
☑ Stateless: Conversations & state persist in Neon DB after restart
☑ Full security: JWT verification, user isolation
☑ Frontend chat UI works seamlessly with backend endpoint
☑ No crashes: Invalid inputs, missing tasks, wrong IDs handled gracefully
☑ README: Setup instructions, env vars, chat examples, Cohere key note

## Explicit Non-Goals for Phase III Basic

× Real-time streaming (simple POST response)
× Advanced Cohere features (fine-tuning, RAG)
× Complex multi-turn chaining beyond basics
× External chatbot UI libraries (build simple in Next.js)
× Tests/CI (optional)

## Governance

This constitution is the supreme guiding document for Phase III of Todo - AI Chatbot Integration.
Any deviation must be:
- Explicitly justified
- Documented in specs/history
- Approved by project owner

All PRs/reviews must verify compliance with these principles.
Complexity must be justified with clear benefits.

Use Cohere API exclusively (with provided key).  
Reuse Phase II infrastructure fully.

**Version**: 2.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-09