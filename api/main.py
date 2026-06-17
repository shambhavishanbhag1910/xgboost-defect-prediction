from fastapi import FastAPI
from pydantic import BaseModel, Field
from src.inference import load_model, create_inference_features
import time
import logging
#from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time
import logging
from fastapi import Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title='Manufacturing Defect Prediction API', description='AWS-ready XGBoost API for predicting high-risk manufacturing batches.', version='1.0.0')
model = load_model()
class DefectPredictionRequest(BaseModel):
    planned_qty: int = Field(..., example=1000)
    actual_qty: int = Field(..., example=880)
    rejected_qty: int = Field(..., example=55)
    downtime_minutes: int = Field(..., example=85)
    supplier_risk_score: float = Field(..., ge=0, le=1, example=0.78)
    machine_age_years: int = Field(..., example=6)
    machine_criticality: str = Field(..., example='High')
    shift: str = Field(..., example='B')
    part_category: str = Field(..., example='Engine')
    supplier_region: str = Field(..., example='West')
    plant: str = Field('Chakan', example='Chakan')
    line: str = Field('Line_A', example='Line_A')
@app.get('/health')
def health_check(): return {'status':'healthy','service':'xgboost-defect-prediction-api'}
@app.post('/predict')
def predict_defect_risk(request: DefectPredictionRequest):
    

    start_time = time.time()
    PREDICTION_REQUESTS.inc()

    features = create_inference_features(request.model_dump())
    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1])
    return {'prediction': prediction, 'risk_label': 'High Risk' if prediction == 1 else 'Normal', 'defect_risk_probability': round(probability,4), 'recommendation': 'Review batch quality and supplier/machine conditions' if prediction == 1 else 'No immediate action required'}

    latency = time.time() - start_time
    PREDICTION_LATENCY.observe(latency)

    logging.info(f"Prediction completed | probability={probability} | risk={risk_label} | latency={latency}")

    if risk_label == "High Risk":
        HIGH_RISK_PREDICTIONS.inc()
    else:
        LOW_RISK_PREDICTIONS.inc()

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

PREDICTION_REQUESTS = Counter(
    "prediction_requests_total",
    "Total number of prediction requests"
)

HIGH_RISK_PREDICTIONS = Counter(
    "high_risk_predictions_total",
    "Total number of high-risk predictions"
)

LOW_RISK_PREDICTIONS = Counter(
    "low_risk_predictions_total",
    "Total number of low-risk predictions"
)

PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds",
    "Prediction request latency in seconds"
)