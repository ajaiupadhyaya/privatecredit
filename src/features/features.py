import pandas as pd
from sklearn.preprocessing import StandardScaler

def build_features(fred_file="data/processed/fred_data.csv",
                   bdc_file="data/processed/bdc_prices.csv"):
    fred_df = pd.read_csv(fred_file, index_col="date", parse_dates=True)
    bdc_df = pd.read_csv(bdc_file, index_col="Date", parse_dates=True)

    df = fred_df.join(bdc_df["avg_bdc"].pct_change().rename("bdc_return"), how="inner")
    df = df.dropna()

    # Standardize variables
    scaler = StandardScaler()
    df[["hy_z", "loan_z", "fed_z", "bdc_z"]] = scaler.fit_transform(
        df[["hy_spread", "loan_spread", "fed_funds", "bdc_return"]]
    )
    df.to_csv("data/processed/features.csv")
    return df