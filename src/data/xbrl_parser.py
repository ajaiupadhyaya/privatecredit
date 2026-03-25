import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Ajai Quant Research ajai@uva.edu"
}

def extract_basic_metrics(filing_url):
    res = requests.get(filing_url, headers=HEADERS)

    soup = BeautifulSoup(res.content, "lxml")

    text = soup.get_text()

    # crude but effective fallback parsing
    nav = None
    non_accrual = None

    for line in text.split("\n"):
        if "Net Asset Value" in line:
            nav = line.strip()

        if "non-accrual" in line.lower():
            non_accrual = line.strip()

    return {
        "nav_raw": nav,
        "non_accrual_raw": non_accrual
    }