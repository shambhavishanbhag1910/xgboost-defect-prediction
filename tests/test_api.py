from fastapi.testclient import TestClient
from api.main import app
client = TestClient(app)
def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'healthy'
def test_predict():
    payload = {'planned_qty':1000,'actual_qty':880,'rejected_qty':55,'downtime_minutes':85,'supplier_risk_score':0.78,'machine_age_years':6,'machine_criticality':'High','shift':'B','part_category':'Engine','supplier_region':'West','plant':'Chakan','line':'Line_A'}
    r = client.post('/predict', json=payload)
    assert r.status_code == 200
    assert 'defect_risk_probability' in r.json()
