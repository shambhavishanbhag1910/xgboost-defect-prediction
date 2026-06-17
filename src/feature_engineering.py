from pathlib import Path
import pandas as pd
INPUT_PATH = Path('data/raw/manufacturing_defect_data.csv')
OUTPUT_PATH = Path('data/processed/features.csv')
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['production_achievement_pct'] = df['actual_qty'] / df['planned_qty']
    df['rejection_rate'] = df['rejected_qty'] / df['actual_qty']
    df['good_rate'] = df['good_qty'] / df['actual_qty']
    df['downtime_per_1000_units'] = df['downtime_minutes'] / (df['actual_qty'] / 1000)
    df['is_night_shift'] = (df['shift'] == 'C').astype(int)
    df['is_high_criticality'] = (df['machine_criticality'] == 'High').astype(int)
    df['supplier_risk_bucket'] = pd.cut(df['supplier_risk_score'], bins=[-0.01,0.33,0.66,1.0], labels=['Low','Medium','High']).astype(str)
    return df.replace([float('inf'), -float('inf')], 0).fillna(0)

if __name__ == '__main__':
    df = pd.read_csv(INPUT_PATH)
    out = create_features(df)
    out.to_csv(OUTPUT_PATH, index=False)
    print(f'Created {OUTPUT_PATH} with {len(out)} rows')
