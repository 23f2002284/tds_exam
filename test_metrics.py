import pandas as pd
import json

def calculate_metrics(file_path, regions, threshold):
    with open(file_path, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    
    results = {}
    for region in regions:
        region_df = df[df['region'] == region]
        if not region_df.empty:
            results[region] = {
                "avg_latency": float(region_df['latency_ms'].mean()),
                "p95_latency": float(region_df['latency_ms'].quantile(0.95)),
                "avg_uptime": float(region_df['uptime_pct'].mean()),
                "breaches": int((region_df['latency_ms'] > threshold).sum())
            }
    return results

if __name__ == "__main__":
    res = calculate_metrics('q-vercel-latency.json', ["emea", "apac"], 178)
    print(json.dumps(res, indent=2))
