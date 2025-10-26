#!/usr/bin/env pwsh
# Vani React Setup Script - Windows PowerShell
# Run this from: C:\workspace\yes-scan-apex\yes_scan_prototype

Write-Host "🌊 Vani React Dashboard Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create Vite project
Write-Host "📦 Step 1: Creating React + Vite + TypeScript project..." -ForegroundColor Yellow
npm create vite@latest vani-frontend -- --template react-ts

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create Vite project" -ForegroundColor Red
    exit 1
}

# Step 2: Navigate to project
Set-Location vani-frontend

# Step 3: Install core dependencies
Write-Host ""
Write-Host "📚 Step 2: Installing core dependencies..." -ForegroundColor Yellow
npm install react-router-dom @clerk/clerk-react

# Step 4: Install Tailwind
Write-Host ""
Write-Host "🎨 Step 3: Installing Tailwind CSS..." -ForegroundColor Yellow
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Step 5: Install shadcn/ui dependencies
Write-Host ""
Write-Host "🎭 Step 4: Installing shadcn/ui dependencies..." -ForegroundColor Yellow
npm install tailwindcss-animate class-variance-authority clsx tailwind-merge
npm install @radix-ui/react-slot @radix-ui/react-toast @radix-ui/react-dialog
npm install @radix-ui/react-dropdown-menu @radix-ui/react-tabs
npm install lucide-react

# Step 6: Install Plotly
Write-Host ""
Write-Host "📊 Step 5: Installing Plotly.js for graphs..." -ForegroundColor Yellow
npm install plotly.js-dist-min react-plotly.js
npm install -D @types/plotly.js

# Step 7: Install React-Leaflet
Write-Host ""
Write-Host "🗺️ Step 6: Installing React-Leaflet for maps..." -ForegroundColor Yellow
npm install leaflet react-leaflet
npm install -D @types/leaflet

# Step 8: Install Framer Motion
Write-Host ""
Write-Host "✨ Step 7: Installing Framer Motion for animations..." -ForegroundColor Yellow
npm install framer-motion

# Step 9: Install Lenis
Write-Host ""
Write-Host "🎢 Step 8: Installing Lenis for smooth scrolling..." -ForegroundColor Yellow
npm install lenis

# Step 10: Install utilities
Write-Host ""
Write-Host "🔧 Step 9: Installing utilities..." -ForegroundColor Yellow
npm install date-fns

# Step 11: Create .env file
Write-Host ""
Write-Host "🔑 Step 10: Creating environment file..." -ForegroundColor Yellow

$envContent = @"
VITE_CLERK_PUBLISHABLE_KEY=pk_test_bWVycnktbW9sbHVzay03NS5jbGVyay5hY2NvdW50cy5kZXYk
VITE_API_BASE_URL=http://127.0.0.1:8000
"@

Set-Content -Path ".env" -Value $envContent

Write-Host ""
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Copy Tailwind config from REACT_MIGRATION_PLAN.md to tailwind.config.js" -ForegroundColor White
Write-Host "  2. Set up shadcn/ui components: npx shadcn-ui@latest init" -ForegroundColor White
Write-Host "  3. Create src/ folder structure (see REACT_MIGRATION_PLAN.md)" -ForegroundColor White
Write-Host "  4. Start dev server: npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "📖 Full guide: ../REACT_MIGRATION_PLAN.md" -ForegroundColor Cyan
Write-Host ""

# Open VS Code if available
if (Get-Command code -ErrorAction SilentlyContinue) {
    Write-Host "🚀 Opening in VS Code..." -ForegroundColor Yellow
    code .
}
