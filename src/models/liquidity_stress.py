"""Deterministic redemption mechanics; amounts share the input asset unit."""
import math
from pathlib import Path
import pandas as pd


def liquidity_stress_simulation(total_assets=1_000_000_000, redemption_request=0.3,
                                quarterly_limit=0.1, illiquidity_discount=0.85,
                                output_path=None):
    """Gate is a fraction of initial NAV. Sale proceeds fund redemptions.

    illiquidity_discount is the fraction of book value realized (0.85 = 15%
    haircut). No income, borrowing, new requests, or price recovery is assumed.
    Unfunded requests remain outstanding after assets are exhausted.
    """
    values = (total_assets, redemption_request, quarterly_limit, illiquidity_discount)
    if not all(math.isfinite(x) for x in values):
        raise ValueError('Inputs must be finite')
    if total_assets <= 0 or not 0 <= redemption_request <= 1:
        raise ValueError('Positive assets and redemption fraction in [0, 1] required')
    if not 0 < quarterly_limit <= 1 or not 0 < illiquidity_discount <= 1:
        raise ValueError('Gate and sale-price fraction must be in (0, 1]')
    assets, pending = total_assets, total_assets * redemption_request
    history = []
    while pending > total_assets * 1e-12 and assets > total_assets * 1e-12:
        paid = min(pending, total_assets * quarterly_limit, assets * illiquidity_discount)
        sold = paid / illiquidity_discount
        assets = max(0.0, assets - sold)
        pending = max(0.0, pending - paid)
        history.append(dict(period=len(history) + 1, remaining_assets=assets,
                            withdrawals_left=pending, redemption_paid=paid,
                            assets_sold=sold, haircut_loss=sold-paid))
    df = pd.DataFrame(history, columns=['period', 'remaining_assets', 'withdrawals_left',
                                       'redemption_paid', 'assets_sold', 'haircut_loss'])
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
    return df
