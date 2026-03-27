# Custom Preprocessing

BatteryML's data preprocessing module supports flexible transformation and
refinement of both features and labels before training.

---

## Transformation Interface

All transformations must implement:

```python
class BaseDataTransformation:
    def fit(self, data: torch.Tensor) -> None:
        """Learn parameters from training data."""
        raise NotImplementedError

    def transform(self, data: torch.Tensor) -> torch.Tensor:
        """Apply the transformation."""
        raise NotImplementedError

    def inverse_transform(self, data: torch.Tensor) -> torch.Tensor:
        """Reverse the transformation (for converting predictions back)."""
        raise NotImplementedError
```

## Example: Min-Max Normalization

```python
# src/data/transformation/min_max.py
import torch
from src.builders import DATA_TRANSFORMATIONS
from src.data.transformation.base import BaseDataTransformation

@DATA_TRANSFORMATIONS.register()
class MinMaxDataTransformation(BaseDataTransformation):
    def __init__(self, base: float = None):
        self.min = None
        self.max = None

    def fit(self, data: torch.Tensor) -> torch.Tensor:
        self.min = torch.min(data)
        self.max = torch.max(data)

    def assert_fitted(self):
        assert self.min is not None, 'Transformation not fitted!'
        assert self.max is not None, 'Transformation not fitted!'

    @torch.no_grad()
    def transform(self, data: torch.Tensor) -> torch.Tensor:
        self.assert_fitted()
        data = (data - self.min) / (self.max - self.min)
        return data

    @torch.no_grad()
    def inverse_transform(self, data: torch.Tensor) -> torch.Tensor:
        self.assert_fitted()
        data = data * (self.max - self.min) + self.min
        return data

    def to(self, device):
        self.min = self.min.to(device)
        self.max = self.max.to(device)
        return self
```

## Built-in Transformations

| Name | Formula | Use Case |
|------|---------|----------|
| ZScoreDataTransformation | $$\frac{x - \mu}{\sigma}$$ | Standardize to zero mean, unit variance |
| LogScaleDataTransformation | $$\log(x)$$ | Compress large ranges (e.g., RUL labels) |
| MinMaxDataTransformation | $$\frac{x - \min(x)}{\max(x) - \min(x)}$$ | Scale to [0, 1] |

## Sequential Transformations

BatteryML supports chaining multiple transformations using the sequential wrapper:

```yaml
label_transformation:
  name: 'SequentialDataTransformation'
  transformations:
    - name: 'LogScaleDataTransformation'
    - name: 'ZScoreDataTransformation'
```

This applies transformations in order:

1. First: Log-scale → $$\log(\text{label})$$
2. Then: Z-score → $$\frac{\log(\text{label}) - \mu}{\sigma}$$

The `inverse_transform` reverses them in the opposite order.

## Using in Configuration

### Feature Transformation

```yaml
feature_transformation:
  name: 'MinMaxDataTransformation'
```

### Label Transformation

```yaml
label_transformation:
  name: 'SequentialDataTransformation'
  transformations:
    - name: 'LogScaleDataTransformation'
    - name: 'MinMaxDataTransformation'
```

## Important Notes

- Transformations are fitted on training data only to prevent data leakage
- `inverse_transform` is applied to predictions before computing evaluation metrics
- The `to(device)` method ensures transformations work on GPU when needed
- Always implement both `transform` and `inverse_transform` for proper evaluation