# src/data/sec_edgar.py

import requests
import pandas as pd

HEADERS = {
    "User-Agent": "Ajai Quant Research ajai@uva.edu"
}

def get_filing_urls(cik):
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    res = requests.get(url, headers=HEADERS)
    data = res.json()

    filings = data["filings"]["recent"]

    df = pd.DataFrame({
        "form": filings["form"],
        "date": filings["filingDate"],
        "accession": filings["accessionNumber"],
        "primary_doc": filings["primaryDocument"]
    })

    df = df[df["form"].isin(["10-Q", "10-K"])]

    df["url"] = df.apply(
        lambda row: f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{row['accession'].replace('-', '')}/{row['primary_doc']}",
        axis=1
    )

    return df