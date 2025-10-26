# YES-Scan Apex - Weather API Integration Guide

## 🌦️ OpenWeatherMap One Call API 3.0

YES-Scan Apex now uses the **One Call API 3.0** from OpenWeatherMap, which provides comprehensive weather data in a single API call.

---

## 📋 API Endpoints

### 1. **One Call Endpoint** (All-in-One)
Get current weather, hourly/daily forecasts, and alerts in one call.

**Endpoint:** `GET /api/weather/onecall`

**Parameters:**
- `lat` (float): Latitude (default: 20.2961)
- `lon` (float): Longitude (default: 85.8245)
- `exclude` (string): Comma-separated list to exclude: `minutely,hourly,daily,alerts,current`

**Example:**
```bash
GET http://localhost:8000/api/weather/onecall?lat=20.2961&lon=85.8245&exclude=minutely
```

**Response includes:**
- `current`: Current weather conditions
- `hourly`: 48-hour hourly forecast
- `daily`: 7-day daily forecast
- `alerts`: Weather alerts and warnings

---

### 2. **Current Weather**
Simplified endpoint for current conditions only.

**Endpoint:** `GET /api/weather/current`

**Response:**
```json
{
  "temp": 28.5,
  "feels_like": 30.2,
  "humidity": 78,
  "description": "heavy rain",
  "icon": "10d",
  "wind_speed": 4.5,
  "pressure": 1008,
  "uvi": 0.5,
  "visibility": 8000
}
```

---

### 3. **7-Day Forecast**
Get daily weather forecast for the next 7 days.

**Endpoint:** `GET /api/weather/forecast`

**Response:**
```json
{
  "daily": [
    {
      "date": "Oct 26",
      "temp_max": 30,
      "temp_min": 24,
      "rainfall": 95,
      "icon": "10d",
      "desc": "heavy rain",
      "pop": 0.9,
      "humidity": 78,
      "wind_speed": 4.5,
      "summary": "Heavy rain expected with flood risk"
    }
  ]
}
```

---

### 4. **Weather Alerts**
Get active weather warnings and alerts.

**Endpoint:** `GET /api/weather/alerts`

**Response:**
```json
{
  "alerts": [
    {
      "sender_name": "India Meteorological Department (IMD)",
      "event": "Heavy Rainfall Warning",
      "start": 1729929600,
      "end": 1730102400,
      "description": "Heavy to very heavy rainfall expected...",
      "tags": ["Flood", "Rain"]
    }
  ]
}
```

---

## 🔑 Getting Your API Key

### Step 1: Sign Up
1. Visit: https://openweathermap.org/api
2. Click **"Sign Up"** (or **"Sign In"** if you have an account)
3. Complete registration with your email

### Step 2: Get API Key
1. Go to: https://home.openweathermap.org/api_keys
2. Your default API key will be displayed
3. Or create a new key with a custom name
4. Copy the API key (it looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

### Step 3: Subscribe to One Call API 3.0
1. Go to: https://openweathermap.org/api/one-call-3
2. Click **"Subscribe"** under **"One Call by Call"**
3. This is a **Pay-as-you-go** plan:
   - First **1,000 calls/day are FREE**
   - After that: **$0.0015 per call** (very affordable!)
4. No monthly fee, only pay for what you use

### Step 4: Activate Your Key
1. API keys can take **10-15 minutes** to activate
2. You'll receive a confirmation email
3. Test your key at: https://api.openweathermap.org/data/3.0/onecall?lat=20.2961&lon=85.8245&appid=YOUR_API_KEY

### Step 5: Add to YES-Scan Apex
1. Open `.env` file in project root
2. Update the line:
   ```env
   WEATHER_API_KEY=your_actual_api_key_here
   ```
3. Save the file
4. Restart the backend server

---

## 🎨 Weather Icons Mapping

The dashboard automatically converts OpenWeather icon codes to emoji:

| Icon Code | Emoji | Description |
|-----------|-------|-------------|
| `01d` / `01n` | ☀️ 🌙 | Clear sky (day/night) |
| `02d` / `02n` | 🌤️ ☁️ | Few clouds |
| `03d` / `03n` | ☁️ | Scattered clouds |
| `04d` / `04n` | ☁️ | Broken/overcast clouds |
| `09d` / `09n` | 🌧️ | Shower rain |
| `10d` / `10n` | 🌧️ | Rain |
| `11d` / `11n` | ⛈️ | Thunderstorm |
| `13d` / `13n` | ❄️ | Snow |
| `50d` / `50n` | 🌫️ | Mist/Fog |

---

## 📊 Features in Dashboard

### Current Weather Card
- Large temperature display with emoji icon
- Feels-like temperature
- Humidity percentage
- Wind speed
- Pressure, UV index, visibility

### 7-Day Forecast Cards
- Daily high/low temperatures
- Weather icon and description
- Rainfall amount and probability (%)
- Wind speed
- Color-coded by day

### Weather Alerts
- Automatic display of active warnings
- Source organization (IMD, NWS, etc.)
- Start/end timestamps
- Full description with recommendations
- Color-coded by severity (danger/warning)

---

## 🧪 Testing Without API Key

The system works perfectly **without an API key** using realistic mock data:

- ✅ All endpoints return valid mock responses
- ✅ Dashboard displays properly with demo data
- ✅ Weather icons show correctly
- ✅ Alerts display with flood warnings
- ✅ Perfect for development and demos

When you add a real API key, the system automatically switches to live data!

---

## 💡 Usage Examples

### Basic Usage (Default Location - Odisha)
```javascript
// Frontend code
fetch('http://localhost:8000/api/weather/forecast')
  .then(res => res.json())
  .then(data => {
    console.log('7-day forecast:', data.daily);
  });
```

### Custom Location
```javascript
// Get weather for Mumbai
fetch('http://localhost:8000/api/weather/forecast?lat=19.0760&lon=72.8777')
  .then(res => res.json())
  .then(data => {
    console.log('Mumbai forecast:', data.daily);
  });
```

### Get All Data at Once
```javascript
// One Call API - get everything
fetch('http://localhost:8000/api/weather/onecall?lat=20.2961&lon=85.8245')
  .then(res => res.json())
  .then(data => {
    console.log('Current:', data.current);
    console.log('Hourly:', data.hourly);
    console.log('Daily:', data.daily);
    console.log('Alerts:', data.alerts);
  });
```

---

## 🚨 Error Handling

The API gracefully handles errors:

1. **No API Key**: Falls back to mock data
2. **API Limit Reached**: Returns cached/mock data
3. **Network Error**: Returns mock data with error message
4. **Invalid Coordinates**: OpenWeather returns nearest location

**Error Response Example:**
```json
{
  "error": "Weather API unavailable: 401 Unauthorized"
}
```

Frontend continues to work with mock data even if backend fails!

---

## 📈 API Pricing (One Call API 3.0)

### Free Tier
- ✅ **1,000 calls per day FREE**
- ✅ Perfect for small deployments
- ✅ Great for demos and development

### Paid Usage
- 💰 **$0.0015 per call** after free tier
- 💰 No monthly subscription
- 💰 Pay only for what you use

### Example Costs
| Daily Calls | Monthly Cost |
|-------------|--------------|
| 1,000 | **FREE** |
| 5,000 | $6/month |
| 10,000 | $13.50/month |
| 50,000 | $67.50/month |

---

## 🔧 Advanced Configuration

### Exclude Specific Data
Save API credits by excluding data you don't need:

```bash
# Only get current weather
GET /api/weather/onecall?exclude=minutely,hourly,daily,alerts

# Only get daily forecast
GET /api/weather/onecall?exclude=minutely,hourly,current,alerts

# Only get alerts
GET /api/weather/onecall?exclude=minutely,hourly,daily,current
```

### Change Units
Modify in `.env` file:
```env
# Default units: Kelvin
# Metric: Celsius (used by YES-Scan)
# Imperial: Fahrenheit
```

Backend always uses `units=metric` for consistent Celsius temperatures.

---

## 📝 API Response Fields

### Current Weather (`current`)
- `dt`: Unix timestamp
- `temp`: Temperature (°C)
- `feels_like`: Perceived temperature (°C)
- `pressure`: Atmospheric pressure (hPa)
- `humidity`: Humidity (%)
- `uvi`: UV index
- `clouds`: Cloudiness (%)
- `visibility`: Visibility (meters)
- `wind_speed`: Wind speed (m/s)
- `rain.1h`: Rainfall in last hour (mm)
- `weather[0].icon`: Weather icon code

### Daily Forecast (`daily`)
- `dt`: Unix timestamp for the day
- `temp.max/min/day/night/eve/morn`: Temperatures
- `pop`: Probability of precipitation (0-1)
- `rain`: Rainfall amount (mm)
- `humidity`: Humidity (%)
- `wind_speed`: Wind speed (m/s)
- `weather[0].icon`: Weather icon code
- `summary`: AI-generated weather summary

### Alerts (`alerts`)
- `sender_name`: Alert source organization
- `event`: Alert type/name
- `start/end`: Unix timestamps
- `description`: Full alert text
- `tags`: Alert categories

---

## 🎯 Best Practices

1. **Cache Results**: Cache weather data for 10-15 minutes
2. **Handle Errors**: Always have fallback mock data
3. **Respect Limits**: Don't exceed free tier if possible
4. **Use Exclude**: Only fetch data you need
5. **Test First**: Use mock data during development

---

## 🆘 Troubleshooting

### API Key Not Working?
- ✅ Wait 10-15 minutes after creation
- ✅ Check you subscribed to One Call API 3.0
- ✅ Verify key is correctly pasted in `.env`
- ✅ Restart backend server after updating `.env`

### Getting 401 Errors?
- API key not activated yet (wait 15 min)
- API key is invalid (generate new one)
- Subscription not active (subscribe to One Call by Call)

### Mock Data Still Showing?
- Verify `WEATHER_API_KEY` is not `demo_key`
- Check backend logs for errors
- Test API key directly: https://api.openweathermap.org/data/3.0/onecall?lat=20&lon=85&appid=YOUR_KEY

### No Alerts Showing?
- Alerts only appear when there are active warnings
- Try different locations with known weather events
- Mock data always includes one sample alert

---

## 📞 Support

- **OpenWeather Support**: https://openweathermap.org/faq
- **API Documentation**: https://openweathermap.org/api/one-call-3
- **YES-Scan Support**: support@yesscan.in

---

**Happy Weather Tracking! 🌦️**
