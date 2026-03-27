# Example Workflow

A day-by-day practical workflow showing how to use BatteryML for a real research project.

---

## Scenario

You are a researcher at a battery company. Your goal is to **predict battery lifespan
from early cycling data** to speed up battery testing and design optimization.

---

## Day 1: Setup and Data Exploration

### Download and Preprocess Data

```bash
# Install BatteryML
git clone https://github.com/microsoft/BatteryML.git
cd BatteryML
pip install -r requirements.txt
pip install .

# Download MATR dataset
batteryml download MATR data/raw/MATR

# Convert to unified format
batteryml preprocess MATR data/raw/MATR data/processed/MATR
```

### Explore the Data

```python
import pickle
import matplotlib.pyplot as plt

# Load a processed cell
with open('data/processed/MATR/MATR_b1c1.pkl', 'rb') as f:
    cell = pickle.load(f)

# Check meta information
print(f"Cell ID: {cell.cell_id}")
print(f"Chemistry: {cell.cathode_material}/{cell.anode_material}")
print(f"Nominal capacity: {cell.nominal_capacity_in_Ah} Ah")
print(f"Number of cycles: {len(cell.cycle_data)}")
```

## Day 2: Baseline Model

### Run the "Variance" Model (simplest baseline)

```python
from batteryml.pipeline import Pipeline

pipeline = Pipeline(
    config_path='configs/baselines/sklearn/variance_model/matr_1.yaml',
    workspace='workspaces/day2_variance'
)
model, dataset = pipeline.train(device='cpu')
# Expected RMSE ≈ 136
```

### Run Ridge Regression

```python
pipeline = Pipeline(
    config_path='configs/baselines/sklearn/ridge_regression/matr_1.yaml',
    workspace='workspaces/day2_ridge'
)
model, dataset = pipeline.train(device='cpu')
# Expected RMSE ≈ 116
```

## Day 3: Try Advanced Models

### Tree-Based Model (XGBoost)

```yaml
# configs/custom/xgboost_matr1.yaml
model:
  name: 'XGBoostRULPredictor'
  n_estimators: 100
  max_depth: 6
  learning_rate: 0.1

train_test_split:
  name: 'MATRPrimaryTestTrainTestSplitter'
  cell_data_path: 'data/processed/MATR'

feature:
  name: 'VoltageCapacityMatrixFeatureExtractor'
  diff_base: 8
  max_cycle_index: 98
  cycles_to_keep: 98
  use_precalculated_qdlin: True

label:
  name: 'RULLabelAnnotator'

feature_transformation:
  name: 'ZScoreDataTransformation'

label_transformation:
  name: 'SequentialDataTransformation'
  transformations:
    - name: 'LogScaleDataTransformation'
    - name: 'ZScoreDataTransformation'
```

### Neural Network (LSTM)

```yaml
# configs/custom/lstm_matr1.yaml
model:
  name: 'LSTMRULPredictor'
  hidden_dim: 32
  num_layers: 2

# ... (same data/feature/label sections)
```

```python
pipeline = Pipeline(
    config_path='configs/custom/lstm_matr1.yaml',
    workspace='workspaces/day3_lstm'
)
model, dataset = pipeline.train(device='cuda')
```

## Day 4: Custom Feature Engineering

### Design a Coulombic Efficiency Feature

See Custom Feature Extractors for the full implementation.

```yaml
# configs/custom/ce_feature_matr1.yaml
feature:
  name: 'NewFeatureExtractor'
  min_cycle_index: 0
  max_cycle_index: 99

model:
  name: 'LinearRegressionRULPredictor'

# ... (same split/label/transformation sections)
```

### Compare Results

```python
import torch

results = {}

for config_name in ['variance', 'ridge', 'xgboost', 'lstm', 'ce_feature']:
    pipeline = Pipeline(
        config_path=f'configs/custom/{config_name}_matr1.yaml',
        workspace=f'workspaces/comparison/{config_name}'
    )
    model, dataset = pipeline.train(device='cpu')
    pred = model.predict(dataset, data_type='test').to('cpu')
    gt = dataset.test_data.label.to('cpu')
    rmse = torch.sqrt(torch.mean((pred - gt) ** 2))
    results[config_name] = rmse.item()

print("Results comparison:")
for name, rmse in sorted(results.items(), key=lambda x: x[1]):
    print(f"  {name}: RMSE = {rmse:.1f}")
```

## Day 5: Cross-Dataset Evaluation

### Combine Multiple Datasets

```bash
# Download additional datasets
batteryml download CALCE data/raw/CALCE
batteryml download HNEI data/raw/HNEI
batteryml preprocess CALCE data/raw/CALCE data/processed/CALCE
batteryml preprocess HNEI data/raw/HNEI data/processed/HNEI
```

### Test Generalization

Try your best model on the combined CRUH dataset to see how it handles
multiple battery chemistries.

## Day 6: Hyperparameter Tuning

### Vary Key Parameters

```python
# Example: test different XGBoost n_estimators
for n_est in [32, 64, 128, 256]:
    # Programmatically modify config or create separate config files
    config = load_config('configs/custom/xgboost_matr1.yaml')
    config['model']['n_estimators'] = n_est

    pipeline = Pipeline(config=config, workspace=f'workspaces/tuning/xgb_{n_est}')
    model, dataset = pipeline.train(device='cpu')
```

## Day 7: Report and Visualization

### Create Final Comparison Plot

```python
from batteryml.visualization.plot_helper import plot_result

# Load best model
pipeline = Pipeline(
    config_path='configs/custom/best_model.yaml',
    workspace='workspaces/final'
)
model, dataset = pipeline.train(device='cpu')

# Plot prediction vs. ground truth
prediction = model.predict(dataset, data_type='test').to('cpu')
ground_truth = dataset.test_data.label.to('cpu')
plot_result(ground_truth, prediction)
```

## Summary of Weekly Progress

| Day | Activity                   | Outcome                                  |
|-----|----------------------------|------------------------------------------|
| 1   | Setup + data exploration   | Understand dataset structure             |
| 2   | Baseline models            | Variance RMSE ≈ 136, Ridge RMSE ≈ 116    |
| 3   | Advanced models            | XGBoost and LSTM results                 |
| 4   | Custom features            | Coulombic efficiency feature tested      |
| 5   | Cross-dataset evaluation   | Generalization assessment                |
| 6   | Hyperparameter tuning      | Optimized model configuration            |
| 7   | Reporting and visualization| Final plots and comparison table         |

