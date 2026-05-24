from Logic.Core import Core
from Logic.PreProcessData import PreProcessData
import pandas as pd
import streamlit as st

core = Core()
data_processor = PreProcessData()
data_frame = data_processor.process_data("clean_test_data.csv")
df = data_frame.head(2)
outcome = (core.explain_classification(df))
classif = outcome[0]
explanation = outcome[1]

print("data structure:", outcome)

for item in explanation:
    print(item)


st.title("Network Traffic Anomaly Detection App")
st.write("Upload your network traffic data to detect anomalies using our machine learning model.")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:

    # Load the data
    # data = data_processor.process_data(uploaded_file)

    data_frame = data_processor.process_data("clean_test_data.csv")
    df = data_frame.head(2)
    outcome = (core.explain_classification(df))
    classif = outcome[0]
    explanation = outcome[1]
    st.write("### **Classification Result:**", f":red[{classif}]")
    st.write("### **Explanation for the classification:**")
    st.warning("The following features had the most influence on the classification result:")
    st.write(f"The features **:blue[{explanation[0]}]**, **:blue[{explanation[1]}]**, **:blue[{explanation[2]}]**, **:blue[{explanation[3]}]**, and **:blue[{explanation[4]}]** pushed traffic classification towards being **:red[{classif}]**.\n")