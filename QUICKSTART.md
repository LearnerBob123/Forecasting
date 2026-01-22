# Quick Start: Weather-Integrated TFT Model

## ✓ Status: READY TO TRAIN

Your notebook now has:
- ✓ Demand data loaded (4 zones, 300k+ timesteps)
- ✓ Weather data integrated (7 features)
- ✓ Zone-based format applied
- ✓ Missing values handled
- ✓ Datasets created (1.27M training sequences)
- ✓ Data quality checked

## Running the Model

### Step 1: Data Verification ✓
Cells 1-3 already executed successfully:
- **Cell 1**: Loaded all data (demand + actual weather + forecast weather)
- **Cell 2**: Created TimeSeriesDataSet with weather features
- **Cell 3**: Verified data quality (no missing values, correlations shown)

### Step 2: Start Training
Execute cells in order:

1. **Cell 4**: Baseline evaluation
2. **Cell 5**: Initialize TFT model
3. **Cell 6**: Find optimal learning rate (5-15 min)
4. **Cell 7**: Train model (30-60 min on CPU, 5-10 min on GPU)
5. **Cell 8**: Load best model
6. **Cells 9+**: Evaluate, visualize, forecast

### Step 3: Monitor Training
Training will show:
```
Epoch 1/50: loss=123.45, val_loss=120.23
Epoch 2/50: loss=110.34, val_loss=112.45
...
Training stopped early when validation loss stops improving
```

### Step 4: Verify Weather Impact
After training, check:

```python
# Run cell 14 (Feature Importance)
predictions_vs_actuals = best_tft.calculate_prediction_actual_by_variable(...)
best_tft.plot_prediction_actual_by_variable(predictions_vs_actuals)
```

**Look for**: weather features (temperature, humidity, wind_speed) showing up in importance

## What's Different from Before?

### Before (without weather):
- Model: "Last 24h demand → Next 6h demand"
- Limited to pure historical patterns
- Can't account for weather events

### Now (with weather):
- Model: "Last 24h demand + weather → Next 6h demand"
- Uses actual historical weather relationships
- Weather forecast improves future predictions
- Can capture temperature/humidity effects

## Expected Improvements

Based on typical energy demand patterns:
- **Temperature impact**: 10-20% forecast improvement (strongest effect)
- **Humidity impact**: 2-5% improvement
- **Wind/Pressure**: 1-3% improvement

Your actual improvement depends on:
- How weather-sensitive your demand is
- Forecast accuracy of weather data
- Regional climate characteristics

## If You Get Errors

### "NaN values found"
- Data loading issue. Run cell 1 again to re-fill missing weather values

### "CUDA out of memory"
- Reduce batch_size from 64 to 32 in cell 2
- Or use CPU for training

### "No data" or "Shape mismatch"
- Verify weather CSV paths are correct: `../Analysis/weather_actual.csv`
- Check zone_to_district mapping matches your data

## Key Statistics

| Metric | Value |
|--------|-------|
| Total demand observations | 1,278,900 |
| Zones | 4 (TPCODL, TPWODL, TPNODL, TPSOSDL) |
| Time period | 2017-01-01 to 2026-01-17 |
| Weather features | 7 |
| Training sequences | 1,267,864 |
| Encoder length | 96 steps (24 hours) |
| Decoder length | 24 steps (6 hours) |
| Temperature range | -1.4°C to 35.3°C |
| Humidity range | 17% to 100% |

## Next Steps

1. **Train** → Execute cell 7
2. **Evaluate** → Check MAE improvement vs baseline
3. **Visualize** → View predictions (cells 12-14)
4. **Forecast** → Generate 6-hour ahead predictions (cells 17-18)
5. **Interpret** → Analyze attention weights (cell 19)

## Configuration Tips

### For Faster Training (testing):
- Reduce `limit_train_batches=50` to `limit_train_batches=10` in cell 6
- Reduce `max_epochs=50` to `max_epochs=10`
- Skip learning rate finder (comment out cell 5)

### For Better Accuracy (production):
- Increase `hidden_size=16` to `hidden_size=32` or `64`
- Increase `attention_head_size=2` to `attention_head_size=4`
- Reduce `dropout=0.1` to `dropout=0.05`
- Run `n_trials=50` in cell 8 (Optuna hyperparameter search)

### For GPU Training:
- Change `accelerator="cpu"` to `accelerator="gpu"` in cells 5 & 6
- Increase `batch_size=64` to `batch_size=256`
- Increase `num_workers=0` to `num_workers=4`

## Weather Data Sources

When updating weather forecast later:
- Same format as `weather_forecast.csv`
- Columns: `id, district_id, time, prediction_time, temperature, humidity, precipitation, rain, surface_pressure, wind_speed, wind_direction, prediction_type`
- 15-minute intervals
- Latest `prediction_time` will be automatically selected

## Questions?

Refer to:
- `WEATHER_INTEGRATION_SUMMARY.md` - What was added
- `CHANGES_DOCUMENTATION.md` - How it was changed
- Cell comments in notebook - Detailed explanations

---

**Ready?** Start with cell 4 (Baseline) or cell 5 (Initialize Model) now!
