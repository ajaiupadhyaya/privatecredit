import pandas as pd

def compute_fragility_index(features_file="data/processed/features.csv"):
    df = pd.read_csv(features_file, index_col="date", parse_dates=True)

    # Composite fragility index with weighted components
    df["fragility_index"] = 0.35*df["bdc_z"] + 0.35*df["hy_z"] + 0.2*df["loan_z"] + 0.1*df["fed_z"]

    # Optional: rolling z-score smoothing
    df["fragility_index_smooth"] = df["fragility_index"].rolling(window=21).mean()
    df.to_csv("data/processed/fragility_index.csv")
    return df