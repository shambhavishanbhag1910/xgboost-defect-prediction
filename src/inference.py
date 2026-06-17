from pathlib import Path
import joblib
import pandas as pd
MODEL_PATH = Path('models/xgboost_defect_pipeline.pkl')
def load_model():
    if not MODEL_PATH.exists(): raise FileNotFoundError('Model artifact not found. Train the model first.')
    return joblib.load(MODEL_PATH)
def create_inference_features(input_data: dict) -> pd.DataFrame:
    df = pd.DataFrame([input_data])
    df['good_qty'] = df['actual_qty'] - df['rejected_qty']
    df['production_achievement_pct'] = df['actual_qty'] / df['planned_qty']
    df['rejection_rate'] = df['rejected_qty'] / df['actual_qty']
    df['good_rate'] = df['good_qty'] / df['actual_qty']
    df['downtime_per_1000_units'] = df['downtime_minutes'] / (df['actual_qty'] / 1000)
    df['is_night_shift'] = (df['shift'] == 'C').astype(int)
    df['is_high_criticality'] = (df['machine_criticality'] == 'High').astype(int)
    df['supplier_risk_bucket'] = df['supplier_risk_score'].apply(lambda x: 'Low' if x <= 0.33 else ('Medium' if x <= 0.66 else 'High'))
    if 'plant' not in df.columns: df['plant'] = 'Chakan'
    if 'line' not in df.columns: df['line'] = 'Line_A'
    return df
