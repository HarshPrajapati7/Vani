import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mangum import Mangum
from backend.app.main import app

# Create the Netlify serverless function handler
handler = Mangum(app, lifespan="off")
