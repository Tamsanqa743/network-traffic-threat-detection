import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

class PreProcessData:

    def __init__(self):

        self.CAT_COLS = ["proto", "state", "service", "ct_state_ttl"]
        self.NUM_COLS = [
        "sport", "dsport", "dur", "sbytes", "dbytes", "sttl",
        "Spkts", "Dpkts", "swin", "stcpb", "dtcpb", "smeansz", "dmeansz",
        ]

        self.PROTO_MAP = {
            "6": "TCP", "6.0": "TCP", "TCP": "TCP",
            "17": "UDP", "17.0": "UDP", "UDP": "UDP",
            "1": "ICMP", "1.0": "ICMP", "ICMP": "ICMP",
            "58": "IPv6-ICMP", "58.0": "IPv6-ICMP", "IPv6-ICMP": "IPv6-ICMP",
            "2": "IGMP", "2.0": "IGMP",
            "0": "unknown", "0.0": "unknown",
        }

        

    def normalize_proto(self, val):
        s = str(val).strip()
        if s.endswith(".0"):
            s = s[:-2]
        if "," in s:
            return "unknown"
        return self.PROTO_MAP.get(s, "unknown")
    

    def process_data(self, filename):

        '''preprocess csv data: assumption ==> data is already cleaned'''
        network_data = pd.read_csv(filename)
        return network_data # return data frame




    def clean_data(self, network_data):
        #  drop all rows with any null columns

        network_data.dropna()

        # 1. Remove duplicates
        network_data_clean = network_data.drop_duplicates()


        # 2. drop rows where trans_depth/res_bdy_len contain HTTP junk (GET, /paths)
        bad_rows = (
            pd.to_numeric(network_data_clean["trans_depth"], errors="coerce").isna() & network_data_clean["trans_depth"].notna()
        ) | (
            pd.to_numeric(network_data_clean["res_bdy_len"], errors="coerce").isna() & network_data_clean["res_bdy_len"].notna()
        )
        print(f"Dropping {bad_rows.sum():,} corrupted rows")
        network_data_clean = network_data_clean[~bad_rows]

        network_data_clean.drop(columns=self.DROP_COLS, inplace=True)
        
        network_data_clean["proto"] = network_data_clean["proto"].map(self.normalize_proto)
        # --- state, service, ct_state_ttl: 0 -> unknown ---
        for col in ["state", "service", "ct_state_ttl"]:
            network_data_clean[col] = (
                network_data_clean[col]
                .astype(str)
                .replace({"0": "unknown", "0.0": "unknown", "nan": "unknown"})
            )
        # --- numeric columns ---
        for col in self.NUM_COLS:
            network_data_clean[col] = pd.to_numeric(network_data_clean[col], errors="coerce")

        encoder = ColumnTransformer(
            transformers=[
            ("num", "passthrough", self.NUM_COLS),
            ("cat", OneHotEncoder(handle_unknown="ignore"), self.CAT_COLS),
            ]
        )

        data_frame = encoder.transform(data_frame)
        feature_names = encoder.get_feature_names_out()