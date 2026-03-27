# Configuration Files

BatteryML uses YAML configuration files to define every aspect of an experiment.
This approach enables **reproducible experiments without code changes**.

---

## Configuration Structure

Every config file has the same top-level structure:

```yaml
# 1. How to split the data
train_test_split:
  name: '<SplitterClass>'
  cell_data_path: '<path/to/processed/data>'

# 2. How to extract features
feature:
  name: '<FeatureExtractorClass>'
  # ... feature-specific parameters

# 3. How to preprocess features
feature_transformation:
  name: '<TransformationClass>'

# 4. How to compute labels
label:
  name: '<LabelAnnotatorClass>'

# 5. How to preprocess labels
label_transformation:
  name: '<TransformationClass>'
  # ... or sequential transformations

# 6. Which model to use
model:
  name: '<ModelClass>'
  # ... model hyperparameters
```

### Complete Example: "Variance" Model on MATR1

```yaml
train_test_split:
  name: 'MATRPrimaryTestTrainTestSplitter'
  cell_data_path: 'data/processed/MATR'

feature:
  name: 'VarianceModelFeatureExtractor'
  interp_dims: 1000
  critical_cycles:
    - 2
    - 9
    - 99
  use_precalculated_qdlin: True

feature_transformation:
  name: 'ZScoreDataTransformation'

label:
  name: 'RULLabelAnnotator'

label_transformation:
  name: 'SequentialDataTransformation'
  transformations:
    - name: 'LogScaleDataTransformation'
    - name: 'ZScoreDataTransformation'

model:
  name: 'LinearRegressionRULPredictor'
```

## What Each Section Does

| Section | Purpose | Example Value |
|---------|---------|---------------|
| train_test_split | Defines how cells are divided | MATR primary test split |
| feature | Specifies feature extraction method | Variance of ΔQdLinear |
| feature_transformation | Preprocessing for features | Z-score normalization |
| label | Specifies prediction target | RUL annotation |
| label_transformation | Preprocessing for labels | Log-scale → Z-score chain |
| model | Defines model and hyperparameters | Linear regression |

### Example: LightGBM with Custom Features

```yaml
model:
  name: 'LightgbmRULPredictor'
  boosting_type: 'gbdt'
  learning_rate: 0.001
  n_estimators: 200
  objective: 'regression'

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

## Config File Organization

BatteryML organizes config files by model type and dataset:

```
configs/
├── baselines/
│   ├── sklearn/
│   │   ├── variance_model/
│   │   │   ├── matr_1.yaml
│   │   │   ├── matr_2.yaml
│   │   │   └── hust.yaml
│   │   ├── discharge_model/
│   │   ├── ridge_regression/
│   │   └── ...
│   └── pytorch/
│       ├── mlp/
│       ├── cnn/
│       ├── lstm/
│       └── transformer/
└── custom/
    └── ...
```

## How Configuration Maps to Code

```
YAML Config                    Python Code
─────────────                  ───────────
name: 'ClassName'         →    Registry looks up ClassName
param1: value1            →    ClassName(param1=value1, param2=value2)
param2: value2
```

All fields beneath `name` are passed as keyword arguments to the constructor
of the registered class.

## Mathematical Equations

Some configurations may involve mathematical equations. For example:

1. Z-Score Normalization:
   $$z = \frac{x - \mu}{\sigma}$$

   Where:
   - $$z$$ is the normalized value
   - $$x$$ is the original value
   - $$\mu$$ is the mean of the population
   - $$\sigma$$ is the standard deviation of the population

2. Log-Scale Transformation:
   $$y = \log(x + 1)$$

   Where:
   - $$y$$ is the transformed value
   - $$x$$ is the original value

## Tips

- **Reproducibility**: Save your config files alongside results
- **Iteration**: Duplicate a config and change one parameter to test variations
- **Organization**: Name configs by `<model>_<dataset>.yaml` for clarity
- **Validation**: BatteryML will raise an error if a registered name is not found