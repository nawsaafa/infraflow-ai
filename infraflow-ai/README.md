# InfraFlow AI - Frontend

The intelligent platform connecting climate finance with bankable infrastructure projects.

## Overview

InfraFlow AI is a comprehensive Next.js 14 application for managing infrastructure finance projects, document processing, compliance monitoring, and portfolio analytics.

## Features

- **Landing Page**: Marketing site with product information and CTAs
- **Dashboard**: Comprehensive portfolio overview
- **Projects**: Project management and detail views
- **Documents**: AI-powered document processing center
- **Analytics**: Portfolio analytics and insights
- **Compliance**: Regulatory compliance monitoring
- **Financial Models**: DCF models and scenario analysis
- **Reports**: Generated investment memos and compliance reports

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn/ui
- **Charts**: Tremor.so (configured for React 19)
- **Icons**: Lucide React
- **Authentication**: Clerk (optional)

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Copy environment variables:
```bash
cp .env.local.example .env.local
```

3. Update `.env.local` with your backend API URL and other configuration:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

### Build

Create a production build:

```bash
npm run build
```

### Start Production Server

```bash
npm start
```

## Project Structure

```
src/
├── app/
│   ├── (marketing)/        # Marketing pages (landing)
│   │   └── page.tsx
│   ├── dashboard/           # Dashboard pages
│   │   ├── page.tsx         # Portfolio overview
│   │   ├── projects/        # Project management
│   │   ├── documents/       # Document processing
│   │   ├── analytics/       # Portfolio analytics
│   │   ├── compliance/      # Compliance monitoring
│   │   ├── models/          # Financial models
│   │   ├── reports/         # Generated reports
│   │   └── settings/        # Settings
│   ├── layout.tsx
│   └── globals.css
├── components/
│   ├── ui/                  # Shadcn/ui components
│   ├── layout/              # Layout components (Sidebar)
│   └── dashboard/           # Dashboard-specific components
├── lib/
│   ├── utils.ts            # Utility functions
│   └── api.ts              # API client
└── types/
    └── index.ts            # TypeScript types
```

## Key Routes

- `/` - Landing page
- `/dashboard` - Portfolio overview
- `/dashboard/projects` - Project list
- `/dashboard/projects/[id]` - Project detail
- `/dashboard/documents` - Document processing
- `/dashboard/analytics` - Analytics dashboard
- `/dashboard/compliance` - Compliance monitoring
- `/dashboard/models` - Financial models
- `/dashboard/reports` - Generated reports
- `/dashboard/settings` - Settings

## API Integration

The frontend communicates with the backend API through the API client located at `src/lib/api.ts`.

### Available API Methods

- `projectApi.getAll()` - Get all projects
- `projectApi.getById(id)` - Get project by ID
- `projectApi.create(data)` - Create new project
- `documentApi.upload(projectId, files)` - Upload documents
- `analyticsApi.getPortfolio()` - Get portfolio analytics
- `complianceApi.check(projectId)` - Run compliance check

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Connect repository to Vercel
3. Configure environment variables
4. Deploy

### Docker

Build and run with Docker:

```bash
docker build -t infraflow-ai .
docker run -p 3000:3000 infraflow-ai
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Clerk public key | No |
| `CLERK_SECRET_KEY` | Clerk secret key | No |

## Development Guidelines

- Use TypeScript strict mode
- Follow Next.js App Router conventions
- Use Shadcn/ui components for UI consistency
- Keep API calls in the API client
- Use proper TypeScript types from `src/types`

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## Backend Integration

This frontend is designed to work with the InfraFlow AI FastAPI backend. Ensure the backend is running and the `NEXT_PUBLIC_API_URL` is correctly configured.

## License

Proprietary - All rights reserved

## Support

For issues and questions, contact the development team.
