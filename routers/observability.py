from fastapi import APIRouter, HTTPException
import logging
from utils.tracing import init_tracer
from utils.anomaly_detection import detect_anomalies
from utils.self_healing import execute_self_healing

router = APIRouter()

# Initialize tracing
tracer = init_tracer()

@router.get("/health")
async def health_check():
    try:
        with tracer.start_as_current_span("health-check"):
            # Simulate health check logic
            return {"status": "healthy"}
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

@router.post("/analyze")
async def analyze_system_data(data: dict):
    try:
        with tracer.start_as_current_span("analyze-data"):
            anomalies = detect_anomalies(data)
            if anomalies:
                execute_self_healing(anomalies)
            return {"anomalies": anomalies}
    except Exception as e:
        logging.error(f"Data analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Data analysis failed")