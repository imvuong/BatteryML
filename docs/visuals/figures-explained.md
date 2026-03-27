# Figures Explained

This chapter interprets all major figures and visualizations from the BatteryML paper.

## Figure 1: BatteryML Architecture Overview

### What It Shows
A three-column diagram illustrating the complete BatteryML ecosystem:
- **Left**: Data Sources (battery testers, public datasets)
- **Center**: BatteryML Pipeline (BatteryData, feature/label extraction, preprocessing, training, evaluation)
- **Right**: ML Tools (model architectures, learning paradigms)

### Key Takeaway
The **modular design** cleanly separates data concerns (left) from modeling concerns (right), with the BatteryML pipeline (center) providing the bridge. This allows battery experts to contribute to the left side while ML experts focus on the right.

---

## Figure 2: MATR1 Degradation Curves

### What It Shows
Normalized discharge capacity (y-axis) plotted against cycle number (x-axis) for approximately 40 battery cells from the MATR1 dataset.

### How to Read It
- Each colored line represents **one battery cell**
- All cells start near capacity 1.0 (100% of nominal)
- Lines trend downward as batteries degrade
- The x-axis shows the number of charge-discharge cycles

### Key Observations
1. **Wide variability**: Some cells last ~300 cycles, others survive 2000+
2. **Non-linear degradation**: Capacity doesn't drop linearly — there are periods of slow and fast decline
3. **"Knee effect"**: Some batteries show a sudden steep drop near end-of-life
4. **Different fast-charging strategies** cause different degradation rates despite identical battery models

### Why It Matters
This variability is exactly what makes **prediction challenging and valuable**. BatteryML aims to predict these diverse trajectories from early-cycle data.

---

## Figure 3: Voltage Curves Across Cycles

### What It Shows
Voltage (y-axis) over time in seconds (x-axis) for discharge cycles 1–99 of a single MATR1 battery cell.

### How to Read It
- Each line represents **one discharge cycle**
- The voltage starts high and drops as the battery discharges
- Different colors represent different cycle numbers

### Key Observations
1. **Voltage plateau shifts**: The flat region of the discharge curve changes with aging
2. **Discharge duration shortens**: Later cycles discharge faster (less capacity)
3. **Curve shape changes**: The overall voltage profile evolves with degradation

### Why It Matters
These changes encode degradation information. Features like **QdLinear** capture these curve shapes, and differences between curves across cycles indicate the rate and nature of degradation.

---

## Figure 4: Prediction vs. Ground Truth (RUL)

### What It Shows
A scatter plot where:
- **X-axis**: Actual (ground truth) RUL
- **Y-axis**: Predicted RUL
- **Diagonal line**: Perfect prediction (predicted = actual)
- **Color**: Indicates cycle life of the battery

### How to Read It
- Points on the diagonal = **perfect predictions**
- Points above the diagonal = **over-predictions** (model thinks battery lasts longer)
- Points below the diagonal = **under-predictions**

### Key Observations
1. Most predictions **cluster near the diagonal** — generally accurate
2. Some **outliers** exist, especially for long-lived batteries
3. Short-lived batteries tend to be predicted more accurately

### Why It Matters
This visualization provides an **intuitive assessment** of model quality and reveals systematic prediction biases.

---

## Figure 5: Feature Space Ablation

### What It Shows
Bar chart comparing RMSE (y-axis) across different feature sets for various statistical models on the MIX dataset.

### Feature Sets Compared
| Feature Set | Color | Description |
|-------------|-------|-------------|
| "Variance" | Blue | Log variance of ΔQdLinear — single scalar |
| "Discharge" | Green | Multiple discharge-period features |
| "Full" | Teal | Charge + discharge + temperature features |
| QdLinear Curve | Red | Raw interpolated discharge curves |

### Key Observations
1. **"Full" features** perform best with linear models (strong linear correlation with RUL)
2. **"Discharge" features** fail with linear models due to non-linear characteristics but work well with Gaussian Process and Random Forest
3. **Raw QdLinear** performs surprisingly well — models can learn from low-level data
4. **Performance gap** between QdLinear and Full features with Random Forest suggests room for improvement in automatic feature extraction

### Why It Matters
Demonstrates that **feature choice significantly impacts performance** and that expert-designed features still have an edge on diverse datasets.

---

## Figures 6a-c: Hyperparameter Analysis (Statistical Models)

### Figure 6a: PLSR — Number of Principal Components
- **Trend**: Performance worsens (RMSE increases) with more components
- **Insight**: PLSR overfits with too many components
- **Recommendation**: Use cross-validation to find the optimal number

### Figure 6b: Random Forest — Number of Decision Trees
- **Trend**: Stable performance across different tree counts
- **Insight**: Random Forest is robust to this hyperparameter
- **Recommendation**: Use a moderate number for efficiency

### Figure 6c: XGBoost — Number of Boosters
- **Trend**: RMSE improves with more boosters, converging around 64
- **Insight**: More boosters help up to a point
- **Recommendation**: Use 64+ boosters for best performance

---

## Figures 7a-d: Hyperparameter Analysis (Deep Models)

### Figure 7a: MLP — Hidden Dimension
- **Trend**: Larger dimensions increase variance without improving mean error
- **Insight**: Bigger is not always better for MLP on battery data
- **Best value**: Hidden dimension = 8

### Figure 7b: CNN — Hidden Dimension
- **Trend**: Extreme sizes (very small or very large) cause high variance
- **Insight**: CNN requires careful tuning of this parameter
- **Best value**: Hidden dimension = 16

### Figure 7c: LSTM — Hidden Dimension
- **Trend**: Performance improves with larger dimensions
- **Insight**: LSTM benefits from increased model capacity
- **Recommendation**: Use larger dimensions when computationally feasible

### Figure 7d: Transformer — Hidden Dimension
- **Trend**: Similar to LSTM — larger is generally better
- **Insight**: Transformers can leverage increased capacity effectively
- **Recommendation**: Use larger dimensions for battery modeling tasks

---

## Mathematical Equations

While the current document doesn't include explicit mathematical equations, here are some examples of how they could be formatted using LaTeX syntax if needed:

1. For the normalized discharge capacity in Figure 2:

   $$Q_{\text{norm}} = \frac{Q_{\text{actual}}}{Q_{\text{nominal}}}$$

2. For the RMSE metric used in Figure 5:

   $$\text{RMSE} = \sqrt{\frac{1}{n}\sum_{i=1}^n (y_i - \hat{y}_i)^2}$$

3. For the QdLinear feature mentioned:

   $$Q_{\text{dLinear}}(t) = \text{LinearInterpolation}(Q(t))$$

These equations can be rendered properly in Markdown viewers that support LaTeX or MathJax.