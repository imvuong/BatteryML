# Libraries & Tools

BatteryML is built on well-established Python libraries for both machine learning and deep learning.

---

## Core Dependencies

| Library | Version Info | Role in BatteryML |
|---------|--------------|-------------------|
| **PyTorch** | Deep learning framework | Neural network models (MLP, CNN, LSTM, GRU, Transformer) |
| **scikit-learn** | ML toolkit | Statistical models (Ridge, PCR, PLSR, GP, RF, SVR, Linear Reg) |
| **XGBoost** | Gradient boosting | XGBoost regression models |
| **LightGBM** | Gradient boosting (Microsoft) | LightGBM regression models |
| **NumPy** | Numerical computing | Array operations and mathematical functions |
| **PyYAML** | Configuration | YAML config file parsing |
| **torch.Tensor** | Tensor operations | Feature and label representation |

---

## Why These Libraries?

### PyTorch for Neural Networks
- Industry standard for deep learning research
- Dynamic computation graphs for flexible model design
- GPU acceleration via CUDA
- Strong ecosystem for experimentation

### scikit-learn for Statistical Models
- Comprehensive collection of classical ML algorithms
- Consistent `fit()` / `predict()` API
- Well-tested and production-ready implementations
- Excellent documentation and community support

### XGBoost & LightGBM for Tree Models
- State-of-the-art gradient boosting implementations
- Handle tabular data exceptionally well
- LightGBM is especially efficient on large datasets
- Both support regression out of the box

---

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install BatteryML
pip install .
```

## Key Internal Modules

| Module Path | Purpose |
|-------------|---------|
| `batteryml/pipeline.py` | Main pipeline orchestration |
| `batteryml/data/battery_data.py` | BatteryData class definition |
| `batteryml/feature/` | Feature extractor implementations |
| `batteryml/label/` | Label annotator implementations |
| `batteryml/data/transformation/` | Data preprocessing transformations |
| `batteryml/models/` | Model implementations |
| `batteryml/train_test_split/` | Split strategy implementations |
| `batteryml/visualization/` | Plotting and visualization utilities |
| `src/builders.py` | Registry managers for components |

## Registry System

BatteryML uses a registry pattern for component management:

```python
from src.builders import FEATURE_EXTRACTORS, MODELS, DATA_TRANSFORMATIONS

# Register a new feature extractor
@FEATURE_EXTRACTORS.register()
class MyFeature(BaseFeatureExtractor):
    ...

# Register a new model
@MODELS.register()
class MyModel(SklearnModel):
    ...

# Register a new transformation
@DATA_TRANSFORMATIONS.register()
class MyTransform(BaseDataTransformation):
    ...
```

This pattern allows new components to be automatically discovered and used via configuration files without modifying core pipeline code.