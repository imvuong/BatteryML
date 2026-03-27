# Evaluation Results

This chapter presents the benchmark results from the BatteryML paper across three
battery degradation tasks.

---

## RUL Prediction Results

### Benchmark Table (RMSE — lower is better)

| Model | MATR1 | MATR2 | HUST | SNL | CLO | CRUH | CRUSH | MIX |
|-------|-------|-------|------|-----|-----|------|-------|-----|
| **Dummy regressor** | 398 | 510 | 419 | 466 | 331 | 239 | 576 | 573 |
| **"Variance" model** | 136 | 211 | 398 | 360 | 179 | 118 | 506 | 521 |
| **"Discharge" model** | 329 | **149** | 322 | 267 | 143 | 76 | >1000 | >1000 |
| **"Full" model** | 167 | >1000 | 335 | 433 | **138** | 93 | >1000 | 331 |
| **Ridge Regression** | 116 | 184 | >1000 | 242 | 169 | 65 | >1000 | 372 |
| **PCR** | **90** | 187 | 435 | **200** | 197 | 68 | 560 | 376 |
| **PLSR** | 104 | 181 | 431 | 242 | 176 | **60** | 535 | 383 |
| **Gaussian Process** | 154 | 224 | >1000 | 251 | 204 | 115 | >1000 | 573 |
| **XGBoost** | 334 | 799 | 395 | 547 | 215 | 119 | **330** | **205** |
| **Random Forest** | 168 | 233 | 368 | 532 | 192 | 81 | 416 | 197 |
| **MLP** | 149 | 275 | 459 | 370 | 146 | 103 | 565 | 451 |
| **CNN** | 102 | 228 | 465 | 924 | >1000 | 174 | 545 | 272 |
| **LSTM** | 119 | 219 | 443 | 539 | 222 | 105 | 519 | 268 |
| **Transformer** | 135 | 364 | 391 | 424 | 187 | 81 | 550 | 271 |

> For neural networks, subscript values in the original paper indicate standard deviation
> across 10 seeds.

### Key Findings — RUL

1. **No universally best model** — each method excels on some datasets and fails on others
2. **Linear models with expert features** work well for single-chemistry datasets
   (MATR2, HUST, CLO) but fail on diverse datasets (CRUSH, MIX)
3. **Tree-based models** (XGBoost, Random Forest) are strongest on combined datasets
4. **Neural networks** show promise but suffer from **high variance** due to initialization
5. **PCR achieves the best score on MATR1** (RMSE = 90)
6. **XGBoost achieves the best score on MIX** (RMSE = 205)

---

## SOH Estimation Results

### Benchmark Table (RMSE — lower is better)

| Method | CALCE | HNEI | HUST | MATR | RWTH | SNL | UL_PUR |
|--------|-------|------|------|------|------|-----|--------|
| **Linear Reg** | **0.45** | **0.30** | 4.74 | 252.75 | 26.48 | 2.89 | **0.75** |
| **Ridge Reg** | 0.46 | 0.31 | 4.62 | 255.27 | 15.68 | 2.90 | **0.75** |
| **PLSR** | 0.60 | 0.36 | 4.39 | 258.93 | 11.83 | 2.77 | 0.76 |
| **PCR** | 3.93 | 0.52 | **4.00** | 755.23 | 14.80 | 13.52 | 1.22 |
| **Random Forest** | 0.72 | 0.38 | 6.04 | **0.53** | **0.17** | **1.80** | 1.04 |
| **LightGBM** | 0.74 | 0.34 | **4.30** | 0.97 | **0.17** | 2.11 | 0.99 |
| **LSTM** | 16.78 | 16.90 | 9.55 | 1.33 | 23.79 | 7.50 | 6.57 |
| **MLP** | 16.73 | 14.36 | 8.62 | 2.89 | 63.38 | 607.46 | 16.89 |
| **GRU** | 16.77 | 16.88 | 9.25 | 1.43 | 23.78 | 7.50 | 6.48 |

### Key Findings — SOH

1. **Tree-based models are the most robust** — consistent low errors even on MATR
2. **Linear models are generally effective** except for MATR (variable charging strategies)
3. **Deep learning models underperform** traditional methods on most datasets
4. **Random Forest achieves RMSE = 0.17 on RWTH** — near-perfect prediction
5. The MATR dataset is challenging for linear models due to diverse charging policies

---

## SOC Estimation Results

### Benchmark Table (RMSE — lower is better)

| Method | CALCE | HNEI | HUST | MATR | RWTH | SNL | UL_PUR |
|--------|-------|------|------|------|------|-----|--------|
| **Linear Reg** | 6.76 | 7.20 | 5.65 | 2.70 | 64.50 | 12.78 | 2.48 |
| **Ridge Reg** | 6.76 | 7.20 | 5.65 | 2.70 | 64.50 | 12.78 | 2.48 |
| **PLSR** | 8.78 | 7.82 | 5.11 | 2.70 | 64.50 | 14.32 | 3.93 |
| **PCR** | 6.76 | 7.20 | 5.65 | 2.70 | 64.50 | 12.78 | 2.49 |
| **LightGBM** | **1.71** | **0.76** | **0.28** | **0.82** | 313.76 | **2.62** | **0.84** |
| **LSTM** | 46.50 | 44.32 | 27.99 | 35.87 | 435.52 | 27.92 | 51.83 |
| **MLP** | 38.25 | 16.19 | 4.60 | 4.57 | 2224.03 | 13.92 | 50.19 |
| **GRU** | 47.54 | 45.57 | 28.30 | 35.93 | 435.55 | 27.90 | 51.04 |

### Key Findings — SOC

1. **LightGBM dominates** — state-of-the-art for SOC prediction on most datasets
2. **RWTH is universally difficult** — all methods show suboptimal performance,
   suggesting current approaches struggle with certain aging patterns
3. **Linear models consistently outperform deep learning** in SOC prediction
4. **Deep learning models need further optimization** — both input features and
   network architectures require improvement for SOC tasks
5. **LightGBM achieves RMSE = 0.28 on HUST** — remarkably accurate

---

## Cross-Task Summary

| Task | Best Traditional Model | Best Neural Model | Overall Winner |
|------|------------------------|-------------------|----------------|
| **RUL** | PCR / PLSR (homogeneous), XGBoost (diverse) | Transformer / LSTM | Depends on dataset |
| **SOH** | Random Forest / LightGBM | LSTM / GRU | Tree-based models |
| **SOC** | LightGBM | MLP | LightGBM |

---

## Key Takeaway

> **There is no universally optimal method for battery modeling.** All methods excel
> on certain datasets and may exhibit error divergence on others. This indicates
> considerable scope for improvement in battery degradation prediction.

---

## Mathematical Definitions

### Root Mean Square Error (RMSE)

RMSE is calculated as:

$$ RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2} $$

where:
- $$n$$ is the number of samples
- $$y_i$$ is the actual value
- $$\hat{y}_i$$ is the predicted value

### State of Health (SOH)

SOH is typically defined as:

$$ SOH = \frac{C_{current}}{C_{nominal}} \times 100\% $$

where:
- $$C_{current}$$ is the current capacity of the battery
- $$C_{nominal}$$ is the nominal (or initial) capacity of the battery

### State of Charge (SOC)

SOC is often calculated using the Coulomb counting method:

$$ SOC(t) = SOC(t_0) + \frac{1}{C_{nominal}} \int_{t_0}^t I(\tau) d\tau $$

where:
- $$SOC(t_0)$$ is the initial state of charge
- $$C_{nominal}$$ is the nominal capacity
- $$I(\tau)$$ is the current (positive for charging, negative for discharging)

These mathematical definitions provide a foundation for understanding the metrics and concepts used in battery degradation prediction tasks.