# Next.js Skills and Knowledge

## Overview
Next.js is a React-based full-stack web development framework that enables functionality such as hybrid static & server rendering, TypeScript support, smart bundling, route pre-fetching, and more. It's designed to make it easy to create user interfaces and handle common web development patterns.

## Key Features
- **File-based Routing System**: Pages in the `pages/` directory become routes automatically
- **API Routes**: Create API endpoints in the `pages/api/` directory
- **Server-Side Rendering (SSR)**: Render pages on the server for better SEO and performance
- **Static Site Generation (SSG)**: Pre-render pages at build time
- **Incremental Static Regeneration (ISR)**: Update static pages after build time
- **Client-Side Rendering**: Use React for dynamic client-side interactions
- **Automatic Code Splitting**: Optimize loading of code chunks
- **Built-in CSS Support**: Including CSS Modules and styled-jsx
- **Optimization**: Automatic image optimization, font optimization, etc.

## Common Commands
- `npx create-next-app@latest` - Create a new Next.js app
- `npm run dev` - Start development server
- `npm run build` - Build the application for production
- `npm start` - Start the production server

## File Structure
```
my-app/
├── node_modules/
├── pages/
│   ├── api/
│   ├── _app.js
│   └── index.js
├── public/
├── styles/
├── package.json
└── README.md
```

## Best Practices
- Use the `pages/` directory for routing
- Leverage `getStaticProps` and `getServerSideProps` for data fetching
- Use `next/link` for client-side navigation
- Optimize images with the `next/image` component
- Use `next/head` to manage head elements
- Implement proper error handling with custom error pages

## App Router vs Pages Router
- **Pages Router**: Traditional Next.js routing using the `pages/` directory
- **App Router**: Newer routing system using the `app/` directory with React Server Components

## React Server Components
- Components that render on the server by default
- Can directly access backend resources
- Reduce JavaScript bundle size
- Support streaming and progressive rendering

## Environment Variables
- Use `.env.local` for sensitive variables
- Use `NEXT_PUBLIC_` prefix for client-side accessible variables

## Deployment
- Deploy to Vercel for optimal Next.js experience
- Can be deployed to other platforms like Netlify, AWS, etc.

# Task CRUD Skills

Core skills for basic task operations

1. create_task
   POST /api/tasks
   Body: { title, description? }
   → New task for current user

2. list_tasks
   GET /api/tasks?status=all|pending|completed&sort=created|title|due_date
   → User's tasks only

3. get_task
   GET /api/tasks/{id}
   → Single task (if owned)

4. update_task
   PUT /api/tasks/{id}
   Body: { title?, description?, completed? }
   → Partial update

5. delete_task
   DELETE /api/tasks/{id}
   → Remove if owned

6. toggle_complete
   PATCH /api/tasks/{id}/complete
   → Flip completed status

# Task Summary Skill

Quick overview of user's tasks

GET /api/tasks/summary

Response example:
{
  "total": 14,
  "pending": 9,
  "completed": 5,
  "overdue": 2,
  "message": "9 tasks pending, 2 overdue"
}

# Auth Status Skill

Quick check current user & session

GET /api/auth/me

Response:
{
  "user_id": "user_abc123",
  "email": "user@example.com",
  "is_authenticated": true
}

# Task Search Skill

Search in title + description

GET /api/tasks/search?q=meeting

Returns matching tasks for current user only

# AI Priority Suggestion Skill (Qwen)

Suggests priority using Qwen

POST /api/tasks/suggest-priority

Body:
{ "title": "...", "description": "..." }

Response:
{
  "priority": "high",
  "reason": "Urgent client deliverable"
}