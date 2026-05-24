from Logic.Core import Core
import pandas as pd

core = Core()

data_frame =pd.read_csv("clean_test_data.csv")
df = data_frame.head(1)
core.explain_classification(df)