from pytorch_forecasting import TimeSeriesDataSet
from pytorch_forecasting.data import GroupNormalizer
from torch.utils.data import DataLoader


def build_tft_datasets(
    train_df,
    val_df,
    config
):
    for df in [train_df, val_df]:
        df["location_id"] = df["location_id"].astype(str)

    max_encoder_length = config["encoder_length"]
    max_prediction_length = config["prediction_length"]

    training = TimeSeriesDataSet(
        train_df,
        time_idx="time_idx",
        target=config["target"],
        group_ids=["location_id"],

        max_encoder_length=max_encoder_length,
        max_prediction_length=max_prediction_length,

        static_categoricals=["location_id"],

        time_varying_known_reals=config["known_reals"],
        time_varying_unknown_reals=config["unknown_reals"],

        target_normalizer=GroupNormalizer(
            groups=["location_id"]
        ),

        add_relative_time_idx=True,
        add_target_scales=True,
        add_encoder_length=True,
    )

    validation = TimeSeriesDataSet.from_dataset(
        training,
        val_df,
        stop_randomization=True
    )

    return training, validation

def build_dataloaders(
    training,
    validation,
    batch_size=64
):

    train_loader = training.to_dataloader(
        train=True,
        batch_size=batch_size,
        num_workers=0
    )

    val_loader = validation.to_dataloader(
        train=False,
        batch_size=batch_size,
        num_workers=0
    )

    return train_loader, val_loader
