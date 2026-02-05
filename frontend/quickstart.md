# Quickstart Guide: Frontend UI

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Access to the backend API (with JWT authentication)

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Environment Configuration
Create a `.env.local` file in the root of the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_JWT_SECRET=your_jwt_secret_here
```

### 4. Run Development Server
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## Key Features and Navigation

### Authentication
- Visit `/signin` to log in to an existing account
- Visit `/signup` to create a new account
- Authentication state is managed using Better Auth

### Dashboard
- After authentication, users are redirected to `/dashboard` or `/`
- The dashboard displays all user tasks in a responsive grid of glassmorphism cards
- Use the floating "Add Task" button to create new tasks

### Task Management
- Create tasks using the modal form
- Edit tasks by clicking the edit icon on task cards
- Delete tasks using the delete icon on task cards
- Toggle task completion with the checkbox

## Project Structure
```
frontend/
├── app/                 # Next.js App Router pages
│   ├── layout.tsx       # Root layout with Navbar
│   ├── page.tsx         # Home page
│   ├── signin/page.tsx  # Signin page
│   ├── signup/page.tsx  # Signup page
│   └── dashboard/
│       └── page.tsx     # Dashboard page
├── components/          # Reusable UI components
│   ├── Navbar.tsx       # Navigation bar
│   ├── TaskCard.tsx     # Task display component
│   ├── GlassCard.tsx    # Glassmorphism card component
│   └── TaskForm.tsx     # Task creation/editing form
├── lib/                 # Utility functions
│   └── api.ts           # API client with JWT handling
├── styles/              # Custom styles
│   └── globals.css      # Global styles and custom utilities
└── public/              # Static assets
```

## Key Technologies
- Next.js 16+ with App Router
- TypeScript with strict typing
- Tailwind CSS with custom glassmorphism utilities
- Framer Motion for animations
- Better Auth for authentication
- React Hot Toast for notifications

## API Integration
The frontend communicates with the backend API through the client in `lib/api.ts`, which handles JWT authentication automatically. All API calls include the authentication token in the request headers.

## Custom UI Elements
- Glassmorphism cards with backdrop blur effects
- Neon glow on hover and focus states
- Smooth animations using Framer Motion
- Responsive design for all screen sizes
- Dark theme with indigo, cyan, and purple accents