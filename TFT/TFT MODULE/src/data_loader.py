import pandas as pd
from pathlib import Path


def load_demand_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, dayfirst=True)

    # Basic validation
    required_cols = ['Timestamp','TPCODL Demand','TPWODL Demand','TPNODL Demand','TPSOSDL Demand','Total Demand (as recorded)']
    _validate_columns(df, required_cols)

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = df.sort_values("Timestamp")

    return df

def load_weather_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    required_cols = ['location_id','Timestamp','temperature','relative_humidity','precipitation','wind_speed','surface_pressure']

    _validate_columns(df, required_cols)

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = df.sort_values("Timestamp")

    return df


def map_zones_to_locations(demand_df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    demand_df["location_id"] = demand_df["zone"].map(mapping)

    if demand_df["location_id"].isnull().any():
        raise ValueError("Some zones do not have mapping!")

    return demand_df


def _validate_columns(df: pd.DataFrame, required_cols: list):
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")