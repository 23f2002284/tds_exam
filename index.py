from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Load telemetry data
FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'q-vercel-latency.json')
with open(FILE_PATH, 'r') as f:
    telemetry_data = json.load(f)
df = pd.DataFrame(telemetry_data)

@app.post("/api")
async def process_telemetry(payload: dict = Body(...)):
    regions = payload.get("regions", [])
    threshold = payload.get("threshold_ms", 180)
    
    results = {}
    
    for region in regions:
        region_df = df[df['region'] == region]
        if region_df.empty:
            continue
            
        avg_latency = float(region_df['latency_ms'].mean())
        p95_latency = float(region_df['latency_ms'].quantile(0.95))
        avg_uptime = float(region_df['uptime_pct'].mean())
        breaches = int((region_df['latency_ms'] > threshold).sum())
        
        results[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches
        }
        
    return results
