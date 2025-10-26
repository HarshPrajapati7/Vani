# YES-Scan Apex - Environment Setup Guide

## 🔐 Setting Up Your Environment

### 1. Weather API (OpenWeatherMap)

Get your **free API key** from OpenWeatherMap:

1. Visit: https://openweathermap.org/api
2. Sign up for free account
3. Navigate to **API Keys** section
4. Copy your API key
5. Add to `.env` file:
   ```
   WEATHER_API_KEY=your_actual_api_key_here
   ```

**Free tier includes:**
- Current weather data
- 7-day forecast
- 1,000 API calls per day

### 2. Database Configuration (Future)

For production deployment with PostgreSQL + PostGIS:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/yes_scan_db
```

**Setup PostgreSQL with PostGIS:**
```bash
# Install PostgreSQL
# Install PostGIS extension
# Run migrations (when ready)
```

### 3. JWT Authentication

The default JWT secret is **dev-secret-key**. 

**⚠️ IMPORTANT for production:**
Generate a secure random key:

```python
import secrets
print(secrets.token_urlsafe(32))
```

Then update in `.env`:
```
JWT_SECRET_KEY=your-super-secure-random-key-here
```

### 4. SMS Alerts (Optional)

For SMS notifications (Twilio, AWS SNS, or similar):

```env
SMS_API_KEY=your_twilio_api_key
SMS_FROM_NUMBER=+919876543210
```

### 5. Cloud Storage (Optional)

For orthomosaic image uploads (AWS S3, Azure Blob):

```env
CLOUD_STORAGE_BUCKET=yes-scan-orthomosaics
CLOUD_STORAGE_KEY=your_cloud_storage_access_key
```

## 🌦️ Weather Icons

The dashboard uses emoji icons mapped to OpenWeatherMap icon codes:

| Icon Code | Emoji | Description |
|-----------|-------|-------------|
| 01d/01n | ☀️🌙 | Clear sky |
| 02d/02n | 🌤️☁️ | Few clouds |
| 03d/03n | ☁️ | Scattered clouds |
| 04d/04n | ☁️ | Broken clouds |
| 09d/09n | 🌧️ | Shower rain |
| 10d/10n | 🌧️ | Rain |
| 11d/11n | ⛈️ | Thunderstorm |
| 13d/13n | ❄️ | Snow |
| 50d/50n | 🌫️ | Mist/Fog |

## 📄 PDF Generation

PDF claim reports are generated using **ReportLab** and include:

- Claim ID and timestamp
- Farmer information
- Field location and crop details
- Flood assessment results
- Model confidence score
- SHA-256 evidence hash
- Approved payout amount

**Download endpoint:**
```
GET /api/claim/{claim_id}/pdf
```

Returns base64-encoded PDF for frontend download.

## 🔑 Demo Credentials

**Field Officer:**
- Email: `officer@yesscan.in`
- Password: `officer123`

**Farmer:**
- Email: `farmer@yesscan.in`
- Password: `farmer123`

## 🚀 Quick Start

1. Copy `.env.example` to `.env`
2. Add your OpenWeatherMap API key
3. Start backend: `.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload`
4. Start frontend: `python -m http.server 8080`
5. Open browser: `http://127.0.0.1:8080/frontend_static/login.html`
6. Login with demo credentials
7. Explore dashboard features!

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Weather
- `GET /api/weather/current?lat=20.2961&lon=85.8245` - Current weather
- `GET /api/weather/forecast?lat=20.2961&lon=85.8245` - 7-day forecast

### Claims
- `POST /api/claim/create` - Create new claim
- `GET /api/claim/{claim_id}/pdf` - Download PDF report

### Segmentation
- `POST /api/segment/unet` - Run U-Net segmentation
- `POST /api/segment/unet/by-field` - Segment specific field

### Farms
- `GET /api/farms` - Get all farms (GeoJSON)

## 🎨 UI Customization

The dashboard uses CSS variables for easy theming:

```css
:root{
  --primary:#10b981;        /* Main brand color */
  --primary-dark:#059669;   /* Darker variant */
  --secondary:#14b8a6;      /* Accent color */
  --danger:#ef4444;         /* Error/Alert color */
  --warning:#f59e0b;        /* Warning color */
  --info:#3b82f6;           /* Info color */
}
```

Change these values in `dashboard.html` to customize your theme!

## 🔧 Troubleshooting

### Weather API not working?
- Check your API key in `.env`
- Ensure you've activated the key on OpenWeatherMap
- Verify free tier limits not exceeded

### PDF download fails?
- Ensure `reportlab` is installed: `pip install reportlab`
- Check backend logs for errors

### Login not working?
- Verify backend is running on port 8000
- Check browser console for CORS errors
- Ensure JWT libraries installed: `pip install python-jose[cryptography] passlib[bcrypt]`

## 📝 Next Steps for Production

1. **Database**: Set up PostgreSQL with PostGIS
2. **Real auth**: Integrate with existing user management
3. **Weather**: Add your paid API key for higher limits
4. **Storage**: Connect to cloud storage for orthomosaics
5. **SMS**: Configure Twilio or AWS SNS for alerts
6. **Hosting**: Deploy to Azure/AWS with HTTPS
7. **Monitoring**: Add logging and error tracking

---

**Need help?** Contact support@yesscan.in
