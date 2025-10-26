# 🎨 Component Examples - Copy & Paste Ready

## 📊 Plotly Chart Examples

### 1. Flood Trend Line Chart

```typescript
// src/components/charts/FloodTrendChart.tsx
import Plot from 'react-plotly.js'
import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'

export default function FloodTrendChart() {
  const [data, setData] = useState<any[]>([])

  useEffect(() => {
    // Fetch from API
    fetch('http://127.0.0.1:8000/api/stats/flood-trend')
      .then(res => res.json())
      .then(result => {
        setData([{
          x: result.dates,
          y: result.percentages,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Flood Affected %',
          line: { color: '#10b981', width: 3, shape: 'spline' },
          marker: { size: 10, color: '#059669', symbol: 'circle' },
          fill: 'tozeroy',
          fillcolor: 'rgba(16, 185, 129, 0.1)',
        }])
      })
  }, [])

  const layout = {
    title: {
      text: 'Flood Detection Trend',
      font: { size: 18, weight: 600, family: 'system-ui' }
    },
    xaxis: { 
      title: 'Date',
      gridcolor: '#e2e8f0',
      showgrid: true,
    },
    yaxis: { 
      title: 'Affected Area (%)',
      gridcolor: '#e2e8f0',
      showgrid: true,
    },
    paper_bgcolor: 'white',
    plot_bgcolor: 'white',
    font: { family: 'system-ui, sans-serif', color: '#1e293b' },
    margin: { t: 60, r: 20, b: 60, l: 60 },
    hovermode: 'x unified',
  }

  const config = {
    responsive: true,
    displayModeBar: false,
    displaylogo: false,
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="bg-white rounded-xl p-6 shadow-sm border border-slate-200"
    >
      <Plot
        data={data}
        layout={layout}
        config={config}
        style={{ width: '100%', height: '400px' }}
      />
    </motion.div>
  )
}
```

### 2. Claims Status Bar Chart

```typescript
// src/components/charts/ClaimStatsChart.tsx
import Plot from 'react-plotly.js'
import { motion } from 'framer-motion'

interface ClaimStatsProps {
  approved?: number
  pending?: number
  rejected?: number
}

export default function ClaimStatsChart({ 
  approved = 45, 
  pending = 23, 
  rejected = 12 
}: ClaimStatsProps) {
  
  const data = [{
    x: ['Approved', 'Pending', 'Rejected'],
    y: [approved, pending, rejected],
    type: 'bar',
    marker: {
      color: ['#10b981', '#f59e0b', '#ef4444'],
      line: { width: 2, color: 'white' }
    },
    text: [approved, pending, rejected],
    textposition: 'outside',
    textfont: { size: 14, weight: 600 },
  }]

  const layout = {
    title: 'Claims Status Overview',
    yaxis: { title: 'Number of Claims', gridcolor: '#e2e8f0' },
    paper_bgcolor: 'white',
    plot_bgcolor: 'white',
    margin: { t: 60, r: 20, b: 60, l: 60 },
    font: { family: 'system-ui, sans-serif' },
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="bg-white rounded-xl p-6 shadow-sm border"
    >
      <Plot
        data={data}
        layout={layout}
        config={{ responsive: true, displayModeBar: false }}
        style={{ width: '100%', height: '350px' }}
      />
    </motion.div>
  )
}
```

### 3. Model IoU Gauge Chart

```typescript
// src/components/charts/ModelIoUGauge.tsx
import Plot from 'react-plotly.js'
import { motion } from 'framer-motion'

export default function ModelIoUGauge({ iou = 0.942 }: { iou?: number }) {
  const data = [{
    type: 'indicator',
    mode: 'gauge+number+delta',
    value: iou * 100,
    title: { text: 'Model IoU Score', font: { size: 16 } },
    delta: { reference: 90, increasing: { color: '#10b981' } },
    gauge: {
      axis: { range: [0, 100], tickwidth: 1 },
      bar: { color: '#10b981' },
      bgcolor: 'white',
      borderwidth: 2,
      bordercolor: '#e2e8f0',
      steps: [
        { range: [0, 50], color: '#fee2e2' },
        { range: [50, 75], color: '#fef3c7' },
        { range: [75, 90], color: '#d1fae5' },
        { range: [90, 100], color: '#a7f3d0' },
      ],
      threshold: {
        line: { color: '#059669', width: 4 },
        thickness: 0.75,
        value: 95,
      },
    },
  }]

  const layout = {
    width: 400,
    height: 300,
    margin: { t: 40, b: 20, l: 20, r: 20 },
    paper_bgcolor: 'white',
    font: { family: 'system-ui', color: '#1e293b' },
  }

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.2 }}
      className="bg-white rounded-xl p-4 shadow-sm border flex justify-center"
    >
      <Plot data={data} layout={layout} config={{ displayModeBar: false }} />
    </motion.div>
  )
}
```

## 🗺️ React-Leaflet Map Examples

### 1. Farm Map with GeoJSON

```typescript
// src/components/maps/FarmMap.tsx
import { MapContainer, TileLayer, GeoJSON, Popup } from 'react-leaflet'
import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Fix Leaflet default marker icon
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png',
})

export default function FarmMap() {
  const [geoJson, setGeoJson] = useState<any>(null)
  const [selectedLayers, setSelectedLayers] = useState({
    satellite: true,
    flood: false,
    boundaries: true,
  })

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/farms')
      .then(res => res.json())
      .then(data => setGeoJson(data))
  }, [])

  const getFeatureStyle = (feature: any) => {
    const floodPercent = feature.properties.flood_percent || 0
    
    if (!selectedLayers.flood) {
      return {
        fillColor: '#10b981',
        weight: 2,
        opacity: 1,
        color: 'white',
        fillOpacity: 0.5,
      }
    }

    // Color based on flood severity
    const color = floodPercent > 50 ? '#ef4444' :
                  floodPercent > 30 ? '#f59e0b' : '#10b981'

    return {
      fillColor: color,
      weight: 2,
      opacity: 1,
      color: 'white',
      fillOpacity: 0.7,
    }
  }

  const onEachFeature = (feature: any, layer: any) => {
    const props = feature.properties
    layer.bindPopup(`
      <div class="p-3 min-w-[200px]">
        <h3 class="text-lg font-bold text-emerald-600 mb-2">🌾 ${props.farm_id}</h3>
        <div class="space-y-1 text-sm">
          <p><span class="font-semibold">Area:</span> ${props.area_ha} hectares</p>
          <p><span class="font-semibold">Flood:</span> 
            <span class="font-bold ${props.flood_percent > 30 ? 'text-red-600' : 'text-green-600'}">
              ${props.flood_percent}%
            </span>
          </p>
          <p><span class="font-semibold">Status:</span> 
            <span class="px-2 py-1 rounded text-xs font-semibold 
              ${props.status === 'verified' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}">
              ${props.status}
            </span>
          </p>
        </div>
      </div>
    `)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="relative"
    >
      <div className="rounded-xl overflow-hidden shadow-lg border-2 border-slate-200">
        <MapContainer
          center={[20.2961, 85.8245]}
          zoom={13}
          style={{ height: '600px', width: '100%' }}
          className="z-0"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          {geoJson && selectedLayers.boundaries && (
            <GeoJSON
              data={geoJson}
              style={getFeatureStyle}
              onEachFeature={onEachFeature}
            />
          )}
        </MapContainer>
      </div>

      {/* Map Controls */}
      <MapControls 
        layers={selectedLayers} 
        onToggle={setSelectedLayers} 
      />
    </motion.div>
  )
}
```

### 2. Map Layer Controls

```typescript
// src/components/maps/MapControls.tsx
import { motion } from 'framer-motion'
import { Layers, Eye, EyeOff } from 'lucide-react'

interface MapControlsProps {
  layers: {
    satellite: boolean
    flood: boolean
    boundaries: boolean
  }
  onToggle: (layers: any) => void
}

export default function MapControls({ layers, onToggle }: MapControlsProps) {
  const toggleLayer = (key: keyof typeof layers) => {
    onToggle({ ...layers, [key]: !layers[key] })
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.3 }}
      className="absolute top-4 right-4 z-[1000] bg-white rounded-xl shadow-lg p-4 border"
    >
      <div className="flex items-center gap-2 mb-3 pb-3 border-b">
        <Layers size={18} className="text-emerald-600" />
        <h4 className="font-semibold text-sm">Map Layers</h4>
      </div>

      <div className="space-y-2">
        {Object.entries(layers).map(([key, value]) => (
          <motion.button
            key={key}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => toggleLayer(key as keyof typeof layers)}
            className={`w-full flex items-center justify-between gap-3 px-3 py-2 rounded-lg transition-colors ${
              value ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-50 text-slate-500'
            }`}
          >
            <span className="text-sm font-medium capitalize">{key}</span>
            {value ? <Eye size={16} /> : <EyeOff size={16} />}
          </motion.button>
        ))}
      </div>
    </motion.div>
  )
}
```

## ✨ Framer Motion Animation Examples

### 1. Staggered Card Grid

```typescript
// src/components/dashboard/StatsGrid.tsx
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown } from 'lucide-react'

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

const stats = [
  { label: 'Total Farms', value: '342', change: '+12%', up: true },
  { label: 'Active Claims', value: '47', change: '-5%', up: false },
  { label: 'Flood Area', value: '23.4%', change: '+8%', up: true },
  { label: 'Model IoU', value: '94.2%', change: 'Excellent', up: true },
]

export default function StatsGrid() {
  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
    >
      {stats.map((stat, i) => (
        <motion.div
          key={i}
          variants={item}
          whileHover={{ scale: 1.05, y: -5 }}
          transition={{ type: 'spring', stiffness: 300 }}
          className="bg-white rounded-xl p-6 shadow-sm border border-slate-200"
        >
          <p className="text-sm text-slate-600 mb-2">{stat.label}</p>
          <p className="text-3xl font-bold text-slate-900 mb-2">{stat.value}</p>
          <div className={`flex items-center gap-1 text-sm font-semibold ${
            stat.up ? 'text-emerald-600' : 'text-red-600'
          }`}>
            {stat.up ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
            {stat.change}
          </div>
        </motion.div>
      ))}
    </motion.div>
  )
}
```

### 2. Page Transition Wrapper

```typescript
// src/components/layout/PageTransition.tsx
import { motion } from 'framer-motion'
import { ReactNode } from 'react'

const pageVariants = {
  initial: { opacity: 0, x: -20 },
  enter: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 20 }
}

export function PageTransition({ children }: { children: ReactNode }) {
  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="enter"
      exit="exit"
      transition={{ duration: 0.4, ease: [0.6, 0.05, 0.01, 0.9] }}
    >
      {children}
    </motion.div>
  )
}
```

### 3. Floating Action Button

```typescript
// src/components/ui/FloatingButton.tsx
import { motion } from 'framer-motion'
import { Plus } from 'lucide-react'

export default function FloatingButton({ onClick }: { onClick: () => void }) {
  return (
    <motion.button
      whileHover={{ scale: 1.1, rotate: 90 }}
      whileTap={{ scale: 0.9 }}
      onClick={onClick}
      className="fixed bottom-8 right-8 w-14 h-14 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-full shadow-lg flex items-center justify-center text-white z-50"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5, type: 'spring' }}
    >
      <Plus size={24} />
    </motion.button>
  )
}
```

## 🎢 Lenis Smooth Scroll Setup

### Hook Implementation

```typescript
// src/hooks/useSmoothScroll.ts
import { useEffect } from 'react'
import Lenis from 'lenis'

export function useSmoothScroll() {
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      smoothTouch: false,
      touchMultiplier: 2,
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

// Usage in App.tsx or DashboardLayout.tsx
import { useSmoothScroll } from './hooks/useSmoothScroll'

function App() {
  useSmoothScroll()
  
  return <div>Your app</div>
}
```

---

## 🚀 Quick Start Checklist

- [ ] Copy Plotly chart components to `src/components/charts/`
- [ ] Copy React-Leaflet map to `src/components/maps/`
- [ ] Copy Framer Motion examples to pages
- [ ] Add `useSmoothScroll` hook to App.tsx
- [ ] Test all animations and interactions
- [ ] Verify API connections to FastAPI backend
- [ ] Deploy and enjoy! 🎉
