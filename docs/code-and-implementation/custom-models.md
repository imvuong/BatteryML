# Custom Models

BatteryML supports easy integration of custom models through its registry pattern
and consistent API design.

## Model Interface

BatteryML follows the **scikit-learn convention**:

- **Statistical models**: Implement `fit()` and `predict()`
- **Neural networks**: Implement `forward()` — BatteryML wraps training/evaluation
  into `fit()` and `predict()` automatically

## Example: LightGBM RUL Predictor

### Implementation

```python
# batteryml/model/rul_predictor/lightgbm.py
from lightgbm import LGBMRegressor
from src.builders import MODELS
from src.models.sklearn_model import SklearnModel

@MODELS.register()
class LightgbmRULPredictor(SklearnModel):
    def __init__(self, *args, workspace: str = None, **kwargs):
        SklearnModel.__init__(self, workspace)
        self.model = LGBMRegressor(*args, **kwargs)
```

### Configuration

```yaml
model:
  name: 'LightgbmRULPredictor'
  boosting_type: 'gbdt'
  learning_rate: 0.001
  n_estimators: 200
  objective: 'regression'
```

### How It Works

1. `@MODELS.register()` adds the class to BatteryML's model registry
2. Config fields (`boosting_type`, `learning_rate`, etc.) are passed as `**kwargs` to the constructor
3. BatteryML calls `LightgbmRULPredictor.model.fit()` during training
4. BatteryML calls `LightgbmRULPredictor.model.predict()` during evaluation

## Creating a Custom Statistical Model

### Step 1: Inherit from SklearnModel

```python
from src.builders import MODELS
from src.models.sklearn_model import SklearnModel

@MODELS.register()
class MyCustomPredictor(SklearnModel):
    def __init__(self, *args, workspace: str = None, **kwargs):
        SklearnModel.__init__(self, workspace)
        # Initialize your model here
        self.model = YourModelClass(*args, **kwargs)
```

### Step 2: Ensure `fit()` and `predict()` exist

If your underlying model already has `fit()` and `predict()` (like scikit-learn
models), no additional work is needed. BatteryML will call these automatically.

### Step 3: Register and Import

The `@MODELS.register()` decorator handles registration. Make sure the module is
imported during BatteryML initialization.

## Creating a Custom Neural Network Model

### Step 1: Inherit from the Neural Network Base

```python
import torch.nn as nn
from src.builders import MODELS

@MODELS.register()
class MyNeuralPredictor(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.layers(x)
```

### Step 2: BatteryML Handles Training

BatteryML wraps the `forward()` method into `fit()` and `predict()` calls,
managing the training loop, loss computation, and optimization automatically.

## Built-in Models

### Statistical Models

| Class | Algorithm |
|-------|-----------|
| LinearRegressionRULPredictor | Linear Regression |
| RidgeRegressionRULPredictor | Ridge Regression |
| PLSRRULPredictor | Partial Least Squares |
| PCRRULPredictor | Principal Component Regression |
| GaussianProcessRULPredictor | Gaussian Process |
| XGBoostRULPredictor | XGBoost |
| RandomForestRULPredictor | Random Forest |
| SVRRULPredictor | Support Vector Regression |

### Neural Network Models

| Class | Architecture |
|-------|--------------|
| MLPRULPredictor | Multi-Layer Perceptron |
| CNNRULPredictor | Convolutional Neural Network |
| LSTMRULPredictor | Long Short-Term Memory |
| GRURULPredictor | Gated Recurrent Unit |
| TransformerRULPredictor | Transformer |

## Math Equations

For completeness, here are some example equations that might be relevant to battery modeling:

1. **Capacity Fade Model**:
   
   $$Q(t) = Q_0 - k \sqrt{t}$$

   Where:
   - $$Q(t)$$ is the capacity at time $$t$$
   - $$Q_0$$ is the initial capacity
   - $$k$$ is the fade rate constant

2. **Arrhenius Equation for Temperature Dependence**:
   
   $$k = A e^{-E_a / (RT)}$$

   Where:
   - $$k$$ is the rate constant
   - $$A$$ is the pre-exponential factor
   - $$E_a$$ is the activation energy
   - $$R$$ is the gas constant
   - $$T$$ is the absolute temperature

3. **State of Health (SoH) Calculation**:

   $$SoH = \frac{Q_{current}}{Q_{nominal}} \times 100\%$$

   Where:
   - $$Q_{current}$$ is the current capacity
   - $$Q_{nominal}$$ is the nominal (initial) capacity
