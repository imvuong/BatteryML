# Custom Feature Extractors

BatteryML provides a general interface for creating custom feature extractors, allowing researchers to incorporate domain knowledge into the ML pipeline.

## Interface

All feature extractors must:
1. Inherit from `BaseFeatureExtractor`
2. Implement the `process_cell` method
3. Accept a `BatteryData` object and return a `torch.Tensor`

```python
class BaseFeatureExtractor:
    def process_cell(self, cell_data: BatteryData) -> torch.Tensor:
        raise NotImplementedError
```

BatteryML handles:
- Iterating through all battery cells
- Collating outputs into structured datasets
- Managing train/test separation

## Example: Coulombic Efficiency Feature

```python
# batteryml/feature/new_feature.py
import torch
from typing import List
from src.builders import FEATURE_EXTRACTORS
from src.data.battery_data import BatteryData
from src.feature.base import BaseFeatureExtractor

@FEATURE_EXTRACTORS.register()
class NewFeatureExtractor(BaseFeatureExtractor):
    def __init__(self,
                 min_cycle_index: int = 0,
                 max_cycle_index: int = 99):
        self.min_cycle_index = min_cycle_index
        self.max_cycle_index = max_cycle_index

    def process_cell(self, cell_data: BatteryData) -> torch.Tensor:
        coulombic_efficiencies = []

        for cycle_index, cycle_data in enumerate(cell_data.cycle_data):
            if self.min_cycle_index <= cycle_index <= self.max_cycle_index:
                ce = f_cycle_coulombic_efficiency(
                    cycle_data.discharge_capacity_in_Ah,
                    cycle_data.charge_capacity_in_Ah
                )
                coulombic_efficiencies.append(ce)

        coulombic_efficiencies = torch.FloatTensor(coulombic_efficiencies)

        feature = torch.tensor([
            torch.mean(coulombic_efficiencies),
            torch.std(coulombic_efficiencies),
            torch.var(coulombic_efficiencies)
        ])

        feature[torch.isnan(feature) | torch.isinf(feature)] = 0.

        return feature


def f_cycle_coulombic_efficiency(Q_d, Q_c):
    """Compute Coulombic efficiency from discharge and charge capacities."""
    return Q_d[-1] / (Q_c[-1] + 1e-5)
```

## Step-by-Step Breakdown

1. **Register the Extractor**
   ```python
   @FEATURE_EXTRACTORS.register()
   ```
   This decorator adds the class to BatteryML's registry, making it available in config files.

2. **Define Configurable Parameters**
   ```python
   def __init__(self, min_cycle_index: int = 0, max_cycle_index: int = 99):
   ```
   Parameters specified in the config file will be passed here as keyword arguments.

3. **Process Each Cell**
   ```python
   def process_cell(self, cell_data: BatteryData) -> torch.Tensor:
   ```
   This method is called once per cell. You have access to all cycle data and meta information through the `cell_data` object.

4. **Return a Tensor**
   The output must be a `torch.Tensor`. Its shape depends on the task:
   - RUL: One feature vector per cell
   - SOH: One feature vector per cycle
   - SOC: One feature vector per time step

## Using Custom Features in Configuration

```yaml
feature:
  name: 'NewFeatureExtractor'
  min_cycle_index: 0
  max_cycle_index: 99
```

The `name` field must match the registered class name. All other fields are passed as constructor arguments.

## Built-in Feature Extractors

| Name | Description |
|------|-------------|
| VarianceModelFeatureExtractor | Log variance of ΔQ₁₀₀₋₁₀(V) |
| DischargeModelFeatureExtractor | Multiple discharge features |
| FullModelFeatureExtractor | Charge + discharge + temperature features |
| VoltageCapacityMatrixFeatureExtractor | Raw QdLinear matrix for neural networks |

## Tips for Custom Features

- Always handle NaN and inf values before returning
- Use `torch.FloatTensor` for consistent dtype
- Keep features as simple tensors for compatibility with all model types
- Document the physical meaning of your features for reproducibility
