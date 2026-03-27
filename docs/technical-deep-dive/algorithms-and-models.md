# Algorithms & Models

BatteryML implements **four categories of models**, spanning from simple baselines to
state-of-the-art deep learning architectures.

---

## Category 1: Dummy Baseline

### Dummy Regressor

| Aspect | Detail |
|--------|--------|
| **What it does** | Predicts the mean of training labels for all test samples |
| **Why it matters** | Establishes an error upper bound — any useful model should beat this |
| **Implementation** | `DummyRegressor` from scikit-learn |

---

## Category 2: Domain-Enhanced Linear Models

These models combine **expert-designed features** with linear regression.

### "Variance" Model
- **Feature**: Log-variance of ΔQ₁₀₀₋₁₀(V) — a single scalar
- **Model**: Linear regression
- **Intuition**: The variance of the capacity-voltage change between early cycles
  indicates how fast the battery is degrading

### "Discharge" Model
- **Features**: Multiple characteristics from the discharge period
- **Model**: Linear regression
- **Intuition**: Discharge patterns encode information about capacity loss mechanisms

### "Full" Model
- **Features**: Charge + discharge + temperature features
- **Model**: Linear regression
- **Intuition**: The most comprehensive expert feature set, capturing a wider view
  of degradation signals

> **Key finding**: These models work well for homogeneous datasets (single battery type)
> but struggle with diverse datasets.

---

## Category 3: Traditional Statistical Models

These models use **QdLinear curves** as features and apply different modeling strategies.

### Ridge Regression

> **Simple**: Regular linear regression with a penalty to prevent wild predictions.

- **Technical**: L2-regularized least squares — minimizes $$\|y - Xw\|^2 + \alpha\|w\|^2$$
- **Strength**: Consistent, modest performance across datasets
- **Weakness**: Underperforms on complex datasets (HUST, CRUSH)

### Principal Component Regression (PCR)

> **Simple**: Compresses the data to its most important patterns first, then predicts linearly.

- **Technical**: PCA dimensionality reduction → linear regression
- **Strength**: Excels on MATR1, CRUH, and SNL datasets
- **Insight**: QdLinear features have a linear relationship in reduced subspaces

### Partial Least Squares Regression (PLSR)

> **Simple**: Finds the best simplified view of both features and labels simultaneously.

- **Technical**: Projects X and Y into latent space maximizing covariance
- **Strength**: Good balance of dimensionality reduction and prediction
- **Caution**: Prone to overfitting with too many components

### Gaussian Process Regression

> **Simple**: Makes predictions with confidence intervals — tells you both the answer
> and how sure it is.

- **Technical**: Non-parametric Bayesian model assuming multivariate Gaussian distribution
- **Weakness**: Underperforms PCR and PLSR on all datasets
- **Insight**: Pairwise kernel functions struggle to capture effective degradation patterns

### XGBoost

> **Simple**: Builds many small decision trees that correct each other's mistakes.

- **Technical**: Gradient-boosted decision tree ensemble with regularization
- **Strength**: Strong on diverse datasets (CRUSH, MIX)
- **Hyperparameter insight**: Performance improves up to ~64 boosters, then converges

### Random Forest

> **Simple**: Asks many independent decision trees to vote on the answer.

- **Technical**: Bagged ensemble of decorrelated decision trees
- **Strength**: Excellent on combined datasets; robust SOH baseline
- **Insight**: Stable performance across different tree counts

### LightGBM

> **Simple**: A faster, more efficient version of XGBoost designed by Microsoft.

- **Technical**: Gradient boosted decision trees with histogram-based splitting
- **Strength**: **State-of-the-art for SOC prediction**; efficient on large datasets
- **Note**: Supports both continuous and categorical features

### Support Vector Regression

> **Simple**: Draws the best line through data points while tolerating some error.

- **Technical**: Extension of SVMs for regression — fits within an ε-insensitive tube
- **Implementation**: scikit-learn's SVR

---

## Category 4: Neural Network Models

These models use **QdLinear curve sequences** (cycles 1–100, minus cycle 10) as input.

### Multi-Layer Perceptron (MLP)

> **Simple**: Layers of connected neurons that learn to recognize patterns.

- **Architecture**: Multiple fully-connected layers
- **Strength**: Good on SNL, CLO, CRUH datasets
- **Weakness**: Higher hidden dimensions reduce robustness (increased variance)
- **Optimal hidden dim**: ~8–16 for MIX dataset

### Convolutional Neural Network (CNN)

> **Simple**: Detects local patterns — like how image recognition spots edges and shapes.

- **Battery adaptation**: Treats (cycles × interpolation dimensions) as a 2D image
- **Strength**: Can achieve very accurate predictions with good initialization
- **Critical weakness**: **Extremely sensitive to initialization** — RMSE ranged from 60
  to 367 across seeds on MATR1
- **Optimal hidden dim**: 16

### Long Short-Term Memory (LSTM)

> **Simple**: A neural network that remembers important events across a long sequence.

- **Architecture**: LSTM layer → linear output layer
- **Strength**: Most robust neural network; best on MATR2 among neural methods
- **Insight**: Benefits from larger model capacity; less variance than CNN
- **Use case**: When battery data is naturally sequential

### Gated Recurrent Unit (GRU)

> **Simple**: A simpler, faster version of LSTM.

- **Advantage**: Comparable performance to LSTM with fewer parameters
- **Trade-off**: Slightly less expressive but more computationally efficient

### Transformer

> **Simple**: Looks at all parts of the sequence simultaneously and decides which parts
> matter most for the prediction.

- **Mechanism**: Self-attention weights the significance of each cycle
- **Strength**: Benefits from larger model capacity
- **Status**: Introduced as a **new neural baseline** for battery modeling
- **Insight**: Groundbreaking in NLP/vision but hasn't yet dominated battery modeling

---

## Key Libraries

| Library | Models |
|---------|--------|
| **scikit-learn** | Ridge, PCR, PLSR, Gaussian Process, Random Forest, SVR, Linear Regression, Elastic Net, Dummy |
| **XGBoost** | XGBoost Regression |
| **LightGBM** | LightGBM Regression |
| **PyTorch** | MLP, CNN, LSTM, GRU, Transformer |

---

## Model Training Protocol

- Each model trained with **10 different random seeds**
- Results are **averaged** to eliminate initialization effects
- Standard deviation is reported for models sensitive to initialization
- Evaluation metric: **RMSE** (Root Mean Squared Error)