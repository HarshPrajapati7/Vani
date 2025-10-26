# 📋 Netlify Deployment Checklist

## Pre-Deployment
- [x] netlify.toml created
- [x] requirements.txt generated
- [x] runtime.txt set to Python 3.11
- [x] netlify/functions/api.py created
- [x] .gitignore configured
- [x] DEPLOYMENT.md guide written
- [ ] Get OpenWeather API key from https://openweathermap.org/api

## Git Setup
```bash
git init
git add .
git commit -m "Ready for Netlify deployment"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

## Netlify Setup
1. [ ] Create account at https://app.netlify.com
2. [ ] Click "Add new site" → "Import an existing project"
3. [ ] Connect to GitHub and select repository
4. [ ] Configure build settings:
   - Build command: `pip install -r requirements.txt`
   - Publish directory: `frontend_static`
   - Functions directory: `netlify/functions`
5. [ ] Add environment variables:
   ```
   WEATHER_API_KEY=your_api_key_here
   PYTHON_VERSION=3.11
   ```
6. [ ] Click "Deploy site"

## Post-Deployment
1. [ ] Test landing page loads
2. [ ] Test API endpoint: `https://your-site.netlify.app/api/weather/current`
3. [ ] Update Clerk dashboard with Netlify URL:
   - Authorized redirect URLs
   - Sign-out URLs
4. [ ] Test login flow
5. [ ] Test dashboard loads with data
6. [ ] Test mobile responsiveness
7. [ ] Test weather integration
8. [ ] Test all pages (Home, Farms, Claims, Weather, Admin)

## Optional Enhancements
- [ ] Set up custom domain
- [ ] Configure Netlify Analytics
- [ ] Set up form notifications
- [ ] Enable deploy previews for PRs
- [ ] Set up branch deploys for staging

## Verification URLs
Replace `your-site-name` with your actual Netlify site name:

- Landing: `https://your-site-name.netlify.app/`
- Login: `https://your-site-name.netlify.app/login.html`
- Dashboard: `https://your-site-name.netlify.app/dashboard.html`
- API: `https://your-site-name.netlify.app/api/weather/current`

## Troubleshooting
If build fails:
1. Check Netlify build logs
2. Verify requirements.txt has all dependencies
3. Ensure Python version matches runtime.txt
4. Check netlify.toml syntax

If functions don't work:
1. Check Functions tab in Netlify dashboard
2. View function logs for errors
3. Verify api.py imports correctly
4. Check environment variables are set

## Success Criteria
✅ Site is live and accessible
✅ All pages load without errors
✅ API endpoints return data
✅ Clerk authentication works
✅ Weather data displays
✅ Mobile navigation works
✅ Forms are functional
✅ Maps and charts render

---
**Ready to deploy? Follow the checklist and refer to DEPLOYMENT.md for detailed instructions!**
