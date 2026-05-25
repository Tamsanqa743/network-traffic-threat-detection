from Logic.Core import Core
from Logic.PreProcessData import PreProcessData
import pandas as pd
import streamlit as st

core = Core()
data_processor = PreProcessData()

st.title("Network Traffic Anomaly Detection App")
st.write("Upload your network traffic data to detect anomalies using our machine learning model.")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:

    data_frame, log_id = data_processor.process_data(uploaded_file)
    outcome = (core.explain_classification(data_frame, log_id))
    classif = outcome[0]
    explanation = outcome[1]
    st.write("### **Classification Result:**", f":red[{classif}]")
    st.write("### **Explanation for the classification:**")
    st.warning("The following features had the most influence on the classification result:")
    st.write(f"The features **:blue[{explanation[0]}]**, **:blue[{explanation[1]}]**, **:blue[{explanation[2]}]**, **:blue[{explanation[3]}]**, and **:blue[{explanation[4]}]** pushed traffic classification towards being **:red[{classif}]**.\n")