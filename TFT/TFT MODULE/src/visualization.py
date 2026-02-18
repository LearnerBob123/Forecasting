"""
Visualization Module for Demand & Weather Analysis
"""

from pathlib import Path
from typing import Optional, List, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (16, 8)
plt.rcParams["font.size"] = 10


class DataVisualizer:
    def __init__(
        self,
        data: pd.DataFrame,
        output_dir: str = "./Visualizations/"
    ):
        self.data = data.copy()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        if "Timestamp" not in self.data.columns:
            raise ValueError("DataFrame must contain 'Timestamp' column.")

        self.data["Timestamp"] = pd.to_datetime(self.data["Timestamp"])

        print(f"Data loaded: {self.data.shape}")
        print(f"Location IDs: {sorted(self.data['location_id'].unique())}")
        print(
            f"Date range: {self.data['Timestamp'].min()} "
            f"to {self.data['Timestamp'].max()}"
        )

    # ============================================================
    # FILTER
    # ============================================================

    def _filter_data(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        location_ids: Optional[List[int]] = None
    ) -> pd.DataFrame:

        df = self.data.copy()

        if start_date:
            df = df[df["Timestamp"] >= pd.Timestamp(start_date)]

        if end_date:
            df = df[df["Timestamp"] <= pd.Timestamp(end_date)]

        if location_ids:
            df = df[df["location_id"].isin(location_ids)]

        return df

    # ============================================================
    # PLOT 1: DEMAND TIME SERIES
    # ============================================================

    def plot_demand_timeseries(
        self,
        location_ids: Optional[List[int]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        title: str = "Demand Over Time"
    ) -> plt.Figure:

        df = self._filter_data(start_date, end_date, location_ids)

        fig, ax = plt.subplots()

        for loc in sorted(df["location_id"].unique()):
            subset = df[df["location_id"] == loc].sort_values("Timestamp")
            ax.plot(
                subset["Timestamp"],
                subset["demand"],
                label=f"Location {loc}",
                linewidth=1.5
            )

        ax.set_title(title, fontweight="bold")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Demand")
        ax.legend()
        ax.grid(alpha=0.3)

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

    # ============================================================
    # PLOT 2: DEMAND & TEMPERATURE (DUAL AXIS)
    # ============================================================

    def plot_demand_temperature(
        self,
        location_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> plt.Figure:

        df = self._filter_data(start_date, end_date, [location_id])
        df = df.sort_values("Timestamp")

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        ax1.plot(df["Timestamp"], df["demand"], label="Demand")
        ax1.set_ylabel("Demand")

        if "temperature" in df.columns:
            ax2.plot(
                df["Timestamp"],
                df["temperature"],
                linestyle="--",
                alpha=0.7,
                label="Temperature"
            )
            ax2.set_ylabel("Temperature")

        ax1.set_title(f"Demand & Temperature - Location {location_id}")
        ax1.grid(alpha=0.3)

        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

    # ============================================================
    # PLOT 3: CORRELATION MATRIX
    # ============================================================

    def plot_correlation_matrix(
        self,
        location_id: int
    ) -> plt.Figure:

        df = self.data[self.data["location_id"] == location_id]

        cols = ["demand"]
        weather_cols = [
            col for col in df.columns
            if col not in ["Timestamp", "location_id", "zone"]
        ]

        cols.extend(weather_cols)

        corr = df[cols].corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=True,
            ax=ax
        )

        ax.set_title(f"Correlation Matrix - Location {location_id}")
        plt.tight_layout()

        return fig

    # ============================================================
    # SAVE
    # ============================================================

    def save_figure(self, fig: plt.Figure, filename: str) -> str:
        path = self.output_dir / filename
        fig.savefig(path, dpi=300, bbox_inches="tight")
        print(f"Saved: {path}")
        return str(path)
