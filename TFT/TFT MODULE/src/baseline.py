import torch
from pytorch_forecasting.models import Baseline


def run_baseline(val_loader):
    actuals = torch.cat([y[0] for x, y in val_loader])
    baseline_predictions = Baseline().predict(val_loader)

    mae = (actuals - baseline_predictions).abs().mean()

    print(f"\nBaseline MAE: {mae.item():.4f}\n")

    return mae.item()
