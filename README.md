# AWS-Ready XGBoost Manufacturing Defect Prediction

This is a production-style prototype for an AI Engineer portfolio. It demonstrates an end-to-end manufacturing defect prediction workflow using synthetic SAP-like production, quality, batch, machine, part, and supplier data.

## What this project includes

- Synthetic manufacturing data generation
- Feature engineering pipeline
- XGBoost defect prediction model
- FastAPI inference service
- Docker containerization
- GitHub Actions CI workflow
- AWS deployment guide for EC2 and ECS
- Basic API tests

## Business Problem

Manufacturing quality teams need early visibility into high-risk production batches before defects become quality escapes, rework, scrap, warranty cost, or customer dissatisfaction.

## Target Variable

`defect_risk_flag`

- `1` = High-risk batch
- `0` = Normal batch

The synthetic target is generated using realistic manufacturing risk logic such as rejection rate, supplier risk, machine criticality, downtime, and unstable production achievement.

## Architecture

```text
Synthetic SAP-like Data
        ↓
Feature Engineering
        ↓
XGBoost Model Training
        ↓
Model Pipeline Artifact
        ↓
FastAPI Inference API
        ↓
Docker Container
        ↓
AWS EC2 / ECS Deployment
```

## Run Locally

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt

python src/generate_synthetic_data.py
python src/feature_engineering.py
python src/train_model.py
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Open:

```text
http://localhost:8000/docs
```

## Run with Docker

```bash
docker build -t xgboost-defect-api .
docker run -p 8000:8000 xgboost-defect-api
```

## Example API Payload

```json
{
  "planned_qty": 1000,
  "actual_qty": 880,
  "rejected_qty": 55,
  "downtime_minutes": 85,
  "supplier_risk_score": 0.78,
  "machine_age_years": 6,
  "machine_criticality": "High",
  "shift": "B",
  "part_category": "Engine",
  "supplier_region": "West",
  "plant": "Chakan",
  "line": "Line_A"
}
```

## Resume Bullet

Built an AWS-ready manufacturing defect prediction prototype using synthetic SAP-like production and quality data, XGBoost, FastAPI, Docker, and GitHub Actions to classify high-risk production batches and expose real-time inference through a cloud-deployable API.

## Interview Explanation

I built an AWS-ready XGBoost defect prediction prototype for manufacturing quality risk detection. The project generates SAP-like synthetic production and quality data, engineers batch, machine, part, supplier, and quality features, trains an XGBoost classifier, saves the full preprocessing and model pipeline, exposes predictions through FastAPI, containerizes the service with Docker, and can be deployed on AWS EC2 or ECS.

## Cloud Deployment Proof to Add After Deployment

After deploying on AWS, add these to this README:

- Public API URL
- `/health` response screenshot
- `/docs` Swagger screenshot
- `/predict` request/response screenshot
- EC2/ECS screenshot
