# Todo Frontend

A beautiful and modern todo application frontend built with Next.js, featuring glassmorphism design, neon glow effects, and smooth animations.

## Features

- 🎨 Stunning glassmorphism UI with neon glow effects
- 📱 Fully responsive design (mobile, tablet, desktop)
- 🔐 Secure authentication with Better Auth
- ⚡ Smooth animations with Framer Motion
- 🎯 Task management (create, read, update, delete)
- 🔄 Real-time task status updates
- 🎯 Intuitive user interface with delightful interactions

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS with custom glassmorphism utilities
- **Animations**: Framer Motion
- **UI Components**: Custom-built with Tailwind
- **State Management**: React Hooks
- **Notifications**: React Hot Toast

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
# Update the variables in .env.local as needed
```

4. Run the development server:
```bash
npm run dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).

## Environment Variables

- `NEXT_PUBLIC_API_URL`: The URL of the backend API (default: http://localhost:8000)

## Scripts

- `npm run dev`: Start the development server
- `npm run build`: Build the application for production
- `npm run start`: Start the production server
- `npm run lint`: Run the linter

## Project Structure

```
frontend/
├── app/                 # Next.js App Router pages
│   ├── layout.tsx       # Root layout with Navbar
│   ├── page.tsx         # Home page (redirects to dashboard if authenticated)
│   ├── signin/page.tsx  # Signin page
│   ├── signup/page.tsx  # Signup page
│   └── dashboard/
│       └── page.tsx     # Dashboard page with task grid
├── components/          # Reusable UI components
│   ├── Navbar.tsx       # Navigation bar with user avatar/logout
│   ├── TaskCard.tsx     # Glassmorphism task card with hover effects
│   ├── GlassCard.tsx    # Reusable glassmorphism card component
│   ├── TaskForm.tsx     # Form for adding/editing tasks
│   └── ProtectedRoute.tsx # Component for protecting routes
├── lib/                 # Utility functions
│   └── api.ts           # API client with JWT handling
├── hooks/               # Custom React hooks
│   └── useAuth.ts       # Authentication state management
├── styles/              # Custom styles and utilities
│   └── globals.css      # Global CSS and custom utilities
└── public/              # Static assets
```

## API Integration

The frontend communicates with the backend API through the client in `lib/api.ts`, which handles JWT authentication automatically. All API calls include the authentication token in the request headers.

## Custom UI Elements

- Glassmorphism cards with backdrop blur effects
- Neon glow on hover and focus states
- Smooth animations using Framer Motion
- Responsive design for all screen sizes
- Dark theme with indigo, cyan, and purple accents