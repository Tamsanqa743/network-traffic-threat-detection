import pandas as pd
import numpy as np
import pickle, os
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
        with open(self.model_filepath, "rb") as f:
            self.trained_rf_model = pickle.load(f)
        # self.trained_rf_model = pickle.load(self.model_filepath)

        # load tree explainer from file
        # self.tree_explainer = pickle.load(self.tree_explainer_filepath)
        with open(self.tree_explainer_filepath, "rb") as f:
            self.tree_explainer = pickle.load(f)

        # detections logger
        self.logger = DetectionLogger()

        # classification text description
        self.descriptive_classification = {1: 'Malicious', 0: 'Normal'}

        self.user_friendly_category_names = {
            'num__sport': 'source port',
            'num__dsport': 'destination port',
            'num__dur': 'duration',
            'num__sbytes': 'source bytes',
            'num__dbytes': 'destination bytes',
            'num__sttl': 'source time to live',
            'num__Spkts': 'source packets',
            'num__Dpkts': 'destination packets',
            'num__swin': 'source tcp window',
            'num__stcpb': 'source tcp base sequence number',
            'num__dtcpb': 'destination tcp base sequence number',
            'num__smeansz': 'source mean packet size',
            'num__dmeansz': 'destination mean packet size',
            'cat__proto_ICMP': 'protocol icmp',
            'cat__proto_IGMP': 'protocol igmp',
            'cat__proto_IPv6-ICMP': 'protocol ipv6 icmp',
            'cat__proto_TCP': 'protocol tcp',
            'cat__proto_UDP': 'protocol udp',
            'cat__proto_unknown': 'protocol unknown',
            'cat__state_closed': 'connection state closed',
            'cat__state_established': 'connection state established',
            'cat__state_new': 'connection state new',
            'cat__state_unknown': 'connection state unknown',
            'cat__service_dhcp': 'service dhcp',
            'cat__service_dns': 'service dns',
            'cat__service_failed': 'service failed',
            'cat__service_ftp': 'service ftp',
            'cat__service_http': 'service http',
            'cat__service_ntp': 'service ntp',
            'cat__service_rfb': 'service rfb',
            'cat__service_smb': 'service smb',
            'cat__service_smtp': 'service smtp',
            'cat__service_ssh': 'service ssh',
            'cat__service_telnet': 'service telnet',
            'cat__service_tls': 'service tls',
            'cat__service_unknown': 'service unknown',
            'cat__ct_state_ttl_close_wait': 'connection state ttl close wait',
            'cat__ct_state_ttl_closed': 'connection state ttl closed',
            'cat__ct_state_ttl_established': 'connection state ttl established',
            'cat__ct_state_ttl_fin_wait2': 'connection state ttl fin wait2',
            'cat__ct_state_ttl_syn_sent': 'connection state ttl syn sent',
            'cat__ct_state_ttl_unknown': 'connection state ttl unknown'
        }



    def explain_classification(self, input_data_frame_x):
        df_shap_values = self.tree_explainer.shap_values(input_data_frame_x) # extract shap values from current data frame
        shap_values_class_1 = df_shap_values[:, :, 1] # sort shap values in descending order

        top_5_features = (
        pd.Series(np.abs(shap_values_class_1).mean(axis=0), index=input_data_frame_x.columns)
        .sort_values(ascending=False)
        .head(5)
        )

        # call classify traffic function
        classification = self.classify_traffic(input_data_frame_x) # I am only calling this function to test the prediction logger class

        explanation = []

        # feature indices
        indices = top_5_features.index
        for index in indices:
            explanation.append(self.user_friendly_category_names[index])

        return self.descriptive_classification[classification], explanation


    # calling this function will depend on how your frontend handles the data. It may not be needed as you can make a prediction directly inside the above function
    def classify_traffic(self, input_data_frame):
        '''classify traffic'''
        classification = self.trained_rf_model.predict(input_data_frame)[0] # return classification as integer
        self.logger.write_log("Network Activity Classification: " + self.descriptive_classification[classification])
        return classification
