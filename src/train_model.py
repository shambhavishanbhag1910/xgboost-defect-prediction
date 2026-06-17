from pathlib import Path
import json, joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier
DATA_PATH = Path('data/processed/features.csv')
MODEL_DIR = Path('models'); MODEL_DIR.mkdir(parents=True, exist_ok=True)
TARGET = 'defect_risk_flag'
DROP_COLS = ['batch_id', 'good_qty', TARGET]
NUMERIC_FEATURES = ['planned_qty','actual_qty','rejected_qty','downtime_minutes','supplier_risk_score','machine_age_years','production_achievement_pct','rejection_rate','good_rate','downtime_per_1000_units','is_night_shift','is_high_criticality']
CATEGORICAL_FEATURES = ['plant','line','machine_criticality','shift','part_category','supplier_region','supplier_risk_bucket']

def train():
    df = pd.read_csv(DATA_PATH)
    X, y = df.drop(columns=DROP_COLS), df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    preprocessor = ColumnTransformer([('num', StandardScaler(), NUMERIC_FEATURES), ('cat', OneHotEncoder(handle_unknown='ignore'), CATEGORICAL_FEATURES)])
    model = XGBClassifier(n_estimators=250, max_depth=4, learning_rate=0.05, subsample=0.9, colsample_bytree=0.9, eval_metric='logloss', random_state=42)
    pipe = Pipeline([('preprocessor', preprocessor), ('model', model)])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test); y_proba = pipe.predict_proba(X_test)[:,1]
    metrics = {
        'precision': round(float(precision_score(y_test, y_pred)),4),
        'recall': round(float(recall_score(y_test, y_pred)),4),
        'f1_score': round(float(f1_score(y_test, y_pred)),4),
        'roc_auc': round(float(roc_auc_score(y_test, y_proba)),4),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
        'classification_report': classification_report(y_test, y_pred, output_dict=True)
    }
    joblib.dump(pipe, MODEL_DIR/'xgboost_defect_pipeline.pkl')
    (MODEL_DIR/'model_metrics.json').write_text(json.dumps(metrics, indent=4))
    print(json.dumps(metrics, indent=4))
if __name__ == '__main__': train()
