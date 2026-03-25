from sec_api import QueryApi, XbrlApi
import os

queryApi = QueryApi(api_key=os.getenv("SEC_API_KEY"))
xbrlApi = XbrlApi(api_key=os.getenv("SEC_API_KEY"))

def get_xbrl_data(ticker="ARCC"):
    query = {
        "query": f"ticker:{ticker} AND formType:(10-Q OR 10-K)",
        "from": "0",
        "size": "20",
        "sort": [{ "filedAt": { "order": "desc" } }]
    }

    filings = queryApi.get_filings(query)

    data = []

    for f in filings["filings"]:
        xbrl = xbrlApi.xbrl_to_json(htm_url=f["linkToFilingDetails"])

        try:
            nav = xbrl["StatementsOfAssetsAndLiabilities"]["NetAssetValue"]
            non_accrual = xbrl["Notes"]["NonAccrualLoans"]
            
            data.append({
                "date": f["filedAt"],
                "nav": nav,
                "non_accrual": non_accrual
            })

        except:
            continue

    return data