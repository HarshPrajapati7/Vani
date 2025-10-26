# Vani - Netlify Deployment Guide

## 🚀 Quick Deploy to Netlify

### Prerequisites
1. GitHub account
2. Netlify account (free tier works fine)
3. OpenWeather API key (get from https://openweathermap.org/api)

### Step 1: Prepare Repository
```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit - Ready for Netlify deployment"

# Push to GitHub
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Deploy on Netlify

#### Option A: Deploy via Netlify UI (Recommended)
1. Go to https://app.netlify.com
2. Click "Add new site" → "Import an existing project"
3. Choose "GitHub" and select your repository
4. Configure build settings:
   - **Build command**: `pip install -r requirements.txt`
   - **Publish directory**: `frontend_static`
   - **Functions directory**: `netlify/functions`
5. Add environment variables (in Site settings → Environment variables):
   ```
   WEATHER_API_KEY=your_openweather_api_key_here
   PYTHON_VERSION=3.11
   ```
6. Click "Deploy site"

#### Option B: Deploy via Netlify CLI
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Initialize and deploy
netlify init
netlify deploy --prod
```

### Step 3: Configure Clerk Authentication
1. Go to your Clerk dashboard (https://dashboard.clerk.com)
2. Update the following URLs with your Netlify domain:
   - **Authorized redirect URLs**: `https://your-site-name.netlify.app/dashboard.html`
   - **Sign-out URLs**: `https://your-site-name.netlify.app/`
3. Update the frontend files with your Netlify URL if needed

### Step 4: Environment Variables
Set these in Netlify dashboard under Site settings → Environment variables:

```
WEATHER_API_KEY=your_openweather_api_key
PYTHON_VERSION=3.11
```

### Step 5: Custom Domain (Optional)
1. Go to Site settings → Domain management
2. Add your custom domain
3. Update DNS records as instructed by Netlify
4. SSL certificate will be automatically provisioned

## 📁 Project Structure

```
yes_scan_prototype/
├── frontend_static/          # Static frontend files (served by Netlify CDN)
│   ├── index.html           # Landing page
│   ├── login.html           # Clerk authentication
│   ├── dashboard.html       # Main dashboard
│   └── dashboard-preview.png
├── backend/                  # FastAPI backend
│   └── app/
│       └── main.py          # API routes
├── netlify/
│   └── functions/
│       └── api.py           # Serverless function wrapper
├── netlify.toml             # Netlify configuration
├── requirements.txt         # Python dependencies
├── runtime.txt              # Python version
└── build.sh                 # Build script

```

## 🔧 Configuration Files Explained

### netlify.toml
- Configures build settings
- Sets up API proxy to serverless functions
- Defines redirects and headers
- Handles SPA routing

### netlify/functions/api.py
- Wraps FastAPI app with Mangum
- Converts FastAPI to AWS Lambda-compatible handler
- Enables serverless execution on Netlify

### requirements.txt
- Lists all Python dependencies
- Auto-generated from your virtual environment
- Includes FastAPI, Uvicorn, httpx, Mangum, etc.

## 🌐 API Endpoints After Deployment

Your API will be available at:
```
https://your-site-name.netlify.app/api/weather/current
https://your-site-name.netlify.app/api/weather/forecast
https://your-site-name.netlify.app/api/weather/alerts
https://your-site-name.netlify.app/api/farms
```

The `/api/*` routes are automatically proxied to Netlify Functions.

## 🐛 Troubleshooting

### Build Fails
- Check Netlify build logs
- Ensure all dependencies are in requirements.txt
- Verify Python version matches runtime.txt

### API Returns 404
- Check netlify.toml redirects configuration
- Ensure functions directory is set to `netlify/functions`
- Verify api.py imports work correctly

### Environment Variables Not Working
- Make sure variables are set in Netlify dashboard
- Redeploy after adding/changing environment variables
- Check variable names match exactly

### Clerk Authentication Issues
- Update Clerk dashboard with correct Netlify URLs
- Clear browser cache and cookies
- Check browser console for errors

## 📊 Monitoring

- **Netlify Analytics**: Site settings → Analytics (basic stats included free)
- **Function Logs**: Functions tab → View function logs
- **Deploy Logs**: Deploys tab → Click any deploy to see logs

## 🔄 Continuous Deployment

Once connected to GitHub:
1. Every push to `main` branch triggers automatic deployment
2. Pull requests create deploy previews
3. You can also set up branch deploys for staging

## 💰 Pricing Considerations

**Netlify Free Tier Includes:**
- 100GB bandwidth/month
- 300 build minutes/month
- 125k serverless function invocations/month
- Automatic HTTPS
- Deploy previews

This should be sufficient for development and moderate production use.

## 🚀 Post-Deployment Checklist

- [ ] Site loads correctly
- [ ] API endpoints respond
- [ ] Clerk authentication works
- [ ] Weather data loads (with real API key)
- [ ] Mobile responsive design works
- [ ] All pages accessible
- [ ] Maps render correctly
- [ ] Charts display data
- [ ] Forms submit successfully

## 📞 Support

For issues with:
- **Netlify**: https://docs.netlify.com or Netlify Support
- **Clerk**: https://clerk.com/docs or Clerk Support
- **OpenWeather API**: https://openweathermap.org/faq

---

**Ready to deploy?** Follow the steps above and your Vani application will be live in minutes! 🎉
