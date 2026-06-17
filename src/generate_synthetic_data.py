from pathlib import Path
import numpy as np
import pandas as pd

np.random.seed(42)
OUTPUT_PATH = Path('data/raw/manufacturing_defect_data.csv')
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
N = 5000
plants = ['Chakan', 'Nashik', 'Bangalore']
lines = ['Line_A', 'Line_B', 'Line_C', 'Line_D']
shifts = ['A', 'B', 'C']
criticalities = ['Low', 'Medium', 'High']
part_categories = ['Engine', 'Transmission', 'Brake', 'Electronics', 'Axle']
supplier_regions = ['West', 'South', 'North', 'East']
rows = []
for i in range(N):
    planned_qty = np.random.randint(700, 1300)
    actual_qty = max(1, int(planned_qty * np.random.uniform(0.72, 1.05)))
    supplier_risk_score = round(float(np.random.beta(2, 4)), 2)
    machine_age_years = int(np.random.randint(1, 12))
    downtime_minutes = int(np.random.poisson(35))
    machine_criticality = np.random.choice(criticalities, p=[0.25, 0.45, 0.30])
    shift = np.random.choice(shifts)
    part_category = np.random.choice(part_categories)
    supplier_region = np.random.choice(supplier_regions)
    rejection_rate = np.random.uniform(0.01, 0.05)
    if supplier_risk_score > 0.65: rejection_rate += np.random.uniform(0.02, 0.05)
    if machine_criticality == 'High' and downtime_minutes > 60: rejection_rate += np.random.uniform(0.02, 0.06)
    if shift == 'C': rejection_rate += np.random.uniform(0.005, 0.025)
    if part_category in ['Electronics', 'Engine']: rejection_rate += np.random.uniform(0.005, 0.02)
    rejected_qty = int(actual_qty * min(rejection_rate, 0.25))
    good_qty = actual_qty - rejected_qty
    risk_score = 0.35*(rejected_qty/actual_qty) + 0.25*supplier_risk_score + 0.15*(downtime_minutes/180) + 0.10*(machine_age_years/12) + 0.10*(machine_criticality=='High') + 0.05*(shift=='C')
    defect_risk_flag = 1 if risk_score > 0.22 or (rejected_qty/actual_qty) > 0.08 else 0
    if np.random.rand() < 0.03: defect_risk_flag = 1 - defect_risk_flag
    rows.append({
        'batch_id': f'BATCH_{i+1:05d}', 'plant': np.random.choice(plants), 'line': np.random.choice(lines),
        'planned_qty': planned_qty, 'actual_qty': actual_qty, 'good_qty': good_qty, 'rejected_qty': rejected_qty,
        'downtime_minutes': downtime_minutes, 'supplier_risk_score': supplier_risk_score,
        'machine_age_years': machine_age_years, 'machine_criticality': machine_criticality, 'shift': shift,
        'part_category': part_category, 'supplier_region': supplier_region, 'defect_risk_flag': defect_risk_flag
    })
df = pd.DataFrame(rows)
df.to_csv(OUTPUT_PATH, index=False)
print(f'Created {OUTPUT_PATH} with {len(df)} rows')
print(df['defect_risk_flag'].value_counts(normalize=True))
