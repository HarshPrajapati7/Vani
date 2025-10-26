# Vani - Clerk Authentication Setup Guide

## 🔐 Integrating Clerk with Vani

Vani is designed to use **Clerk** for secure, enterprise-grade authentication. Follow this guide to integrate Clerk into your deployment.

---

## 📋 Prerequisites

- Node.js 16+ and npm/yarn/pnpm
- Clerk account (free tier available)
- Vani project cloned locally

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Clerk Application

1. Go to https://clerk.com and sign up (free)
2. Create a new application
3. Choose your authentication methods:
   - ✅ Email & Password
   - ✅ Google OAuth
   - ✅ GitHub OAuth
   - ✅ Phone (SMS)

### Step 2: Get Your Publishable Key

1. Navigate to https://dashboard.clerk.com/last-active?path=api-keys
2. Select **React** from framework dropdown
3. Copy your **Publishable Key** (starts with `pk_test_...` or `pk_live_...`)

### Step 3: Add to Environment

Create or update `.env.local` in project root:

```bash
VITE_CLERK_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
```

⚠️ **IMPORTANT**: 
- Use `.env.local` for local development
- Use `VITE_` prefix (required for Vite)
- Never commit real keys to git

### Step 4: Install Clerk React SDK

```bash
npm install @clerk/clerk-react@latest
```

Or with yarn:
```bash
yarn add @clerk/clerk-react@latest
```

### Step 5: Wrap App with ClerkProvider

Create/update `main.tsx` or `main.jsx`:

```typescript
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { ClerkProvider } from "@clerk/clerk-react";

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

if (!PUBLISHABLE_KEY) {
  throw new Error("Missing Clerk Publishable Key");
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY} afterSignOutUrl="/">
      <App />
    </ClerkProvider>
  </StrictMode>
);
```

### Step 6: Use Clerk Components

Update your `App.tsx`:

```typescript
import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
} from "@clerk/clerk-react";
import Dashboard from "./Dashboard";

export default function App() {
  return (
    <>
      <header className="header">
        <div className="logo">🌊 Vani</div>
        <nav>
          <SignedOut>
            <SignInButton mode="modal">
              <button className="btn-primary">Sign In</button>
            </SignInButton>
            <SignUpButton mode="modal">
              <button className="btn-secondary">Sign Up</button>
            </SignUpButton>
          </SignedOut>
          <SignedIn>
            <UserButton afterSignOutUrl="/" />
          </SignedIn>
        </nav>
      </header>

      <main>
        <SignedOut>
          <div className="hero">
            <h1>Welcome to Vani</h1>
            <p>AI-Powered Flood Insurance Platform</p>
            <SignInButton mode="modal">
              <button className="btn-cta">Get Started</button>
            </SignInButton>
          </div>
        </SignedOut>
        
        <SignedIn>
          <Dashboard />
        </SignedIn>
      </main>
    </>
  );
}
```

---

## 🎨 Advanced Configuration

### Custom Sign-In Page

```typescript
import { SignIn } from "@clerk/clerk-react";

export default function SignInPage() {
  return (
    <div className="auth-container">
      <SignIn 
        path="/sign-in" 
        routing="path"
        signUpUrl="/sign-up"
        appearance={{
          elements: {
            rootBox: "vani-auth-root",
            card: "vani-auth-card"
          }
        }}
      />
    </div>
  );
}
```

### Get User Information

```typescript
import { useUser } from "@clerk/clerk-react";

function UserProfile() {
  const { user } = useUser();

  if (!user) return null;

  return (
    <div>
      <h2>Welcome, {user.firstName}!</h2>
      <p>Email: {user.primaryEmailAddress?.emailAddress}</p>
      <p>Role: {user.publicMetadata.role || 'farmer'}</p>
    </div>
  );
}
```

### Protect API Routes

```typescript
import { useAuth } from "@clerk/clerk-react";

function Dashboard() {
  const { getToken } = useAuth();

  const fetchData = async () => {
    const token = await getToken();
    
    const response = await fetch('http://localhost:8000/api/farms', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    return response.json();
  };

  // ...
}
```

---

## 🔧 Backend Integration

Update FastAPI backend to verify Clerk JWTs:

```python
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from clerk_sdk import Clerk

security = HTTPBearer()
clerk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        user = clerk.verify_token(token)
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/api/farms")
async def get_farms(user = Depends(verify_token)):
    # user is authenticated
    return farms_data
```

Install Clerk Python SDK:
```bash
pip install clerk-sdk-python
```

---

## 🌐 Environment Variables Reference

### Frontend (.env.local)
```bash
# Clerk Publishable Key (required)
VITE_CLERK_PUBLISHABLE_KEY=pk_test_...

# Weather API
VITE_WEATHER_API_KEY=your_openweather_key

# Backend API URL
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```bash
# Clerk Secret Key (for backend verification)
CLERK_SECRET_KEY=sk_test_...

# Weather API
WEATHER_API_KEY=your_openweather_key
WEATHER_API_URL=https://api.openweathermap.org/data/3.0

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/vani_db
```

---

## 🎭 User Roles & Permissions

### Add Custom Metadata in Clerk

1. Go to Clerk Dashboard → Users
2. Click on a user
3. Go to "Metadata" tab
4. Add public metadata:

```json
{
  "role": "officer",
  "organization": "Odisha Agriculture Dept",
  "permissions": ["view_claims", "approve_claims"]
}
```

### Use in Frontend

```typescript
import { useUser } from "@clerk/clerk-react";

function AdminPanel() {
  const { user } = useUser();
  const role = user?.publicMetadata?.role;

  if (role !== 'officer') {
    return <div>Access Denied</div>;
  }

  return <div>Admin Content</div>;
}
```

---

## 🚦 Authentication Flow

```
1. User visits Vani dashboard
   ↓
2. <SignedOut> renders → Shows sign-in button
   ↓
3. User clicks "Sign In"
   ↓
4. Clerk modal opens (or redirects to /sign-in)
   ↓
5. User enters credentials
   ↓
6. Clerk verifies → Issues JWT token
   ↓
7. <SignedIn> renders → Shows dashboard
   ↓
8. Frontend sends token with API requests
   ↓
9. Backend verifies token with Clerk
   ↓
10. User accesses protected resources
```

---

## 📱 Social Authentication

Enable in Clerk Dashboard:

1. Go to **User & Authentication** → **Social Connections**
2. Enable providers:
   - Google
   - GitHub  
   - Facebook
   - Apple
3. Configure OAuth credentials from provider
4. Save changes

Automatically works with:
```typescript
<SignInButton mode="modal" />
```

No additional code needed!

---

## 🧪 Testing Without Clerk

For development/demo without Clerk setup, Vani includes a fallback mode:

```typescript
// In main.tsx
const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

if (!PUBLISHABLE_KEY) {
  // Demo mode - skip Clerk
  console.warn("Running in demo mode without Clerk");
  
  createRoot(document.getElementById("root")!).render(
    <StrictMode>
      <App demoMode={true} />
    </StrictMode>
  );
} else {
  // Production mode with Clerk
  createRoot(document.getElementById("root")!).render(
    <StrictMode>
      <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
        <App />
      </ClerkProvider>
    </StrictMode>
  );
}
```

---

## 🐛 Troubleshooting

### Error: "Missing Clerk Publishable Key"
- ✅ Check `.env.local` exists in project root
- ✅ Verify key starts with `VITE_CLERK_PUBLISHABLE_KEY`
- ✅ Restart dev server after adding env vars

### Clerk modal not showing
- ✅ Ensure `@clerk/clerk-react` is latest version
- ✅ Check browser console for errors
- ✅ Verify ClerkProvider wraps entire app

### "Invalid token" on backend
- ✅ Add `CLERK_SECRET_KEY` to backend `.env`
- ✅ Install `clerk-sdk-python`
- ✅ Verify token is sent in Authorization header

### CORS errors
- ✅ Add Clerk domain to FastAPI CORS:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific clerk domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📚 Resources

- **Clerk Documentation**: https://clerk.com/docs
- **React Quickstart**: https://clerk.com/docs/quickstarts/react
- **Vite Integration**: https://clerk.com/docs/references/react/clerk-provider
- **FastAPI + Clerk**: https://clerk.com/docs/backend-requests/making/jwt-templates

---

## 🆘 Support

- **Clerk Discord**: https://clerk.com/discord
- **Vani Issues**: support@vani.ai
- **Community Forum**: https://github.com/vani-ai/community

---

**Happy Building with Vani! 🌊**
