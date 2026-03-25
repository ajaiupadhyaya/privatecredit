import numpy as np
import pandas as pd

def liquidity_stress_simulation(
    total_assets=1_000_000_000,
    redemption_request=0.3,
    quarterly_limit=0.1,
    illiquidity_discount=0.85
):
    remaining_assets = total_assets
    withdrawals = total_assets * redemption_request
    periods = 0
    history = []

    while withdrawals > 0:
        allowed = total_assets * quarterly_limit
        if withdrawals > allowed:
            withdrawals -= allowed
        else:
            withdrawals = 0

        forced_sale = allowed * illiquidity_discount
        remaining_assets -= forced_sale

        history.append({
            "period": periods,
            "remaining_assets": remaining_assets,
            "withdrawals_left": withdrawals
        })
        periods += 1
        if remaining_assets <= 0:
            break

    df = pd.DataFrame(history)
    df.to_csv("data/processed/liquidity_sim.csv", index=False)
    return df