import pandas as pd


def train_val_split(
    df: pd.DataFrame,
    val_ratio: float = 0.2
):
    """
    Time-based split per location_id.
    """

    train_list = []
    val_list = []

    for loc in df["location_id"].unique():
        subset = df[df["location_id"] == loc].sort_values("time_idx")

        split_point = int(len(subset) * (1 - val_ratio))

        train_list.append(subset.iloc[:split_point])
        val_list.append(subset.iloc[split_point:])

    train_df = pd.concat(train_list)
    val_df = pd.concat(val_list)

    return train_df, val_df
