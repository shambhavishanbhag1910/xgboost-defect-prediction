from pathlib import Path
import json
p=Path('models/model_metrics.json')
if not p.exists(): raise FileNotFoundError('Run src/train_model.py first')
print(json.dumps(json.loads(p.read_text()), indent=4))
