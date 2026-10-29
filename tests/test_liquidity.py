import pytest
from src.models.liquidity_stress import liquidity_stress_simulation as simulate


def test_final_partial_payment_and_accounting():
    df = simulate(100, .25, .1, .8)
    assert df.redemption_paid.tolist() == pytest.approx([10, 10, 5])
    assert df.iloc[-1].remaining_assets == pytest.approx(68.75)
    assert df.haircut_loss.sum() == pytest.approx(6.25)
    assert df.redemption_paid.sum() + df.haircut_loss.sum() + df.iloc[-1].remaining_assets == pytest.approx(100)


def test_insolvency_retains_unfunded_requests():
    df = simulate(100, 1, .1, .5)
    assert df.iloc[-1].remaining_assets == 0
    assert df.iloc[-1].withdrawals_left == pytest.approx(50)


def test_zero_requests():
    assert simulate(redemption_request=0).empty


@pytest.mark.parametrize('kwargs', [{'quarterly_limit':0}, {'illiquidity_discount':0}, {'total_assets':-1}, {'redemption_request':1.1}, {'total_assets':float('nan')}])
def test_invalid_inputs(kwargs):
    with pytest.raises(ValueError): simulate(**kwargs)
