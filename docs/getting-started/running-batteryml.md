# Running BatteryML

## Overview

Now that your environment is set up, it's time to run your first machine learning model! In this section, you'll learn how to execute BatteryML's training pipeline, understand the output, and make your first modifications. By the end, you'll have successfully trained multiple models on real battery data.

## Why This Matters

Running the code before fully understanding it might seem backward, but it's intentional:
- **Build intuition:** See what ML actually does before diving into theory
- **Immediate feedback:** Know your setup works correctly
- **Motivation:** Experience the "aha!" moment of a trained model
- **Reference point:** Have working examples to return to when learning details

This "run first, understand later" approach mirrors how professional developers explore new codebases.

## Key Concepts

### Command-Line Interface (CLI)

BatteryML uses a CLI for training models. This means you run commands in the terminal rather than clicking buttons in a GUI.

**Advantages:**
- Reproducible: Commands can be scripted
- Fast: No GUI overhead
- Professional: Industry-standard approach
- Automatable: Easy to run batch experiments

### Configuration Files (YAML)

BatteryML uses **YAML files** to control behavior. Instead of changing code, you modify configurations.

**Example structure:**
```yaml
key: value
nested:
  key1: value1
  key2: value2
list:
  - item1
  - item2
```
Training Pipeline
The training pipeline has these stages:

Load data: Read battery cycling data from files
Preprocess: Clean and normalize the data
Engineer features: Extract meaningful features
Train model: Fit the ML algorithm
Evaluate: Measure performance on test set
Save results: Store model and metrics

## Step-by-Step Guide
Step 1: Understand the Basic Command
The basic BatteryML command structure:

```bash
python main.py --config <config_file>
```

Or if using a training script:

```bash
python scripts/train.py --config configs/baseline.yaml
```

Components:

python: The Python interpreter
main.py or scripts/train.py: Entry point script
--config: Flag specifying configuration file path
configs/baseline.yaml: The configuration file to use
Step 2: Explore Available Configurations

```bash
# List all config files
ls configs/

# Expected output:
# baseline.yaml
# random_forest.yaml
# xgboost.yaml
# lstm.yaml
# svm.yaml
```
View a configuration:
```bash
cat configs/baseline.yaml
```

Typical contents:
```yaml
# Dataset configuration
data:
  name: "severson"
  path: "data/severson_dataset.pkl"
  target: "cycle_life"  # What we're predicting
  
# Train/test split
split:
  test_size: 0.2
  random_state: 42
  shuffle: true

# Preprocessing
preprocessing:
  normalize: true
  normalization_method: "standard"  # z-score normalization
  
# Feature engineering
features:
  feature_set: "statistical"
  include:
    - "discharge_capacity_mean"
    - "voltage_mean"
    - "temperature_max"
    - "internal_resistance"

# Model configuration
model:
  type: "random_forest"
  hyperparameters:
    n_estimators: 100
    max_depth: 10
    random_state: 42

# Training
training:
  verbose: 1
  
# Evaluation metrics
evaluation:
  metrics:
    - "rmse"
    - "mae"
    - "r2"
  
# Output
output:
  save_model: true
  model_path: "models/baseline_model.pkl"
  save_predictions: true
  predictions_path: "results/baseline_predictions.csv"
```

Step 3: Run Your First Model
Let's start with the baseline configuration:
```bash
# Ensure you're in the batteryml directory
cd ~/projects/batteryml

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Run baseline model
python main.py --config configs/baseline.yaml
```
Expected output:

```bash
==================================================
BatteryML Training Pipeline
==================================================

[INFO] Loading configuration: configs/baseline.yaml
[INFO] Configuration loaded successfully

[INFO] Loading dataset: severson
[INFO] Dataset shape: (124, 9) cells
[INFO] Target variable: cycle_life

[INFO] Splitting data: 80% train, 20% test
[INFO] Train set: 99 samples
[INFO] Test set: 25 samples

[INFO] Preprocessing data...
[INFO] Normalizing features using standard scaler
[INFO] Preprocessing complete

[INFO] Engineering features...
[INFO] Feature set: statistical
[INFO] Features extracted: 20
[INFO] Feature engineering complete

[INFO] Training model: RandomForestRegressor
[INFO] Hyperparameters: {'n_estimators': 100, 'max_depth': 10}
[INFO] Training started...
[INFO] Training complete (2.3s)

[INFO] Evaluating model...
[INFO] Metrics:
  - RMSE: 145.32
  - MAE: 98.67
  - R²: 0.8234
  
[INFO] Saving model to: models/baseline_model.pkl
[INFO] Saving predictions to: results/baseline_predictions.csv

==================================================
Training complete! ✅
==================================================
```
Step 4: Understand the Output
Let's break down what happened:

Data Loading
```bash
[INFO] Dataset shape: (124, 9) cells
```
124 battery cells in the dataset
9 raw features per cell
Train/Test Split
```bash
[INFO] Train set: 99 samples
[INFO] Test set: 25 samples
```
80/20 split as specified in config
Model trains on 99 cells, evaluates on 25 unseen cells
Feature Engineering
```bash
[INFO] Features extracted: 20
```
Started with 9 raw features
Created 20 engineered features
These are statistical aggregations (mean, std, etc.)
Model Training
```bash
[INFO] Training complete (2.3s)
```
RandomForest trained in 2.3 seconds
Time varies based on hardware and dataset size
```bash
RMSE: 145.32    # Root Mean Squared Error (lower is better)
MAE: 98.67      # Mean Absolute Error (lower is better)
R²: 0.8234      # R-squared (higher is better, max 1.0)
```
Interpretation:

R² = 0.82 means model explains 82% of variance
On average, predictions are off by ~99 cycles (MAE)
This is a reasonably good baseline!
Step 5: Examine the Results
Saved Model

```bash
# Check that model was saved
ls -lh models/

# Expected:
# baseline_model.pkl  (file size: ~2.5 MB)
```
This .pkl file contains the trained model. You can load it later without retraining.

Predictions File
```bash
# View predictions
head results/baseline_predictions.csv
```
Contents:
```csv
cell_id,actual_cycle_life,predicted_cycle_life,error
cell_001,1200,1145,55
cell_002,850,912,-62
cell_003,1450,1389,61
...
```
Visualize Results (Optional)
Create a quick visualization script:
```python
# File: visualize_results.py
import pandas as pd
import matplotlib.pyplot as plt

# Load predictions
df = pd.read_csv('results/baseline_predictions.csv')

# Plot actual vs predicted
plt.figure(figsize=(10, 6))
plt.scatter(df['actual_cycle_life'], df['predicted_cycle_life'], alpha=0.6)
plt.plot([df['actual_cycle_life'].min(), df['actual_cycle_life'].max()],
         [df['actual_cycle_life'].min(), df['actual_cycle_life'].max()],
         'r--', label='Perfect prediction')
plt.xlabel('Actual Cycle Life')
plt.ylabel('Predicted Cycle Life')
plt.title('Model Predictions vs Actual Values')
plt.legend()
plt.grid(True)
plt.savefig('results/prediction_plot.png')
plt.show()

print("✅ Plot saved to results/prediction_plot.png")
```
Run it:
```bash
python visualize_results.py
```
Step 6: Run a Different Model
Now let's try XGBoost for comparison:
```bash
python main.py --config configs/xgboost.yaml
```
Expected output:
```yaml
[INFO] Training model: XGBRegressor
[INFO] Hyperparameters: {'n_estimators': 100, 'max_depth': 6, 'learning_rate': 0.1}
...
[INFO] Metrics:
  - RMSE: 132.18
  - MAE: 89.23
  - R²: 0.8512
```
Comparison:

Model	RMSE	MAE	R²
Random Forest	145.32	98.67	0.8234
XGBoost	132.18	89.23	0.8512
XGBoost performs better! (Lower error, higher R²)

Step 7: Modify a Configuration
Let's create a custom configuration:

```bash
# Copy baseline config
cp configs/baseline.yaml configs/my_experiment.yaml

# Edit it
code configs/my_experiment.yaml  # or use your preferred editor
```
Make these changes:

```yaml
model:
  type: "random_forest"
  hyperparameters:
    n_estimators: 200      # Increased from 100
    max_depth: 15          # Increased from 10
    min_samples_split: 5   # Added new parameter
    random_state: 42
```

Run your custom config:

```bash
python main.py --config configs/my_experiment.yaml
```
Did performance improve? Document the results!

Step 8: Use Command-Line Arguments
You can override config values from the command line:
```bash
# Override random seed
python main.py --config configs/baseline.yaml --seed 123

# Override model type
python main.py --config configs/baseline.yaml --model xgboost

# Override multiple parameters
python main.py \
  --config configs/baseline.yaml \
  --model random_forest \
  --n_estimators 150 \
  --max_depth 12
```

This is useful for quick experiments without editing config files.

Step 9: Enable Logging
For detailed debugging, enable verbose logging:

```bash
# Run with debug logging
python main.py --config configs/baseline.yaml --log-level DEBUG

# Save log to file
python main.py --config configs/baseline.yaml --log-file train.log

# Check the log
cat train.log
```

Step 10: Batch Experiments
Run multiple configurations automatically:

```bash
# Create a simple bash script: run_experiments.sh
#!/bin/bash

configs=("baseline" "random_forest" "xgboost" "svm")

for config in "${configs[@]}"; do
    echo "Running $config..."
    python main.py --config "configs/${config}.yaml"
    echo "Completed $config"
    echo "---"
done

echo "All experiments complete!"
```

Make it executable and run:

```bash
chmod +x run_experiments.sh
./run_experiments.sh
```
