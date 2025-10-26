from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json, hashlib, random, time, os, io, base64
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import numpy as np
from shapely.geometry import shape as shapely_shape
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# JWT and password hashing
try:
    from jose import JWTError, jwt
    from passlib.context import CryptContext
    JWT_AVAILABLE = True
except:
    JWT_AVAILABLE = False

# PDF generation
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    PDF_AVAILABLE = True
except:
    PDF_AVAILABLE = False

# Weather API
try:
    import requests
    REQUESTS_AVAILABLE = True
except:
    REQUESTS_AVAILABLE = False

# Optional torch import for DL endpoint
try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except Exception:
    TORCH_AVAILABLE = False
try:
    import joblib
except Exception:
    joblib = None

app = FastAPI(title="Vani - Flood Insurance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security setup - Clerk will handle authentication
# Keep minimal JWT support for legacy endpoints
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") if JWT_AVAILABLE else None
security = HTTPBearer(auto_error=False)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY", "")

# Note: Demo credentials removed. Use Clerk for authentication.
# All users authenticate through Clerk's secure sign-in flow.

# Load fields (robust to current working directory)
try:
    # Try project-root relative path first
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    candidate_paths = [
        PROJECT_ROOT / "data" / "sample_fields.geojson",
        Path(__file__).resolve().parent / "data" / "sample_fields.geojson",
        Path.cwd() / "data" / "sample_fields.geojson",
    ]
    geojson_path = next((p for p in candidate_paths if p.exists()), None)
    if not geojson_path:
        raise FileNotFoundError("sample_fields.geojson not found in expected locations")
    with open(geojson_path, "r", encoding="utf-8") as f:
        GEOJSON = json.load(f)
except Exception as e:
    # Fail fast with a clear message (helps when uvicorn started from a different CWD)
    raise RuntimeError(f"Failed to load sample fields GeoJSON: {e}")

# ============= AUTH ENDPOINTS - DEPRECATED =============
# Note: Authentication is now handled by Clerk on the frontend.
# These endpoints are kept for backward compatibility but will be removed.

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Optional dependency for protected endpoints.
    Returns None if no credentials provided (Clerk handles auth on frontend).
    """
    if not credentials:
        return None
    
    if not JWT_AVAILABLE:
        return {"username": "demo@vani.in", "role": "user"}
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return {"username": username, "role": payload.get("role", "user")}
    except JWTError:
        return None

@app.post("/api/auth/login", response_model=TokenResponse, deprecated=True)
def login(req: LoginRequest):
    """
    DEPRECATED: Use Clerk authentication instead.
    This endpoint is kept for backward compatibility only.
    """
    raise HTTPException(
        status_code=410,
        detail="This authentication method is deprecated. Please use Clerk sign-in."
    )

@app.get("/api/auth/me", deprecated=True)
def get_me(current_user: dict = Depends(get_current_user)):
    """
    DEPRECATED: Use Clerk's user management instead.
    """
    raise HTTPException(
        status_code=410,
        detail="This endpoint is deprecated. User info is managed by Clerk."
    )

# ============= WEATHER ENDPOINTS (One Call API 3.0) =============

@app.get("/api/weather/onecall")
def get_weather_onecall(lat: float = 20.2961, lon: float = 85.8245, exclude: str = "minutely"):
    """
    One Call API 3.0 - Get current weather, hourly, daily forecast, and alerts
    https://api.openweathermap.org/data/3.0/onecall
    """
    api_key = os.getenv("WEATHER_API_KEY", "demo_key")
    
    if api_key == "demo_key" or not REQUESTS_AVAILABLE:
        # Return comprehensive mock data
        return {
            "lat": lat,
            "lon": lon,
            "timezone": "Asia/Kolkata",
            "timezone_offset": 19800,
            "current": {
                "dt": int(time.time()),
                "temp": 28.5,
                "feels_like": 30.2,
                "pressure": 1008,
                "humidity": 78,
                "dew_point": 24.1,
                "uvi": 0.5,
                "clouds": 85,
                "visibility": 8000,
                "wind_speed": 4.5,
                "wind_deg": 240,
                "weather": [{"id": 501, "main": "Rain", "description": "heavy rain", "icon": "10d"}],
                "rain": {"1h": 12.5}
            },
            "hourly": [
                {
                    "dt": int(time.time()) + i*3600,
                    "temp": 28 - i*0.5,
                    "feels_like": 29 - i*0.5,
                    "pressure": 1008,
                    "humidity": 75 + i,
                    "wind_speed": 4 + i*0.3,
                    "weather": [{"id": 501, "main": "Rain", "description": "moderate rain", "icon": "10d"}],
                    "pop": 0.8 - i*0.05
                } for i in range(8)
            ],
            "daily": [
                {"dt": int(time.time()) + i*86400, "temp": {"day": 30-i, "min": 24, "max": 32-i, "night": 26, "eve": 28, "morn": 25},
                 "feels_like": {"day": 32, "night": 27, "eve": 29, "morn": 26},
                 "pressure": 1008, "humidity": 78, "wind_speed": 4.5, "wind_deg": 240, "clouds": 85,
                 "pop": 0.9 - i*0.1, "rain": 95 - i*10, "uvi": 5.2,
                 "weather": [{"id": 501, "main": "Rain", "description": "heavy rain", "icon": "10d"}],
                 "summary": "Heavy rain expected with flood risk"
                } for i in range(7)
            ],
            "alerts": [
                {
                    "sender_name": "India Meteorological Department (IMD)",
                    "event": "Heavy Rainfall Warning",
                    "start": int(time.time()),
                    "end": int(time.time()) + 172800,
                    "description": "Heavy to very heavy rainfall expected in coastal Odisha. Flood risk HIGH. Farmers advised to harvest ready crops immediately and prepare drainage systems.",
                    "tags": ["Flood", "Rain"]
                }
            ]
        }
    
    try:
        # Use One Call API 3.0 endpoint
        url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
            "exclude": exclude
        }
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        # Fallback to mock data if API fails
        print(f"Weather API error: {e}")
        return {"error": f"Weather API unavailable: {str(e)}"}

@app.get("/api/weather/current")
def get_current_weather(lat: float = 20.2961, lon: float = 85.8245):
    """Get current weather - simplified endpoint"""
    onecall = get_weather_onecall(lat, lon, exclude="minutely,hourly,daily,alerts")
    
    if "error" in onecall or "current" not in onecall:
        # Return mock data
        return {
            "temp": 28.5,
            "feels_like": 30.2,
            "humidity": 78,
            "description": "Heavy Rain",
            "icon": "10d",
            "wind_speed": 4.5,
            "pressure": 1008,
            "uvi": 0.5,
            "visibility": 8000
        }
    
    current = onecall["current"]
    return {
        "temp": current.get("temp", 0),
        "feels_like": current.get("feels_like", 0),
        "humidity": current.get("humidity", 0),
        "description": current["weather"][0]["description"] if current.get("weather") else "",
        "icon": current["weather"][0]["icon"] if current.get("weather") else "01d",
        "wind_speed": current.get("wind_speed", 0),
        "pressure": current.get("pressure", 0),
        "uvi": current.get("uvi", 0),
        "visibility": current.get("visibility", 10000)
    }

@app.get("/api/weather/forecast")
def get_weather_forecast(lat: float = 20.2961, lon: float = 85.8245):
    """Get 7-day forecast"""
    onecall = get_weather_onecall(lat, lon, exclude="minutely,current,hourly,alerts")
    
    if "error" in onecall or "daily" not in onecall:
        # Return mock 7-day forecast
        return {
            "daily": [
                {"date": "Oct 26", "temp_max": 30, "temp_min": 24, "rainfall": 95, "icon": "10d", "desc": "Heavy Rain", "pop": 0.9, "humidity": 78, "wind_speed": 4.5},
                {"date": "Oct 27", "temp_max": 29, "temp_min": 23, "rainfall": 110, "icon": "11d", "desc": "Thunderstorm", "pop": 0.95, "humidity": 82, "wind_speed": 5.2},
                {"date": "Oct 28", "temp_max": 31, "temp_min": 25, "rainfall": 20, "icon": "02d", "desc": "Partly Cloudy", "pop": 0.3, "humidity": 65, "wind_speed": 3.8},
                {"date": "Oct 29", "temp_max": 32, "temp_min": 26, "rainfall": 5, "icon": "01d", "desc": "Clear Sky", "pop": 0.1, "humidity": 55, "wind_speed": 3.2},
                {"date": "Oct 30", "temp_max": 33, "temp_min": 26, "rainfall": 8, "icon": "02d", "desc": "Few Clouds", "pop": 0.15, "humidity": 58, "wind_speed": 3.5},
                {"date": "Oct 31", "temp_max": 31, "temp_min": 25, "rainfall": 15, "icon": "03d", "desc": "Scattered Clouds", "pop": 0.25, "humidity": 62, "wind_speed": 4.0},
                {"date": "Nov 1", "temp_max": 30, "temp_min": 24, "rainfall": 30, "icon": "09d", "desc": "Light Rain", "pop": 0.6, "humidity": 70, "wind_speed": 4.2}
            ]
        }
    
    daily_data = []
    for day in onecall.get("daily", [])[:7]:
        daily_data.append({
            "date": datetime.fromtimestamp(day["dt"]).strftime("%b %d"),
            "temp_max": day["temp"]["max"],
            "temp_min": day["temp"]["min"],
            "rainfall": day.get("rain", 0),
            "icon": day["weather"][0]["icon"] if day.get("weather") else "01d",
            "desc": day["weather"][0]["description"] if day.get("weather") else "",
            "pop": day.get("pop", 0),
            "humidity": day.get("humidity", 0),
            "wind_speed": day.get("wind_speed", 0),
            "summary": day.get("summary", "")
        })
    
    return {"daily": daily_data}

@app.get("/api/weather/alerts")
def get_weather_alerts(lat: float = 20.2961, lon: float = 85.8245):
    """Get weather alerts for location"""
    onecall = get_weather_onecall(lat, lon, exclude="minutely,current,hourly,daily")
    
    if "error" in onecall or "alerts" not in onecall:
        # Return mock alert
        return {
            "alerts": [
                {
                    "sender_name": "India Meteorological Department (IMD)",
                    "event": "Heavy Rainfall Warning",
                    "start": int(time.time()),
                    "end": int(time.time()) + 172800,
                    "description": "Heavy to very heavy rainfall expected in coastal Odisha. Flood risk HIGH. Farmers advised to harvest ready crops immediately.",
                    "tags": ["Flood", "Rain"]
                }
            ]
        }
    
    return {"alerts": onecall.get("alerts", [])}

# ============= EXISTING ENDPOINTS =============

@app.get("/api/farms")
def farms():
    return GEOJSON

class TriageInput(BaseModel):
    sat_source: str
    date: str
    ndvi_threshold: float

@app.post("/api/triage/run")
def run_triage(inp: TriageInput):
    hotspots = []
    for feat in GEOJSON["features"]:
        ndvi = round(random.uniform(0.1, 0.8), 2)
        if ndvi < inp.ndvi_threshold:
            hotspots.append({
                "field_id": feat["properties"]["field_id"],
                "ndvi": ndvi
            })
    return {"hotspots": hotspots}

class ModelInput(BaseModel):
    field_id: str
    ndvi_mean: float
    avg_temp_c: float
    rainfall_mm: float

@app.post("/api/model/run")
def run_model(inp: ModelInput):
    # ORYZA-stub math
    yield_est = inp.ndvi_mean * 60  
    ci = yield_est * 0.12
    return {
        "field_id": inp.field_id,
        "yield_est_q_ha": round(yield_est, 2),
        "ci_low": round(yield_est - ci, 2),
        "ci_high": round(yield_est + ci, 2),
        "model_run_id": f"MR{int(time.time())}"
    }

@app.post("/api/claim/create")
def create_claim(model_run_id: str, field_id: str):
    claim_id = f"C{int(time.time())}"
    data = f"{model_run_id}-{field_id}"
    audit_hash = hashlib.sha256(data.encode()).hexdigest()
    return {"claim_id": claim_id, "audit_hash": audit_hash}

@app.get("/api/claim/{claim_id}/pdf")
def generate_claim_pdf(claim_id: str):
    """Generate PDF claim report"""
    if not PDF_AVAILABLE:
        raise HTTPException(status_code=500, detail="PDF generation unavailable (install reportlab)")
    
    # Mock claim data (in production, fetch from database)
    claim_data = {
        "claim_id": claim_id,
        "field_id": "F-2301",
        "farmer_name": "Ramesh Kumar",
        "farmer_phone": "+91 98765 43210",
        "location": "20.2961, 85.8245",
        "area_ha": 3.2,
        "crop_type": "Rice (Paddy)",
        "flooded_pct": 42.5,
        "confidence": 93.8,
        "evidence_hash": hashlib.sha256(claim_id.encode()).hexdigest(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Verified",
        "payout_amount": 85000
    }
    
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#10b981'),
        spaceAfter=30,
        alignment=1
    )
    story.append(Paragraph("YES-Scan Apex", title_style))
    story.append(Paragraph("Flood Insurance Claim Report", styles['Heading2']))
    story.append(Spacer(1, 0.5*inch))
    
    # Claim details table
    data = [
        ['Claim Information', ''],
        ['Claim ID:', claim_data['claim_id']],
        ['Field ID:', claim_data['field_id']],
        ['Status:', claim_data['status']],
        ['Timestamp:', claim_data['timestamp']],
        ['', ''],
        ['Farmer Information', ''],
        ['Name:', claim_data['farmer_name']],
        ['Phone:', claim_data['farmer_phone']],
        ['Location:', claim_data['location']],
        ['Farm Area:', f"{claim_data['area_ha']} hectares"],
        ['Crop Type:', claim_data['crop_type']],
        ['', ''],
        ['Assessment Results', ''],
        ['Flood Affected Area:', f"{claim_data['flooded_pct']}%"],
        ['Model Confidence:', f"{claim_data['confidence']}%"],
        ['Evidence Hash (SHA-256):', claim_data['evidence_hash'][:32] + '...'],
        ['', ''],
        ['Claim Settlement', ''],
        ['Approved Payout:', f"₹{claim_data['payout_amount']:,}"],
    ]
    
    table = Table(data, colWidths=[2.5*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 6), (-1, 6), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 6), (-1, 6), colors.whitesmoke),
        ('BACKGROUND', (0, 13), (-1, 13), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 13), (-1, 13), colors.whitesmoke),
        ('BACKGROUND', (0, 18), (-1, 18), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 18), (-1, 18), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer = Paragraph(
        "<i>This report is generated by YES-Scan Apex AI system and verified by field officers. "
        "For queries, contact support@yesscan.in</i>",
        styles['Normal']
    )
    story.append(footer)
    
    doc.build(story)
    buffer.seek(0)
    
    # Return as base64 for frontend download
    pdf_b64 = base64.b64encode(buffer.read()).decode()
    return {
        "claim_id": claim_id,
        "pdf_base64": pdf_b64,
        "filename": f"claim_{claim_id}.pdf"
    }



# ----------------------
# DL: FT-Transformer serving
# ----------------------
# Locate models directory relative to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
FT_MODEL_PATH = os.path.join(MODELS_DIR, "best_tabtransformer.pt")
FT_SCALER_PATH = os.path.join(MODELS_DIR, "tab_scaler.joblib")
FT_META_PATH = os.path.join(MODELS_DIR, "tab_meta.json")

ft_loaded = False
soil_vocab: List[str] = []
cont_cols: List[str] = []
cat_col: str = "soil_type"
ft_model = None
ft_scaler = None

if TORCH_AVAILABLE and os.path.exists(FT_MODEL_PATH) and os.path.exists(FT_SCALER_PATH) and os.path.exists(FT_META_PATH) and joblib is not None:
    # Define minimal model to load weights (must match training definition)
    class FeatureTokenizer(nn.Module):
        def __init__(self, n_cont, d_model):
            super().__init__()
            self.linears = nn.ModuleList([nn.Linear(1, d_model) for _ in range(n_cont)])
        def forward(self, x):
            tokens = []
            for j, lin in enumerate(self.linears):
                tok = lin(x[:, j:j+1])
                tokens.append(tok)
            return torch.stack(tokens, dim=1)

    class FTTransformer(nn.Module):
        def __init__(self, n_cont, n_cat, d_model=64, nhead=4, nlayers=2, dropout=0.1):
            super().__init__()
            self.cls = nn.Parameter(torch.randn(1,1,d_model))
            self.cont_tok = FeatureTokenizer(n_cont, d_model)
            self.cat_emb = nn.Embedding(n_cat, d_model)
            enc_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=256, dropout=dropout, batch_first=True)
            self.encoder = nn.TransformerEncoder(enc_layer, num_layers=nlayers)
            self.head = nn.Sequential(nn.LayerNorm(d_model), nn.Linear(d_model, 1))
        def forward(self, x_cont, x_cat):
            B = x_cont.size(0)
            cont_tokens = self.cont_tok(x_cont)
            cat_token = self.cat_emb(x_cat).unsqueeze(1)
            tokens = torch.cat([cont_tokens, cat_token], dim=1)
            cls = self.cls.expand(B, -1, -1)
            seq = torch.cat([cls, tokens], dim=1)
            enc = self.encoder(seq)
            cls_out = enc[:,0,:]
            return self.head(cls_out)

    try:
        with open(FT_META_PATH, "r") as f:
            meta = json.load(f)
        cont_cols = meta.get("cont_cols") or meta.get("features") or []
        cat_col = meta.get("cat_col", "soil_type")
        soil_vocab = meta.get("soil_vocab", ["loam","clay","sandy"])
        n_cont = len(cont_cols)
        n_cat = len(soil_vocab)
        ft_model = FTTransformer(n_cont, n_cat)
        ft_model.load_state_dict(torch.load(FT_MODEL_PATH, map_location="cpu"))
        ft_model.eval()
        ft_scaler = joblib.load(FT_SCALER_PATH)
        ft_loaded = True
    except Exception as e:
        ft_loaded = False


class DLInput(BaseModel):
    # Expect all continuous features and a soil_type string
    ndvi_mean: float = 0.35
    ndvi_std: float = 0.05
    evi_mean: float = 0.3
    avg_temp_c: float = 29.0
    rainfall_mm: float = 260.0
    plant_density_plants_m2: float = 20.0
    fertilizer_kg_ha: float = 90.0
    irrigation_mm: float = 40.0
    elevation_m: float = 100.0
    slope_pct: float = 1.0
    prior_yield_qha: float = 35.0
    sowing_doy: int = 180
    soil_type: str = "loam"


@app.post("/api/model/dl-run")
def dl_run(inp: DLInput):
    if not TORCH_AVAILABLE:
        return {"status":"error","message":"PyTorch not available in backend environment."}
    if not ft_loaded:
        return {"status":"error","message":"DL model artifacts not found or failed to load. Train notebook to generate models."}
    # Build input vector in cont_cols order
    sample = {
        "ndvi_mean": inp.ndvi_mean,
        "ndvi_std": inp.ndvi_std,
        "evi_mean": inp.evi_mean,
        "avg_temp_c": inp.avg_temp_c,
        "rainfall_mm": inp.rainfall_mm,
        "plant_density_plants_m2": inp.plant_density_plants_m2,
        "fertilizer_kg_ha": inp.fertilizer_kg_ha,
        "irrigation_mm": inp.irrigation_mm,
        "elevation_m": inp.elevation_m,
        "slope_pct": inp.slope_pct,
        "prior_yield_qha": inp.prior_yield_qha,
        "sowing_doy": inp.sowing_doy,
    }
    x_cont = np.array([[sample.get(k, 0.0) for k in cont_cols]], dtype=np.float32)
    x_cont_s = ft_scaler.transform(x_cont)
    soil_idx = soil_vocab.index(inp.soil_type) if inp.soil_type in soil_vocab else 0
    with torch.no_grad():
        xc = torch.tensor(x_cont_s, dtype=torch.float32)
        xcat = torch.tensor([soil_idx], dtype=torch.int64)
        pred = ft_model(xc, xcat).squeeze(1).cpu().numpy()[0].item()
    return {"yield_est_q_ha": round(float(pred), 2), "model": "FT-Transformer", "soil_vocab": soil_vocab}


# ----------------------
# U-Net demo segmentation (2-channel 256x256)
# ----------------------
UNET_PATH = os.path.join(MODELS_DIR, "best_unet.pt")
UNET_READY = False
UNET_DEVICE = "cpu"
unet_model = None

try:
    import torch
    import torch.nn as nn
    class DoubleConv(nn.Module):
        def __init__(self, in_ch, out_ch):
            super().__init__()
            self.seq = nn.Sequential(
                nn.Conv2d(in_ch, out_ch, 3, padding=1), nn.BatchNorm2d(out_ch), nn.ReLU(inplace=True),
                nn.Conv2d(out_ch, out_ch, 3, padding=1), nn.BatchNorm2d(out_ch), nn.ReLU(inplace=True),
            )
        def forward(self, x):
            return self.seq(x)

    class UNetSmall(nn.Module):
        def __init__(self, in_ch=2, out_ch=1):
            super().__init__()
            self.down1 = DoubleConv(in_ch, 32)
            self.pool1 = nn.MaxPool2d(2)
            self.down2 = DoubleConv(32, 64)
            self.pool2 = nn.MaxPool2d(2)
            self.down3 = DoubleConv(64, 128)
            self.pool3 = nn.MaxPool2d(2)
            self.bott = DoubleConv(128, 256)
            self.up3 = nn.ConvTranspose2d(256, 128, 2, stride=2)
            self.conv3 = DoubleConv(256, 128)
            self.up2 = nn.ConvTranspose2d(128, 64, 2, stride=2)
            self.conv2 = DoubleConv(128, 64)
            self.up1 = nn.ConvTranspose2d(64, 32, 2, stride=2)
            self.conv1 = DoubleConv(64, 32)
            self.outc = nn.Conv2d(32, out_ch, 1)
        def forward(self, x):
            d1 = self.down1(x); p1 = self.pool1(d1)
            d2 = self.down2(p1); p2 = self.pool2(d2)
            d3 = self.down3(p2); p3 = self.pool3(d3)
            b = self.bott(p3)
            u3 = self.up3(b); c3 = self.conv3(torch.cat([u3, d3], dim=1))
            u2 = self.up2(c3); c2 = self.conv2(torch.cat([u2, d2], dim=1))
            u1 = self.up1(c2); c1 = self.conv1(torch.cat([u1, d1], dim=1))
            return self.outc(c1)

    if os.path.exists(UNET_PATH):
        unet_model = UNetSmall(in_ch=2, out_ch=1)
        state = torch.load(UNET_PATH, map_location="cpu")
        unet_model.load_state_dict(state)
        unet_model.eval()
        UNET_READY = True
except Exception:
    UNET_READY = False


@app.get("/api/segment/unet/demo")
def unet_demo(threshold: float = 0.5):
    if not UNET_READY:
        return {"status":"error","message":"U-Net model not available. Train with train_unet.ipynb first."}
    import torch
    from PIL import Image
    # Synthetic demo tile: circle region brighter in both channels
    size = 256
    img = np.random.rand(2, size, size).astype("float32")*0.1
    msk = np.zeros((size, size), dtype="float32")
    cx, cy = np.random.randint(64, size-64, 2)
    rr, cc = np.ogrid[:size, :size]
    rad = np.random.randint(25, 55)
    circle = (rr-cy)**2 + (cc-cx)**2 <= rad*rad
    msk[circle] = 1.0
    img[0][circle] += 0.8; img[1][circle] += 0.6
    with torch.no_grad():
        x = torch.from_numpy(img)[None, ...]
        pred = unet_model(x).squeeze(0)
        prob = torch.sigmoid(pred).numpy()[0]
    pred_bin = (prob > float(threshold)).astype(np.uint8)
    flooded_pct = float(pred_bin.sum()/(size*size)*100.0)
    # Encode PNG (single-channel mask 0/255)
    pil = Image.fromarray((pred_bin*255).astype(np.uint8), mode="L")
    buf = io.BytesIO()
    pil.save(buf, format="PNG")
    mask_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return {"flooded_pct": round(flooded_pct,2), "size": size, "mask_png_base64": mask_b64}


@app.post("/api/segment/unet")
def unet_predict(
    tile_npy: Optional[UploadFile] = File(None),
    vv_png: Optional[UploadFile] = File(None),
    vh_png: Optional[UploadFile] = File(None),
    bounds: Optional[str] = None,  # JSON stringified [south, west, north, east]
    field_id: Optional[str] = None,  # for polygon clipping
    threshold: float = 0.5,
):
    if not UNET_READY:
        return {"status":"error","message":"U-Net model not available. Train with train_unet.ipynb first."}
    import torch
    from PIL import Image

    arr = None
    if tile_npy is not None:
        raw = tile_npy.file.read()
        arr = np.load(io.BytesIO(raw))  # expects (2,H,W)
    elif vv_png is not None and vh_png is not None:
        vv = Image.open(io.BytesIO(vv_png.file.read())).convert("L")
        vh = Image.open(io.BytesIO(vh_png.file.read())).convert("L")
        vv_np = (np.array(vv).astype("float32")/255.0)
        vh_np = (np.array(vh).astype("float32")/255.0)
        if vv_np.shape != vh_np.shape:
            return {"status":"error","message":"vv_png and vh_png must have same dimensions."}
        arr = np.stack([vv_np, vh_np], axis=0)
    else:
        # Fallback: generate a synthetic demo tile (same as /demo) for quick UI wiring
        size = 256
        img = np.random.rand(2, size, size).astype("float32")*0.1
        msk_demo = np.zeros((size, size), dtype="float32")
        cx, cy = np.random.randint(64, size-64, 2)
        rr, cc = np.ogrid[:size, :size]
        rad = np.random.randint(25, 55)
        circle = (rr-cy)**2 + (cc-cx)**2 <= rad*rad
        msk_demo[circle] = 1.0
        img[0][circle] += 0.8; img[1][circle] += 0.6
        arr = img

    if arr.ndim != 3 or arr.shape[0] != 2:
        return {"status":"error","message":"Expected image array with shape (2, H, W)."}
    with torch.no_grad():
        x = torch.from_numpy(arr.astype("float32"))[None, ...]
        pred = unet_model(x).squeeze(0)
        prob = torch.sigmoid(pred).numpy()[0]
    pred_bin = (prob > float(threshold)).astype(np.uint8)
    flooded_pct = float(pred_bin.sum()/(pred_bin.size)*100.0)

    # Polygon-aware per-field flooded percent if field_id + bounds provided
    flooded_pct_in_field = None
    img_bounds = None
    if bounds:
        try:
            img_bounds = json.loads(bounds) if isinstance(bounds, str) else bounds
        except Exception:
            img_bounds = None
    if field_id and img_bounds and isinstance(img_bounds, (list, tuple)) and len(img_bounds)==4:
        south, west, north, east = img_bounds
        # Find field polygon from loaded GEOJSON
        field_geom = None
        for feat in GEOJSON.get("features", []):
            if str(feat.get("properties", {}).get("field_id")) == str(field_id):
                field_geom = shapely_shape(feat.get("geometry"))
                break
        if field_geom is not None and not field_geom.is_empty:
            H, W = pred_bin.shape
            transform = from_bounds(west, south, east, north, width=W, height=H)
            poly_mask = rasterize(
                [(field_geom, 1)], out_shape=(H, W), transform=transform, fill=0, dtype=np.uint8
            )
            inside = poly_mask.astype(bool)
            denom = float(inside.sum())
            if denom > 0:
                flooded_pct_in_field = float((pred_bin.astype(bool) & inside).sum())/denom*100.0
    pil = Image.fromarray((pred_bin*255).astype(np.uint8), mode="L")
    buf = io.BytesIO(); pil.save(buf, format="PNG")
    mask_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    resp = {"flooded_pct": round(flooded_pct,2), "mask_png_base64": mask_b64}
    # Echo bounds back if provided (client can overlay with these Leaflet bounds)
    if bounds:
        try:
            resp["bounds"] = json.loads(bounds)
        except Exception:
            resp["bounds"] = bounds
    if flooded_pct_in_field is not None:
        resp["flooded_pct_in_field"] = round(flooded_pct_in_field, 2)
    return resp


@app.post("/api/segment/unet/by-field")
def unet_by_field(field_id: str, date: str = "", threshold: float = 0.5):
    """Attempt to locate a tile from manifests that overlaps the field bbox and run segmentation.
    Requires manifests with columns: image_path (npy), and optionally south,west,north,east.
    """
    if not UNET_READY:
        return {"status":"error","message":"U-Net model not available. Train with train_unet.ipynb first."}
    # Find field geometry and bbox
    fld = None
    for feat in GEOJSON.get("features", []):
        if str(feat.get("properties", {}).get("field_id")) == str(field_id):
            fld = feat; break
    if not fld:
        return {"status":"error","message":f"field_id {field_id} not found"}
    geom = shapely_shape(fld.get("geometry"))
    minx, miny, maxx, maxy = geom.bounds
    # Read manifests
    man_dir = os.path.join(PROJECT_ROOT, "processed", "manifests")
    cand_paths = []
    for name in ["tiles.csv", "train.csv", "val.csv"]:
        p = os.path.join(man_dir, name)
        if os.path.exists(p):
            cand_paths.append(p)
    if not cand_paths:
        return {"status":"error","message":"No manifests found; run preprocessing.ipynb first."}
    import pandas as pd
    df_list = [pd.read_csv(p) for p in cand_paths]
    df = pd.concat(df_list, ignore_index=True)
    # Prefer rows with bounds present
    has_bounds = all(col in df.columns for col in ["south","west","north","east"])
    if not has_bounds:
        return {"status":"error","message":"Manifests missing bounds columns (south,west,north,east). Re-run preprocessing to include tile bounds."}
    # Simple overlap test
    sel = df[((df["west"] <= maxx) & (df["east"] >= minx) & (df["south"] <= maxy) & (df["north"] >= miny))]
    if len(sel)==0:
        return {"status":"error","message":"No tiles overlap field bbox. Check manifests or date selection."}
    row = sel.iloc[0]
    img_path = row.get("image_path")
    if not img_path or not os.path.exists(img_path):
        # Try path relative to project root
        rel = os.path.join(PROJECT_ROOT, str(img_path)) if img_path else None
        if rel and os.path.exists(rel):
            img_path = rel
        else:
            return {"status":"error","message":f"Tile not found on disk: {img_path}"}
    arr = np.load(img_path).astype("float32")
    if arr.ndim!=3 or arr.shape[0]!=2:
        return {"status":"error","message":"Tile array must be (2,H,W)."}
    # Run model
    import torch
    with torch.no_grad():
        x = torch.from_numpy(arr)[None, ...]
        pred = unet_model(x).squeeze(0)
        prob = torch.sigmoid(pred).numpy()[0]
    pred_bin = (prob > float(threshold)).astype(np.uint8)
    flooded_pct = float(pred_bin.sum()/pred_bin.size*100.0)
    # Polygon clip using manifest bounds
    south, west, north, east = float(row["south"]), float(row["west"]), float(row["north"]), float(row["east"])
    H, W = pred_bin.shape
    transform = from_bounds(west, south, east, north, width=W, height=H)
    poly_mask = rasterize([(geom,1)], out_shape=(H,W), transform=transform, fill=0, dtype=np.uint8)
    inside = poly_mask.astype(bool)
    denom = float(inside.sum())
    flooded_pct_in_field = None
    if denom>0:
        flooded_pct_in_field = float((pred_bin.astype(bool) & inside).sum())/denom*100.0
    # Encode PNG
    from PIL import Image
    pil = Image.fromarray((pred_bin*255).astype(np.uint8), mode="L")
    buf = io.BytesIO(); pil.save(buf, format="PNG")
    mask_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return {
        "flooded_pct": round(flooded_pct,2),
        "flooded_pct_in_field": round(flooded_pct_in_field,2) if flooded_pct_in_field is not None else None,
        "bounds": [south, west, north, east],
        "mask_png_base64": mask_b64,
        "tile_path": img_path,
    }
