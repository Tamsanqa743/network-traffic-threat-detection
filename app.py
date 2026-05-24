from Logic.Core import Core
from Logic.PreProcessData import PreProcessData

core = Core()
data_processor = PreProcessData()
data_frame = data_processor.process_data("clean_test_data.csv")
df = data_frame.head(2)
outcome = (core.explain_classification(df))
for item in outcome:
    print(item)