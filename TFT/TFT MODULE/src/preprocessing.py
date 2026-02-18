import pandas as pd


# --------------------------------------------------
# 1️⃣ Zone → Location Mapping
# --------------------------------------------------

def prepare_demand_dataframe(
    demand_df: pd.DataFrame,
    zone_mapping: dict,
    zone_to_location_id: dict
) -> pd.DataFrame:

    demand_df = demand_df.copy()
    demand_df["Timestamp"] = pd.to_datetime(demand_df["Timestamp"])

    # Rename columns based on mapping
    demand_df = demand_df.rename(columns=zone_mapping)

    value_columns = list(zone_mapping.values())

    demand_long = demand_df.melt(
        id_vars=["Timestamp"],
        value_vars=value_columns,
        var_name="zone",
        value_name="demand"
    )

    demand_long["location_id"] = demand_long["zone"].map(zone_to_location_id)

    if demand_long["location_id"].isnull().any():
        missing = demand_long[demand_long["location_id"].isnull()]["zone"].unique()
        raise ValueError(f"Unmapped zones found: {missing}")

    demand_long = demand_long.sort_values(["location_id", "Timestamp"])

    return demand_long


def map_zone_to_location(
    demand_df: pd.DataFrame,
    zone_mapping: dict
) -> pd.DataFrame:

    demand_df = demand_df.copy()

    demand_df["Timestamp"] = pd.to_datetime(demand_df["Timestamp"])
    demand_df = demand_df.sort_values(["zone", "Timestamp"])

    demand_df["location_id"] = demand_df["zone"].map(zone_mapping)

    if demand_df["location_id"].isnull().any():
        missing = demand_df[demand_df["location_id"].isnull()]["zone"].unique()
        raise ValueError(f"Unmapped zones found: {missing}")

    return demand_df


# --------------------------------------------------
# 2️⃣ Upsample Weather (Hourly → 15 min)
# --------------------------------------------------
def upsample_weather(weather_df: pd.DataFrame) -> pd.DataFrame:

    weather_df = weather_df.copy()

    weather_df["Timestamp"] = pd.to_datetime(weather_df["Timestamp"])
    weather_df = weather_df.sort_values(["location_id", "Timestamp"])

    weather_15min = (
        weather_df
        .set_index("Timestamp")
        .groupby("location_id", group_keys=False)
        .resample("15min")
        .interpolate(method="linear")
        .reset_index()
    )

    return weather_15min


# --------------------------------------------------
# 3️⃣ Merge Demand + Weather
# --------------------------------------------------
def merge_demand_weather(
    demand_df: pd.DataFrame,
    weather_df: pd.DataFrame
) -> pd.DataFrame:

    merged_df = pd.merge(
        demand_df,
        weather_df,
        on=["Timestamp", "location_id"],
        how="left"
    )

    return merged_df


# --------------------------------------------------
# 4️⃣ Clean Final DataFrame
# --------------------------------------------------
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    df = df.sort_values(["location_id", "Timestamp"])

    # Drop rows with missing values after merge
    df = df.dropna()

    df = df.reset_index(drop=True)

    return df


# --------------------------------------------------
# 5️⃣ Full Processing Pipeline Function
# --------------------------------------------------
def process_data(
    demand_df: pd.DataFrame,
    weather_df: pd.DataFrame,
    zone_mapping: dict
) -> pd.DataFrame:

    demand_df = map_zone_to_location(demand_df, zone_mapping)
    weather_15min = upsample_weather(weather_df)
    merged_df = merge_demand_weather(demand_df, weather_15min)
    final_df = clean_dataframe(merged_df)

    return final_df
