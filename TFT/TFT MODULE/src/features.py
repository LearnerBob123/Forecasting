import pandas as pd
import numpy as np


# ============================================================
# 1️⃣ Data Subsetting
# ============================================================

def subset_data(
    df: pd.DataFrame,
    location_ids: list
) -> pd.DataFrame:

    df = df[df["location_id"].isin(location_ids)].copy()

    if df.empty:
        raise ValueError("No data after filtering location_ids.")

    return df


# ============================================================
# 2️⃣ Time Index & Calendar Features
# ============================================================

def add_time_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.sort_values(["location_id", "Timestamp"]).copy()

    # Sequential index per location
    df["time_idx"] = (
        df.groupby("location_id")
        .cumcount()
    )

    df["hour"] = df["Timestamp"].dt.hour
    df["dayofweek"] = df["Timestamp"].dt.dayofweek
    df["month"] = df["Timestamp"].dt.month
    df["quarter"] = df["Timestamp"].dt.quarter

    return df


# ============================================================
# 3️⃣ Seasonal Statistics
# ============================================================

def add_seasonal_stats(df: pd.DataFrame) -> pd.DataFrame:

    grouped = (
        df.groupby(["location_id", "hour"])["demand"]
        .agg(["mean", "std"])
        .reset_index()
        .rename(columns={
            "mean": "hour_mean_demand",
            "std": "hour_std_demand"
        })
    )

    df = df.merge(
        grouped,
        on=["location_id", "hour"],
        how="left"
    )

    return df


# ============================================================
# 4️⃣ Rolling Windows
# ============================================================

def add_rolling_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.sort_values(["location_id", "Timestamp"]).copy()

    # 1 hour rolling (4 steps for 15min)
    df["rolling_1h_mean"] = (
        df.groupby("location_id")["demand"]
        .transform(lambda x: x.rolling(window=4).mean())
    )

    # 6 hour rolling (24 steps)
    df["rolling_6h_mean"] = (
        df.groupby("location_id")["demand"]
        .transform(lambda x: x.rolling(window=24).mean())
    )

    return df


# ============================================================
# 5️⃣ Log Transform
# ============================================================

def add_log_transform(df: pd.DataFrame) -> pd.DataFrame:

    df["log_demand"] = np.log1p(df["demand"])
    return df


# ============================================================
# 6️⃣ Data Health Check
# ============================================================

def validate_features(df: pd.DataFrame) -> None:

    print("\n===== DATA HEALTH CHECK =====")
    print("Shape:", df.shape)
    print("Location IDs:", df["location_id"].unique())
    print("NaN counts:\n", df.isna().sum())
    print("=============================\n")


# ============================================================
# 7️⃣ Full Feature Pipeline
# ============================================================

def build_features(
    df: pd.DataFrame,
    location_ids: list
) -> pd.DataFrame:

    df = subset_data(df, location_ids)
    df = add_time_features(df)
    df = add_seasonal_stats(df)
    df = add_rolling_features(df)
    df = add_log_transform(df)

    df["rolling_1h_mean"] = (
    df.groupby("location_id")["rolling_1h_mean"]
    .transform(lambda x: x.fillna(method="bfill"))
    )

    df["rolling_6h_mean"] = (
        df.groupby("location_id")["rolling_6h_mean"]
        .transform(lambda x: x.fillna(method="bfill"))
    )

    validate_features(df)

    return df
