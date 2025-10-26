# 🚀 React Migration Plan - Vani Dashboard

## Tech Stack Overview

| Type   | Winner                      | Why                             |
| ------ | --------------------------- | ------------------------------- |
| Graphs | **Plotly**                  | Interactive, ML-friendly, quick |
| Maps   | **Leaflet (React-Leaflet)** | GeoJSON + farm polygons         |

### Additional Libraries
- **Framer Motion**: Smooth animations for UI transitions
- **Lenis**: Buttery-smooth scrolling experience
- **shadcn/ui**: Hero UI components (built on Radix UI + Tailwind CSS)

## 📦 Step 1: Create React + Vite Project

```powershell
# From workspace root
cd c:\workspace\yes-scan-apex\yes_scan_prototype

# Create new React + TypeScript + Vite project
npm create vite@latest vani-frontend -- --template react-ts

cd vani-frontend
```

## 📚 Step 2: Install Dependencies

```powershell
# Core dependencies
npm install react-router-dom @clerk/clerk-react

# UI Framework - shadcn/ui setup
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# shadcn/ui dependencies
npm install tailwindcss-animate class-variance-authority clsx tailwind-merge
npm install @radix-ui/react-slot @radix-ui/react-toast @radix-ui/react-dialog
npm install @radix-ui/react-dropdown-menu @radix-ui/react-tabs
npm install lucide-react

# Graphs - Plotly
npm install plotly.js-dist-min
npm install react-plotly.js
npm install @types/plotly.js --save-dev

# Maps - React-Leaflet
npm install leaflet react-leaflet
npm install @types/leaflet --save-dev

# Animations - Framer Motion
npm install framer-motion

# Smooth Scrolling - Lenis
npm install lenis

# Date handling & utilities
npm install date-fns
```

## 🎨 Step 3: Configure Tailwind CSS

**File: `tailwind.config.js`**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "#10b981",
          foreground: "#ffffff",
        },
        secondary: {
          DEFAULT: "#14b8a6",
          foreground: "#ffffff",
        },
        destructive: {
          DEFAULT: "#ef4444",
          foreground: "#ffffff",
        },
        muted: {
          DEFAULT: "#f8fafc",
          foreground: "#64748b",
        },
        accent: {
          DEFAULT: "#f1f5f9",
          foreground: "#1e293b",
        },
        card: {
          DEFAULT: "#ffffff",
          foreground: "#1e293b",
        },
      },
      borderRadius: {
        lg: "0.75rem",
        md: "0.5rem",
        sm: "0.25rem",
      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

## 🎯 Step 4: Project Structure

```
vani-frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── table.tsx
│   │   │   ├── tabs.tsx
│   │   │   └── toast.tsx
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Topbar.tsx
│   │   │   └── DashboardLayout.tsx
│   │   ├── charts/
│   │   │   ├── FloodTrendChart.tsx    # Plotly line chart
│   │   │   └── ClaimStatsChart.tsx    # Plotly bar chart
│   │   ├── maps/
│   │   │   ├── FarmMap.tsx            # React-Leaflet map
│   │   │   └── MapControls.tsx        # Layer toggles
│   │   └── weather/
│   │       ├── CurrentWeather.tsx
│   │       ├── ForecastCards.tsx
│   │       └── WeatherAlerts.tsx
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Farms.tsx
│   │   ├── Claims.tsx
│   │   ├── Weather.tsx
│   │   └── Admin.tsx
│   ├── lib/
│   │   ├── utils.ts          # cn() helper
│   │   └── api.ts            # Backend API calls
│   ├── hooks/
│   │   ├── useSmoothScroll.ts  # Lenis integration
│   │   └── useWeather.ts       # Weather data hook
│   ├── App.tsx
│   └── main.tsx
├── public/
│   └── vani-logo.svg
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── vite.config.ts
```

## 🔧 Step 5: Key Files Setup

### `src/main.tsx` - App Entry with Clerk & Lenis

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { ClerkProvider } from '@clerk/clerk-react'
import App from './App.tsx'
import './index.css'

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

if (!PUBLISHABLE_KEY) {
  throw new Error("Missing Publishable Key")
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
      <App />
    </ClerkProvider>
  </React.StrictMode>,
)
```

### `src/App.tsx` - Router & Lenis Setup

```typescript
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { SignIn, SignedIn, SignedOut } from '@clerk/clerk-react'
import { useEffect } from 'react'
import Lenis from 'lenis'
import DashboardLayout from './components/layout/DashboardLayout'
import Dashboard from './pages/Dashboard'
import Farms from './pages/Farms'
import Claims from './pages/Claims'
import Weather from './pages/Weather'
import Admin from './pages/Admin'

function App() {
  // Initialize Lenis smooth scroll
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      smoothWheel: true,
    })

    function raf(time: number) {
      lenis.raf(time)
      requestAnimationFrame(raf)
    }

    requestAnimationFrame(raf)

    return () => {
      lenis.destroy()
    }
  }, [])

  return (
    <BrowserRouter>
      <Routes>
        {/* Public Route - Sign In */}
        <Route
          path="/sign-in/*"
          element={
            <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-600 via-purple-800 to-emerald-500">
              <SignIn routing="path" path="/sign-in" />
            </div>
          }
        />

        {/* Protected Routes */}
        <Route
          path="/*"
          element={
            <>
              <SignedOut>
                <Navigate to="/sign-in" replace />
              </SignedOut>
              <SignedIn>
                <DashboardLayout>
                  <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/farms" element={<Farms />} />
                    <Route path="/claims" element={<Claims />} />
                    <Route path="/weather" element={<Weather />} />
                    <Route path="/admin" element={<Admin />} />
                  </Routes>
                </DashboardLayout>
              </SignedIn>
            </>
          }
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App
```

### `src/hooks/useSmoothScroll.ts`

```typescript
import { useEffect } from 'react'
import Lenis from 'lenis'

export function useSmoothScroll() {
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      smoothWheel: true,
      smoothTouch: false,
    })

    function raf(time: number) {
      lenis.raf(time)
      requestAnimationFrame(raf)
    }

    requestAnimationFrame(raf)

    return () => {
      lenis.destroy()
    }
  }, [])
}
```

## 📊 Step 6: Plotly Chart Component

### `src/components/charts/FloodTrendChart.tsx`

```typescript
import Plot from 'react-plotly.js'
import { motion } from 'framer-motion'

export default function FloodTrendChart() {
  const data = [
    {
      x: ['Oct 15', 'Oct 17', 'Oct 19', 'Oct 21', 'Oct 23', 'Oct 25'],
      y: [12.3, 18.5, 23.4, 21.8, 25.6, 23.4],
      type: 'scatter' as const,
      mode: 'lines+markers' as const,
      name: 'Flood Affected %',
      line: { color: '#10b981', width: 3 },
      marker: { size: 8, color: '#059669' },
    },
  ]

  const layout = {
    title: 'Flood Detection Trend (Last 7 Days)',
    xaxis: { title: 'Date' },
    yaxis: { title: 'Affected Area (%)' },
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { family: 'system-ui, sans-serif' },
    margin: { t: 50, r: 20, b: 50, l: 60 },
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-white rounded-xl p-6 shadow-sm"
    >
      <Plot
        data={data}
        layout={layout}
        config={{ responsive: true, displayModeBar: false }}
        style={{ width: '100%', height: '400px' }}
      />
    </motion.div>
  )
}
```

## 🗺️ Step 7: React-Leaflet Map Component

### `src/components/maps/FarmMap.tsx`

```typescript
import { MapContainer, TileLayer, GeoJSON, Marker, Popup } from 'react-leaflet'
import { motion } from 'framer-motion'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Fix default marker icon
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png',
})

interface FarmMapProps {
  geoJsonData?: any
  center?: [number, number]
  zoom?: number
}

export default function FarmMap({ 
  geoJsonData, 
  center = [20.2961, 85.8245], 
  zoom = 13 
}: FarmMapProps) {
  
  const onEachFeature = (feature: any, layer: any) => {
    if (feature.properties) {
      const { farm_id, area_ha, flood_percent, status } = feature.properties
      layer.bindPopup(`
        <div class="p-2">
          <h3 class="font-bold text-emerald-600">${farm_id}</h3>
          <p class="text-sm">Area: ${area_ha} ha</p>
          <p class="text-sm">Flood: ${flood_percent}%</p>
          <p class="text-sm">Status: <span class="font-semibold">${status}</span></p>
        </div>
      `)
    }
  }

  const style = (feature: any) => {
    const floodPercent = feature.properties.flood_percent || 0
    return {
      fillColor: floodPercent > 30 ? '#ef4444' : '#10b981',
      weight: 2,
      opacity: 1,
      color: 'white',
      fillOpacity: 0.6,
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="rounded-xl overflow-hidden shadow-lg"
    >
      <MapContainer
        center={center}
        zoom={zoom}
        style={{ height: '600px', width: '100%' }}
        className="z-0"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {geoJsonData && (
          <GeoJSON
            data={geoJsonData}
            style={style}
            onEachFeature={onEachFeature}
          />
        )}
      </MapContainer>
    </motion.div>
  )
}
```

## 🎭 Step 8: Framer Motion Animations

### `src/components/layout/DashboardLayout.tsx`

```typescript
import { ReactNode } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useLocation } from 'react-router-dom'
import Sidebar from './Sidebar'
import Topbar from './Topbar'

interface DashboardLayoutProps {
  children: ReactNode
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const location = useLocation()

  return (
    <div className="flex h-screen bg-slate-50">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Topbar />
        
        <main className="flex-1 overflow-y-auto">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
              className="p-6"
            >
              {children}
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  )
}
```

### Page Transition Wrapper

```typescript
import { motion } from 'framer-motion'
import { ReactNode } from 'react'

export function PageTransition({ children }: { children: ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.4, ease: "easeInOut" }}
    >
      {children}
    </motion.div>
  )
}
```

## 🎨 Step 9: shadcn/ui Components

Initialize shadcn/ui components:

```powershell
# Add components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add table
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add dropdown-menu
```

## 🔌 Step 10: API Integration

### `src/lib/api.ts`

```typescript
const API_BASE = 'http://127.0.0.1:8000'

export const api = {
  farms: {
    getAll: async () => {
      const res = await fetch(`${API_BASE}/api/farms`)
      return res.json()
    },
  },
  
  weather: {
    getCurrent: async () => {
      const res = await fetch(`${API_BASE}/api/weather/current`)
      return res.json()
    },
    getForecast: async () => {
      const res = await fetch(`${API_BASE}/api/weather/forecast`)
      return res.json()
    },
    getAlerts: async () => {
      const res = await fetch(`${API_BASE}/api/weather/alerts`)
      return res.json()
    },
  },
  
  claims: {
    getAll: async () => {
      const res = await fetch(`${API_BASE}/api/claims`)
      return res.json()
    },
    downloadPDF: async (claimId: string) => {
      const res = await fetch(`${API_BASE}/api/claim/${claimId}/pdf`)
      const data = await res.json()
      
      // Decode base64 and create download
      const byteCharacters = atob(data.pdf_base64)
      const byteNumbers = new Array(byteCharacters.length)
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i)
      }
      const byteArray = new Uint8Array(byteNumbers)
      const blob = new Blob([byteArray], { type: 'application/pdf' })
      
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `claim_${claimId}.pdf`
      a.click()
      window.URL.revokeObjectURL(url)
    },
  },
  
  triage: {
    run: async (threshold: number = 30.0) => {
      const res = await fetch(`${API_BASE}/api/triage?threshold=${threshold}`, {
        method: 'POST',
      })
      return res.json()
    },
  },
}
```

## 🚀 Step 11: Run Development Server

```powershell
cd vani-frontend

# Start dev server
npm run dev

# Open browser to http://localhost:5173
```

## 📋 Environment Variables

Create `.env` in `vani-frontend/`:

```env
VITE_CLERK_PUBLISHABLE_KEY=pk_test_bWVycnktbW9sbHVzay03NS5jbGVyay5hY2NvdW50cy5kZXYk
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## 🎯 Benefits Summary

### Plotly.js
- ✅ **Interactive charts**: Zoom, pan, hover tooltips
- ✅ **ML-friendly**: Perfect for displaying model metrics
- ✅ **Fast rendering**: Hardware-accelerated WebGL
- ✅ **Export ready**: Save charts as PNG/SVG

### React-Leaflet
- ✅ **GeoJSON native**: Perfect for farm polygons
- ✅ **Lightweight**: Better performance than Google Maps
- ✅ **Open-source**: No API keys needed for base maps
- ✅ **Customizable**: Easy to style flood detection layers

### Framer Motion
- ✅ **Smooth animations**: 60fps page transitions
- ✅ **Easy syntax**: Simple `motion.*` components
- ✅ **Spring physics**: Natural movement feel
- ✅ **Gesture support**: Drag, hover, tap animations

### Lenis
- ✅ **Buttery smooth**: Native-like scrolling
- ✅ **Lightweight**: Only 2KB gzipped
- ✅ **Performance**: RequestAnimationFrame based
- ✅ **Customizable**: Adjust easing and duration

### shadcn/ui
- ✅ **Copy-paste components**: Not a package, you own the code
- ✅ **Accessible**: Built on Radix UI primitives
- ✅ **Tailwind**: Fully customizable styling
- ✅ **Modern**: Beautiful hero-style designs

## 🔄 Migration Checklist

- [ ] Create React + Vite project
- [ ] Install all dependencies
- [ ] Configure Tailwind CSS
- [ ] Set up Clerk authentication
- [ ] Initialize shadcn/ui components
- [ ] Create layout components (Sidebar, Topbar)
- [ ] Build Plotly chart components
- [ ] Build React-Leaflet map components
- [ ] Implement Framer Motion page transitions
- [ ] Set up Lenis smooth scrolling
- [ ] Connect to FastAPI backend
- [ ] Test Clerk sign-in flow
- [ ] Test map GeoJSON rendering
- [ ] Test weather API integration
- [ ] Deploy to production

---

**Next Step**: Run the commands in Step 1 to create your React project!
