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


# st.title("Network Traffic Anomaly Detection App")
# st.write("Upload your network traffic data to detect anomalies using our machine learning model.")
# uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
# if uploaded_file is not None:
#     # from sklearn.ensemble import IsolationForest

#     # Load the data
#     data = data_processor.process_data(uploaded_file)

#     data_frame = data_processor.process_data("clean_test_data.csv")
#     df = data_frame.head(2)
#     outcome = (core.explain_classification(df))
#     classif = outcome[0]
#     explanation = outcome[1]

#     for item in explanation:
#         print(item)

#     # Preprocess the data (this is a placeholder, you should implement your own preprocessing)
#     # For example, you might want to select specific features or handle missing values
#     # data = preprocess_data(data)

#     st.write("Anomaly Detection Results will be displayed here after processing the data.")
#     # st.dataframe(data[['anomaly']])