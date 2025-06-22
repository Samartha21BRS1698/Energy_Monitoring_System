import streamlit as st
import pandas as pd
import plotly.express as px
from simulation import generate_data
import time

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="Home Energy Monitor", layout="centered")
st.title("🔌 Home Energy Monitoring Dashboard (Simulated)")

# -----------------------------
# Define Appliances
# -----------------------------
appliances = ["Fan", "Light", "AC", "Fridge", "TV"]

# -----------------------------
# Appliance Toggle Controls
# -----------------------------
st.sidebar.header("🕹️ Appliance Control Panel")
status_dict = {}
for appliance in appliances:
    status_dict[appliance] = st.sidebar.toggle(f"{appliance}", value=True)

# -----------------------------
# Session State to Store Data
# -----------------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame()

# -----------------------------
# Start Monitoring Simulation
# -----------------------------
if st.button("▶️ Start Monitoring"):
    placeholder = st.empty()
    for _ in range(30):  # simulate 30 seconds
        new_data = pd.DataFrame(generate_data(status_dict))
        st.session_state.data = pd.concat([st.session_state.data, new_data])
        time.sleep(1)
        placeholder.line_chart(
            st.session_state.data.groupby("appliance")["power"].mean()
        )

# -----------------------------
# Display Latest Data Table
# -----------------------------
if not st.session_state.data.empty:
    st.subheader("📊 Latest Appliance Readings")
    st.dataframe(st.session_state.data.tail(10))

    # -------------------------
    # Plot Average Power Usage
    # -------------------------
    avg_power = (
        st.session_state.data.groupby("appliance")["power"]
        .mean()
        .reset_index()
    )
    fig = px.bar(
        avg_power,
        x="appliance",
        y="power",
        color="appliance",
        title="Average Power Usage (W)",
    )
    st.plotly_chart(fig)

    # -------------------------
    # High Usage Alert
    # -------------------------
    threshold = 400  # watts
    high_power = st.session_state.data[
        st.session_state.data["power"] > threshold
    ]
    if not high_power.empty:
        st.warning("⚠️ High power usage detected!")
        st.dataframe(high_power[["appliance", "power", "timestamp"]])

    # -------------------------
    # CSV Export
    # -------------------------
    st.subheader("📥 Download Data as CSV")
    csv = st.session_state.data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📄 Download CSV",
        data=csv,
        file_name="energy_data.csv",
        mime="text/csv"
    )
