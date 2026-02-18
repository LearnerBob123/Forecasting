from src.data_loader import load_demand_data, load_weather_data
from src.visualization import DataVisualizer
from src.features import build_features
from src.splits import train_val_split
from src.dataset import build_tft_datasets, build_dataloaders
from src.preprocessing import (
    prepare_demand_dataframe,
    upsample_weather,
    merge_demand_weather,
    clean_dataframe
)
from src.baseline import run_baseline
from src.rate_finder import run_lr_finder
from src.model import build_tft_model
from src.train import train_model
import torch
torch.set_float32_matmul_precision("medium")
import matplotlib
matplotlib.use("Agg")
from src.evaluation import load_model, evaluate_model, plot_actual_vs_predicted
import numpy as np


# -------------------------------
# Configuration (lives here)
# -------------------------------

zone_mapping = {
    'TPCODL Demand': 'TPCODL',
    'TPWODL Demand': 'TPWODL',
    'TPNODL Demand': 'TPNODL',
    'TPSOSDL Demand': 'TPSOSDL',
    'Total Demand (as recorded)': 'TOTAL'
}

zone_to_location_id = {
    'TPCODL': 4,
    'TPWODL': 3,
    'TPNODL': 2,
    'TPSOSDL': 1,
    'TOTAL': 0
}


config = {
    "encoder_length": 168,
    "prediction_length": 120,
    "target": "demand",

# "known_reals": [
#     "time_idx",
#     "hour",
#     "dayofweek",
#     "month",
#     "quarter"
# ],

# "unknown_reals": [
#     "log_demand",
#     "rolling_1h_mean",
#     "rolling_6h_mean",
#     "temperature",
#     "relative_humidity"
# ]

    "known_reals": [
        "time_idx",
        "hour",
        "dayofweek",
        "month",
        "quarter",
        "temperature",
        "relative_humidity",
        "precipitation",
        "wind_speed",
        "surface_pressure"
    ],

    "unknown_reals": [
        "demand",
        "log_demand",
        "rolling_1h_mean",
        "rolling_6h_mean"
    ]
}

config.update({
    "learning_rate": 1e-3,
    "hidden_size": 32,
    "attention_heads": 4,
    "dropout": 0.1,
    "hidden_continuous_size": 16,
    "max_epochs": 2
})

# -------------------------------
# Pipeline
# -------------------------------

demand_df = load_demand_data("data/demand.csv")
weather_df = load_weather_data("data/weather.csv")

# Clip data to after 2023-01-01
demand_df = demand_df[demand_df["Timestamp"] >= "2023-01-01"]
weather_df = weather_df[weather_df["Timestamp"] >= "2023-01-01"]

demand_long = prepare_demand_dataframe(
    demand_df,
    zone_mapping,
    zone_to_location_id
)

weather_15min = upsample_weather(weather_df)

merged_df = merge_demand_weather(demand_long, weather_15min)

final_df = clean_dataframe(merged_df)

# print(final_df.head())
# print(final_df.shape)

# viz = DataVisualizer(final_df)

# fig = viz.plot_demand_timeseries(location_ids=[1, 2, 3])
# viz.save_figure(fig, "demand_timeseries.png")

# fig = viz.plot_demand_temperature(location_id=1)
# viz.save_figure(fig, "demand_temperature_loc1.png")

selected_locations = [0]

feature_df = build_features(
    final_df,
    location_ids=selected_locations
)

# print(feature_df.head())
# print(feature_df.tail())


train_df, val_df = train_val_split(feature_df, val_ratio=0.2)
# val_df = val_df.groupby("location_id").head(10000)
training, validation = build_tft_datasets(train_df, val_df, config)
# print("Columns in train_df:")
# print(train_df.columns)

train_loader, val_loader = build_dataloaders(training, validation)

# -----------------------------------
# 1️⃣ Baseline
# -----------------------------------

baseline_mae = run_baseline(val_loader)
# baseline_mae = 376.0551
# -----------------------------------
# 2️⃣ Build Model
# -----------------------------------

model = build_tft_model(training, config)

# -----------------------------------
# 3️⃣ Learning Rate Finder
# -----------------------------------

# suggested_lr = run_lr_finder(model, train_loader, val_loader)

# if suggested_lr:
#     config["learning_rate"] = suggested_lr

# Rebuild model with new LR
# model = build_tft_model(training, config)

# # -----------------------------------
# # 4️⃣ Train
# # -----------------------------------

trainer, best_model_path = train_model(
    model,
    train_loader,
    val_loader,
    config
)

# ------------------------------------
# Load Best Model
# ------------------------------------
# checkpoint_path = "checkpoints/tft-best.ckpt" # replace with actual path
# model = load_model(checkpoint_path)

# print("Model loaded.")

# model = model.cpu()
# torch.cuda.empty_cache()

# print("Moved model to CPU for inference.")


# print("\n==============================")
# print("Model loaded successfully!")
# print(f"Checkpoint path: {checkpoint_path}")
# print(f"Model class: {type(model).__name__}")
# print(f"Device: {next(model.parameters()).device}")
# print(f"Total parameters: {sum(p.numel() for p in model.parameters()):,}")
# print("==============================\n")

# # ------------------------------------
# # Evaluate
# # ------------------------------------

# timestamps, actuals, predictions = evaluate_model(
#     model,
#     val_loader,
#     feature_df
# )
# print("\nEvaluation complete.")
# print(f"Total prediction points: {len(actuals)}")

# mae = np.mean(np.abs(np.array(actuals) - np.array(predictions)))
# print(f"Validation MAE: {mae:.4f}")
# print("Sample actuals:", actuals[:5])
# print("Sample predictions:", predictions[:5])
# print()

# # ------------------------------------
# # Plot
# # ------------------------------------

# # plot_actual_vs_predicted(
# #     timestamps,
# #     actuals,
# #     predictions
# # )

# # ---- Select a slice ----
# slice_start = 0
# slice_length = 3000  # change this as needed

# slice_end = slice_start + slice_length

# slice_timestamps = timestamps[slice_start:slice_end]
# slice_actuals = actuals[slice_start:slice_end]
# slice_predictions = predictions[slice_start:slice_end]

# print(f"Plotting slice from index {slice_start} to {slice_end}")

# plot_actual_vs_predicted(
#     slice_timestamps,
#     slice_actuals,
#     slice_predictions
# )
