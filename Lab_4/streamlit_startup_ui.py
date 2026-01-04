import streamlit as st
import joblib
import numpy as np
import os
import pickle

st.set_page_config(page_title="Startup Profit Predictor", layout="centered")
st.title("📊 Startup Profit Predictor")

MODEL_PATH = "model1.pkl"

# ---------------------------
# Load Model
# ---------------------------
@st.cache_resource
def load_model(path):
    try:
        return joblib.load(path)
    except:
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except:
            return None

model = None
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
    if model:
        st.success("Model loaded successfully (model1.pkl)")
    else:
        st.error("model1.pkl found but could not be loaded")

uploaded_model = st.file_uploader("Upload model1.pkl", type=["pkl", "joblib"])
if uploaded_model is not None:
    model = load_model(uploaded_model)
    if model:
        st.success("Model uploaded successfully")
    else:
        st.error("Invalid model file")

st.markdown("---")
st.subheader("Enter Startup Details")

# ---------------------------
# Input Fields
# ---------------------------
rd_spend = st.number_input("R&D Spend", min_value=0.0, value=100000.0)
admin_spend = st.number_input("Administration Spend", min_value=0.0, value=50000.0)
marketing_spend = st.number_input("Marketing Spend", min_value=0.0, value=80000.0)

state = st.selectbox("State", ["California", "Florida", "New York"])

# Encode State
state_florida = 1 if state == "Florida" else 0
state_newyork = 1 if state == "New York" else 0

# ---------------------------
# Prediction
# ---------------------------
if st.button("Predict Profit"):
    if model is None:
        st.error("❌ No model loaded")
    else:
        X = np.array([[rd_spend, admin_spend, marketing_spend,
                       state_florida, state_newyork]])

        try:
            prediction = model.predict(X)[0]
            st.success(f"💰 Predicted Profit: **₹ {prediction:,.2f}**")
        except Exception as e:
            st.error(f"Prediction failed: {e}")

st.markdown("---")
st.caption("Model expects features in order: R&D Spend, Administration, Marketing Spend, State_Florida, State_New York")
