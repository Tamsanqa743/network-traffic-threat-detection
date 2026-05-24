import pandas as pd
import numpy as np
import joblib, os
from pathlib import Path
import shap
from .DetectionLogger import DetectionLogger

class Core:

    def __init__(self):
        
        # exported models file names from training
        self.parent_path = Path(__file__).parent/'..'
        self.model_filepath = self.parent_path/'Models/rf_model.pkl'
        self.tree_explainer_filepath = self.parent_path/'Models/tree_explainer.pkl'


        # load random forest trained model from file
        self.trained_rf_model = joblib.load(self.model_filepath)

        # load tree explainer from file
        self.tree_explainer = joblib.load(self.tree_explainer_filepath)

        # detections logger
        self.logger = DetectionLogger()

        # classification text description
        self.descriptive_classification = {1: 'Malicious', 0: 'Normal'}



    def explain_classification(self, input_data_frame_x):
        df_shap_values = self.tree_explainer.shap_values(input_data_frame_x) # extract shap values from current data frame
        shap_values_class_1 = df_shap_values[:, :, 1] # sort shap values in descending order

        top_5_features = (
        pd.Series(np.abs(shap_values_class_1).mean(axis=0), index=input_data_frame_x.columns)
        .sort_values(ascending=False)
        .head(5)
        )

        # make classification
        classification = self.trained_rf_model.predict(input_data_frame_x)[0] # store classification as integer
        print('classifiication:', classification)
        self.classify_traffic(input_data_frame_x)

    #     shap.summary_plot(
    #     shap_values_class_1,
    #     input_data_frame_x,
    #     plot_type="bar",
    #     max_display=5,
    #     show=True,
    # )


    def classify_traffic(self, input_data_frame):
        '''classify traffic'''
        classification = self.trained_rf_model.predict(input_data_frame)[0] # return classification as integer
        self.logger.write_log("Network Activity Classification: " + self.descriptive_classification[classification])
        return classification
