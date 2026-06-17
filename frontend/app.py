import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Manufacturing Defect Prediction",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Manufacturing Defect Prediction Platform")
st.write("AWS-deployed XGBoost model with FastAPI, Docker, Prometheus, Grafana, and Evidently monitoring.")

API_URL = st.sidebar.text_input(
    "FastAPI URL",
    value="http://16.170.251.13:8000"
)

st.sidebar.markdown("### System Links")
st.sidebar.write(f"[API Health]({API_URL}/health)")
st.sidebar.write(f"[API Docs]({API_URL}/docs)")
st.sidebar.write(f"[Metrics]({API_URL}/metrics)")

st.subheader("Enter Production & Quality Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    production_qty = st.number_input("Production Quantity", min_value=1, value=500)
    rejected_qty = st.number_input("Rejected Quantity", min_value=0, value=12)
    defect_count = st.number_input("Defect Count", min_value=0, value=5)

with col2:
    rework_count = st.number_input("Rework Count", min_value=0, value=3)
    cycle_time = st.number_input("Cycle Time", min_value=1.0, value=45.0)
    machine_downtime = st.number_input("Machine Downtime", min_value=0.0, value=20.0)

with col3:
    supplier_risk_score = st.slider("Supplier Risk Score", 0.0, 1.0, 0.35)
    temperature = st.number_input("Temperature", min_value=0.0, value=72.0)
    shift = st.selectbox("Shift", ["A", "B", "C"])

payload = {
    "production_qty": production_qty,
    "rejected_qty": rejected_qty,
    "defect_count": defect_count,
    "rework_count": rework_count,
    "cycle_time": cycle_time,
    "machine_downtime": machine_downtime,
    "supplier_risk_score": supplier_risk_score,
    "temperature": temperature,
    "shift": shift
}

st.subheader("Prediction Request Payload")
st.json(payload)

if st.button("Predict Defect Risk"):
    try:
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()

            st.success("Prediction completed successfully")

            col_a, col_b, col_c = st.columns(3)

            with col_a:
                st.metric("Risk Level", result.get("risk_level", result.get("risk", "NA")))

            with col_b:
                st.metric("Defect Probability", result.get("defect_probability", result.get("probability", "NA")))

            with col_c:
                st.metric("Prediction", result.get("prediction", "NA"))

            st.subheader("Full API Response")
            st.json(result)

            st.subheader("Recommendation")
            risk = str(result.get("risk_level", result.get("risk", ""))).lower()

            if "high" in risk:
                st.warning("High defect risk detected. Recommended action: inspect batch, review machine condition, and validate supplier quality before release.")
            else:
                st.info("Low defect risk. Continue normal production monitoring.")

        else:
            st.error(f"API error: {response.status_code}")
            st.write(response.text)

    except Exception as e:
        st.error("Unable to connect to FastAPI service")
        st.write(e)