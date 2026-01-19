# Weather-Demand Change Analysis: Complete Methodology Guide

## Problem Statement
Simple correlation between weather and demand data shows weak relationships, but there's a strong theoretical belief that sudden demand pattern changes are influenced by weather changes. This analysis uses multiple statistical and machine learning approaches to uncover hidden weather-demand relationships.

---

## Six Core Analytical Approaches Implemented

### 1. FIRST DIFFERENCES & ROLLING WINDOW CHANGES ✓
**Concept**: Convert absolute values into rate-of-change metrics
```
Demand_Change = Current_Demand - Previous_Demand
Weather_Change = Current_Weather - Previous_Weather
```

**Why It Works**:
- Raw weather values (e.g., 25°C) don't directly correlate with demand
- But CHANGES in weather (temp increases by 5°C) trigger demand adjustments
- Removes long-term trends that mask short-term relationships

**Parameters Used**:
- Window sizes: 1-hour and 3-hour changes
- Fills missing values with 0

**Output**: Time series of instantaneous and rolling changes

---

### 2. LEAD-LAG CORRELATION ANALYSIS ✓
**Concept**: Test if weather changes at time t correlate with demand changes at time t+lag
```
For lag in [-12h to +12h]:
    Correlation = corr(Weather_t, Demand_t+lag)
```

**Why It Works**:
- Weather may influence demand with a time delay
- Positive lag: weather leads (causes) demand change
- Negative lag: demand leads (anticipates) weather change

**Findings** (4,375 hourly points analyzed):
| Feature | Max Correlation | Lag | Interpretation |
|---------|-----------------|-----|-----------------|
| Humidity | 0.356 | 0h | Simultaneous relationship |
| Precipitation | 0.334 | -9h | Demand leads precipitation |
| Wind Speed | 0.281 | -1h | Demand leads wind speed |
| Temperature | 0.133 | -10h | Demand leads temperature |

**Key Insight**: Humidity has the strongest simultaneous relationship, while other features show anticipatory demand responses.

---

### 3. CHANGE POINT DETECTION & CO-OCCURRENCE ANALYSIS ✓
**Concept**: Identify sudden changes in time series and measure overlap
```
Threshold = Mean ± 1.5 * RollingStdDev
Changepoint_i = |Change_i - RollingMean_i| > Threshold
CoOccurrence = % of demand changes where weather also changes
```

**Why It Works**:
- Focuses on significant shifts, not noise
- High co-occurrence suggests shared drivers
- Rolling statistics adapt to local variability

**Findings**:
- Demand changes detected: 500 events (11.43% of time)
- Co-occurrence with weather:
  - **Humidity: 32.4%** ⭐ Highest synchronization
  - **Temperature: 27.2%**
  - **Wind Speed: 21.4%**
  - **Precipitation: 13.0%**

**Interpretation**: When demand jumps unexpectedly, humidity is most likely to jump simultaneously. This suggests a **common forcing mechanism** (perhaps seasonality or synoptic weather patterns).

---

### 4. DISTRICT-SPECIFIC CHANGE CORRELATION ✓
**Concept**: Calculate change correlations for each geographic region separately
```
For each district:
    Weather_Change = Weather_t - Weather_t-1
    Demand_Change = Demand_t - Demand_t-1
    Correlation = corr(Weather_Change, Demand_Change)
```

**Why It Works**:
- Different regions have different infrastructure and climates
- Coastal areas may respond differently to wind than inland areas
- Aggregate analysis hides regional patterns

**Top Findings** (30 districts analyzed):

**Strongest Positive Relationships**:
1. JAJPUR (Wind Speed): r = 0.209
2. KENDRAPARA (Wind Speed): r = 0.204
3. BHADRAK (Wind Speed): r = 0.199

**Pattern**: Coastal districts show strong positive wind-demand correlation
- Hypothesis: Wind affects power generation (renewable energy) and transmission losses

**Strongest Negative Relationships**:
- PHULBANI (Wind Speed): r = -0.107
- BARIPADA (Wind Speed): r = -0.091
- DEOGARH (Temperature): r = -0.078

**Overall Statistics by Feature**:
| Feature | Mean Correlation | Std Dev | Interpretation |
|---------|------------------|---------|-----------------|
| Wind Speed | 0.072 | 0.073 | **Most consistent positive** |
| Temperature | -0.008 | 0.023 | Near-zero on average |
| Humidity | -0.002 | 0.033 | Weak, variable |
| Precipitation | -0.016 | 0.016 | Slight negative trend |

---

### 5. SLIDING WINDOW CORRELATION (Time-Varying Relationship) ✓
**Concept**: Calculate correlation in moving windows to identify periods of strong/weak relationships
```
For each 168-hour (1-week) window:
    Correlation = corr(Weather_Change_window, Demand_Change_window)
Plot correlation over time
```

**Why It Works**:
- Weather-demand relationships are not constant
- Summer weather affects demand differently than winter
- Captures seasonal and cyclical patterns

**Findings** (4,207 weekly windows analyzed):

| Feature | Avg Corr | Max Corr | Min Corr | Std Dev | Positive % |
|---------|----------|----------|----------|---------|------------|
| **Wind Speed** | 0.170 | 0.575 | -0.283 | 0.150 | **89.4%** ⭐ |
| **Temperature** | 0.085 | 0.642 | -0.321 | 0.238 | 56.7% |
| **Humidity** | -0.069 | 0.362 | -0.574 | 0.218 | 43.8% |
| **Precipitation** | -0.066 | 0.322 | -0.330 | 0.119 | 16.6% |

**Key Insights**:
1. **Wind speed**: Persistently positive - consistent driver
2. **Temperature**: Highly variable - strong seasonal effects
3. **Humidity**: Predominantly negative on average - inverse relationship
4. **Precipitation**: Rare and weak relationship

**Pattern Recognition**:
- Wind correlation peaks during specific periods (possibly monsoon/winter months)
- Temperature correlation shows bimodal pattern (strong summer & winter, weak monsoon)
- Humidity inversely correlated most of the time

---

### 6. GRANGER CAUSALITY TEST (Brief) ✓
**Concept**: Test if past weather values improve demand prediction
```
H0: Weather does not Granger-cause Demand
Test: Does adding past Weather_t-k improve prediction of Demand_t?
p-value < 0.05 = Reject H0 (Weather DOES cause Demand)
```

**Why It Works**:
- Establishes predictive causality (not just correlation)
- Uses statistical hypothesis testing
- Accounts for temporal ordering

**Status**: Requires data stationarity - implementation ongoing with additional preprocessing

---

## Seven Additional Recommended Methodologies

### Method A: Seasonal Decomposition
```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Separate: Trend + Seasonal + Residual
decomposition = seasonal_decompose(demand_series, period=365)

# Analyze how weather correlates with each component
# Example: Weather may only affect residuals (anomalies), not trend
```

**When to use**: When seasonality is strong and masks underlying relationships

---

### Method B: Threshold-Based (Non-Linear) Analysis
```python
# Identify extreme weather events
extreme_temp = temp > 35 | temp < 10
extreme_humidity = humidity > 90
extreme_wind = wind_speed > 30

# Measure demand response to extremes vs. normal conditions
demand_response_extreme = demand[extreme_condition].std()
demand_response_normal = demand[~extreme_condition].std()
```

**Why**: Weather effects may be non-linear (e.g., above 35°C, demand sensitivity increases)

---

### Method C: Frequency Domain Analysis (Fourier/Wavelet)
```python
from scipy.fft import fft
from pywt import wavedec

# Decompose into frequencies
weather_freq = np.abs(fft(weather_changes))
demand_freq = np.abs(fft(demand_changes))

# Find common frequencies (coherence analysis)
# High coherence at certain frequencies = shared oscillations
```

**Why**: Hidden periodicities not visible in time domain

---

### Method D: ARIMAX Models (Autoregressive with Exogenous Variables)
```python
from statsmodels.tsa.arima.model import ARIMA

# Include weather as exogenous variables
model = ARIMA(demand, 
              exog=weather_features,
              order=(p, d, q))

# Compare AIC/BIC with vs. without weather
# If weather significantly improves model, it's influential
```

**Advantage**: Quantifies "% of demand variance explained by weather"

---

### Method E: Machine Learning Feature Importance
```python
from xgboost import XGBRegressor

model = XGBRegressor()
model.fit(X=[temperature, humidity, precipitation, wind_speed, hour, day, ...],
          y=demand)

# Feature importance: How much does each weather variable reduce error?
importances = model.feature_importances_
```

**Advantage**: Captures non-linear relationships automatically

---

### Method F: Causality with Confounding Variable Control
```python
# Partial correlation: Remove effects of confounders
# parcel_corr(weather, demand | hour, day, season)
# This isolates genuine weather effect from day/night and seasonal effects
```

**Why**: Demand varies by hour/day independent of weather. Controlling removes this noise.

---

### Method G: Dynamic Causal Modeling (Advanced)
```
State-Space Models: Model weather → demand mechanisms explicitly
Event Study Analysis: Quantify impact of specific weather events
Impulse Response Functions: How demand responds to weather shock over time
```

---

## Implementation Recommendations

### Phase 1: Quick Wins (Already Implemented ✓)
- [x] First differences analysis
- [x] Lead-lag analysis
- [x] Change point detection
- [x] Regional analysis
- [x] Time-varying correlation
- [x] Visualization of findings

### Phase 2: Medium Effort (Recommended)
- [ ] Seasonal decomposition
- [ ] Threshold-based analysis
- [ ] ARIMAX modeling
- [ ] XGBoost feature importance

### Phase 3: Advanced (If Deeper Analysis Needed)
- [ ] Wavelet coherence analysis
- [ ] Partial correlation with confounders
- [ ] LSTM neural networks
- [ ] Causal inference (PC algorithm, etc.)

---

## Interpretation of Current Results

### What We Know Now
1. ✅ Wind speed is **most consistent driver** (avg r=0.17)
2. ✅ Humidity **co-occurs with demand changes 32% of the time**
3. ✅ Coastal districts show **stronger weather-demand relationship**
4. ✅ Relationships **vary seasonally** (temperature especially)
5. ✅ Some **anticipatory responses** exist (demand leads weather)

### Why Correlation Seems Weak
1. **Non-linearity**: Demand doesn't increase proportionally with temperature
2. **Multiple drivers**: Holidays, day-of-week, time-of-day dominate weather
3. **Regional differences**: Aggregating 30 districts masks local patterns
4. **Time lags**: Effects delayed by hours or days
5. **Threshold effects**: Only extreme weather triggers demand response

### Recommended Next Action
**Implement Method D (ARIMAX)** to:
- Quantify how much weather explains demand
- Account for time lags automatically
- Compare weather + hour + day model vs. weather-only model
- Establish statistical significance

---

## Code Template for ARIMAX

```python
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, r2_score

# Prepare data
train_size = int(len(demand) * 0.8)
train_demand = demand[:train_size]
train_weather = weather_features[:train_size]
test_demand = demand[train_size:]
test_weather = weather_features[train_size:]

# Fit ARIMAX
model = ARIMA(train_demand, 
              exog=train_weather,
              order=(1, 1, 1))  # (p,d,q) - try different values
fitted = model.fit()

# Predict
forecast = fitted.get_forecast(steps=len(test_demand),
                               exog=test_weather)
pred_demand = forecast.predicted_mean

# Evaluate
mae = mean_absolute_error(test_demand, pred_demand)
r2 = r2_score(test_demand, pred_demand)

print(f"Weather-enhanced ARIMAX R²: {r2:.4f}")
print(f"MAE: {mae:.2f} MW")

# Compare with baseline ARIMA (no weather)
baseline = ARIMA(train_demand, order=(1, 1, 1))
baseline_fitted = baseline.fit()
baseline_pred = baseline_fitted.get_forecast(steps=len(test_demand))
baseline_r2 = r2_score(test_demand, baseline_pred.predicted_mean)

print(f"Baseline ARIMA R²: {baseline_r2:.4f}")
print(f"Weather improvement: {(r2-baseline_r2)*100:.2f}%")
```

---

## Key Takeaways

| Aspect | Finding | Implication |
|--------|---------|-------------|
| **Strongest Predictor** | Wind Speed | Use in models first |
| **Best Regional Match** | Coastal Districts + Wind | Geographic focus area |
| **Temporal Pattern** | Time-varying correlation | Seasonal models needed |
| **Co-occurrence** | Humidity 32% overlap | May share drivers |
| **Next Step** | ARIMAX/XGBoost | Quantify real predictive power |

---

**Report Generated**: January 18, 2026
**Analysis Type**: Multi-method weather-demand change correlation
**Data Points**: 4,375 hourly observations across 30 districts
