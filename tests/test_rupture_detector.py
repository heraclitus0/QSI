import pandas as pd
import numpy as np
import pytest
from rupture import generate_dummy, compute_drift_thresholds, compute_ewma_threshold

#  Dummy Data Tests
def test_generate_dummy_valid_schema():
    df = generate_dummy(days=30)
    assert df.shape[0] == 30
    assert set(df.columns) == {"Date", "Forecast", "Actual", "Unit_Cost"}

def test_generate_dummy_non_negative_actual():
    df = generate_dummy(days=50)
    assert (df["Actual"] >= 0).all()

#  Drift Threshold Tests
def test_drift_threshold_no_drift():
    df = pd.DataFrame({
        "Date": pd.date_range(end=pd.Timestamp.today(), periods=10),
        "Forecast": np.full(10, 1000),
        "Actual": np.full(10, 1000),
        "Unit_Cost": np.full(10, 40)
    })
    df_out, ruptures, total_loss = compute_drift_thresholds(df, c=0.1, a=0.1, base_threshold=50, noise_level=10)
    assert ruptures.empty
    assert total_loss == 0

def test_drift_threshold_high_drift_trigger():
    df = pd.DataFrame({
        "Date": pd.date_range(end=pd.Timestamp.today(), periods=5),
        "Forecast": [1000]*5,
        "Actual": [1000, 1200, 1000, 1300, 1000],
        "Unit_Cost": [40]*5
    })
    df_out, ruptures, total_loss = compute_drift_thresholds(df, c=0.1, a=0.1, base_threshold=50, noise_level=0)
    assert (ruptures["Rupture"] == True).sum() >= 2
    assert total_loss > 0

#  EWMA Threshold Tests
def test_ewma_threshold_exists():
    df = generate_dummy(days=20)
    df_drift, _, _ = compute_drift_thresholds(df, c=0.1, a=0.1, base_threshold=50, noise_level=5)
    df_final = compute_ewma_threshold(df_drift, alpha=0.2, k=3)
    assert "Threshold_EWMA" in df_final.columns

def test_ewma_threshold_alpha_sensitivity():
    df = generate_dummy(days=50)
    df_drift, _, _ = compute_drift_thresholds(df, c=0.1, a=0.1, base_threshold=50, noise_level=5)
    df_ewma_low_alpha = compute_ewma_threshold(df_drift, alpha=0.1, k=3)
    df_ewma_high_alpha = compute_ewma_threshold(df_drift, alpha=0.4, k=3)
    assert df_ewma_high_alpha["Threshold_EWMA"].iloc[-1] != df_ewma_low_alpha["Threshold_EWMA"].iloc[-1]

#  Edge Case Test
def test_invalid_input_handling():
    df = pd.DataFrame({
        "Date": pd.date_range(end=pd.Timestamp.today(), periods=10),
        "Forecast": np.full(10, 1000),
        # 'Actual' column intentionally omitted
        "Unit_Cost": np.full(10, 40)
    })
    with pytest.raises(Exception):
        compute_drift_thresholds(df, c=0.1, a=0.1, base_threshold=50, noise_level=5)
