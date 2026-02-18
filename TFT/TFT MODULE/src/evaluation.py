import torch
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pytorch_forecasting import TemporalFusionTransformer


def load_model(checkpoint_path: str):
    model = TemporalFusionTransformer.load_from_checkpoint(checkpoint_path)
    model.eval()
    return model


def evaluate_model(model, val_loader, feature_df):

    # Predict
    raw_predictions, x, *_ = model.predict(
        val_loader,
        return_x=True,
        mode="raw",
        trainer_kwargs=dict(accelerator="cpu")
    )

    # Median quantile (0.5)
    predictions = raw_predictions["prediction"][:, :, 1]

    # Decoder time indices
    decoder_time_idx = x["decoder_time_idx"]

    # Actual decoder targets (correct alignment)
    actuals = x["decoder_target"]

    # Flatten everything
    predictions = predictions.reshape(-1).cpu().numpy()
    actuals = actuals.reshape(-1).cpu().numpy()
    decoder_time_idx = decoder_time_idx.reshape(-1).cpu().numpy()

    # Build evaluation dataframe
    df_eval = pd.DataFrame({
        "time_idx": decoder_time_idx,
        "Actual": actuals,
        "Predicted": predictions
    })

    # Aggregate duplicates (mean per timestamp)
    df_eval = df_eval.groupby("time_idx").mean().reset_index()

    # Map time_idx to Timestamp
    time_mapping = (
        feature_df[["time_idx", "Timestamp"]]
        .drop_duplicates()
        .set_index("time_idx")
    )

    df_eval["Timestamp"] = time_mapping.loc[df_eval["time_idx"]]["Timestamp"].values

    # Compute MAE
    mae = np.mean(np.abs(df_eval["Actual"] - df_eval["Predicted"]))
    print(f"\nTFT MAE (deduplicated): {mae:.4f}\n")

    return (
        df_eval["Timestamp"].values,
        df_eval["Actual"].values,
        df_eval["Predicted"].values
    )



def plot_actual_vs_predicted(
    timestamps,
    actual,
    predicted,
    title="Actual vs Predicted Demand"
):

    df = pd.DataFrame({
        "Timestamp": timestamps,
        "Actual": actual,
        "Predicted": predicted
    })

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Timestamp"],
            y=df["Actual"],
            mode="lines",
            name="Actual"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Timestamp"],
            y=df["Predicted"],
            mode="lines",
            name="Predicted"
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Demand",
        template="plotly_white"
    )

    fig.show()

    return fig
