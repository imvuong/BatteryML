# Getting Started

A practical guide to setting up and running your first BatteryML experiment.

---

## Prerequisites

### Required Software
- **Python 3.8+**
- **pip** package manager
- **Git** for cloning the repository

### Recommended Hardware
- **CPU**: Any modern processor (statistical models run on CPU)
- **GPU**: NVIDIA GPU with CUDA support (recommended for neural network models)
- **RAM**: 8GB+ (16GB recommended for large datasets like MATR)
- **Storage**: 10GB+ for datasets

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/microsoft/BatteryML.git
cd BatteryML
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
pip install .
```

---

## Downloading Data

### Download a Public Dataset

```bash
# Download the MATR dataset (largest, 180 cells)
batteryml download MATR /path/to/save/raw/data

# Download CALCE dataset (smaller, good for testing)
batteryml download CALCE /path/to/save/raw/data
```

### Convert to Unified Format

```bash
batteryml preprocess MATR /path/to/save/raw/data /path/to/save/processed/data
```

### Available Datasets

| Command | Dataset | Size | Chemistry |
|---------|---------|------|-----------|
| `batteryml download MATR` | MATR | 180 cells | LFP |
| `batteryml download CALCE` | CALCE | 13 cells | LCO |
| `batteryml download HUST` | HUST | 77 cells | LFP |
| `batteryml download HNEI` | HNEI | 14 cells | NMC_LCO |
| `batteryml download RWTH` | RWTH | 48 cells | NMC |
| `batteryml download SNL` | SNL | 61 cells | NCA/NMC/LFP |
| `batteryml download UL_PUR` | UL_PUR | 10 cells | NCA |

---

## Running Your First Experiment

### Option 1: Using a Pre-Built Configuration

```python
from batteryml.pipeline import Pipeline
from batteryml.visualization.plot_helper import plot_result

# Create pipeline with existing config
pipeline = Pipeline(
    config_path='configs/baselines/sklearn/variance_model/matr_1.yaml',
    workspace='workspaces/my_first_experiment'
)

# Train the model
model, dataset = pipeline.train(device='cpu')

# Evaluate
pipeline.evaluate()

# Visualize results
prediction = model.predict(dataset, data_type='test').to('cpu')
ground_truth = dataset.test_data.label.to('cpu')
plot_result(ground_truth, prediction)
```

### Option 2: Creating a Custom Configuration

Create a file `configs/my_experiment.yaml`:

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

Then run:

```python
pipeline = Pipeline(
    config_path='configs/my_experiment.yaml',
    workspace='workspaces/my_experiment'
)
model, dataset = pipeline.train(device='cpu')
```

---

## Quick Verification

After running your first experiment, you should see:

✅ Model checkpoint saved in the workspace directory
✅ RMSE metric printed to console
✅ Results saved in the workspace

### Expected RMSE Range (MATR1, Variance Model)

| Model | Expected RMSE |
|-------|---------------|
| Linear Regression ("Variance") | ~136 |
| Ridge Regression | ~116 |
| PCR | ~90 |

If your RMSE is in this range, everything is working correctly!

---

## Common Issues

| Issue | Solution |
|-------|----------|
| `FileNotFoundError` on data path | Ensure you've downloaded and preprocessed the data |
| CUDA not available | Use `device='cpu'` instead of `device='cuda'` |
| `ModuleNotFoundError` | Run `pip install .` from the BatteryML root directory |
| High RMSE values | Check that your config file paths are correct |

---

## Mathematical Background

For those interested in the underlying mathematics, here are some key equations used in battery modeling:

1. **Remaining Useful Life (RUL) Calculation:**
   
   $$RUL = EOL - t$$

   Where:
   - $$EOL$$ is the End of Life cycle
   - $$t$$ is the current cycle

2. **Root Mean Square Error (RMSE):**
   
   $$RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^n (y_i - \hat{y}_i)^2}$$

   Where:
   - $$n$$ is the number of predictions
   - $$y_i$$ is the actual value
   - $$\hat{y}_i$$ is the predicted value

3. **Z-Score Normalization:**
   
   $$z = \frac{x - \mu}{\sigma}$$

   Where:
   - $$x$$ is the original value
   - $$\mu$$ is the mean of the distribution
   - $$\sigma$$ is the standard deviation of the distribution

These equations form the basis for many of the models and transformations used in BatteryML.