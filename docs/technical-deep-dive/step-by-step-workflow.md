# Step-by-Step Workflow

This chapter walks through the complete BatteryML pipeline from raw data to evaluation.

---

## Workflow Diagram

```
Step 1          Step 2         Step 3           Step 4
Data         Configuration   Feature          Label
Ingestion    ────────────>   Extraction       Annotation
│                           │                  │
▼                           ▼                  ▼
Step 5          Step 6         Step 7           Step 8
Data           Train/Test     Model            Evaluation &
Preprocessing  Split          Training         Visualization
```

---

## Step 1: Data Ingestion & Unification

**Goal**: Convert raw battery data from any source into the unified `BatteryData` format.

```bash
# Download dataset
batteryml download MATR /path/to/raw

# Preprocess into unified format
batteryml preprocess MATR /path/to/raw /path/to/processed
```

What happens:

- Raw files (MATLAB, CSV, etc.) are parsed
- Fields are mapped to standardized names
- Time-series data is organized into cycle records
- Meta information is extracted
- Output is saved as serialized BatteryData objects

## Step 2: Configuration

**Goal**: Define the complete experiment in a single YAML file.

```yaml
train_test_split:
  name: 'MATRPrimaryTestTrainTestSplitter'
  cell_data_path: 'data/processed/MATR'

feature:
  name: 'VarianceModelFeatureExtractor'
  interp_dims: 1000
  critical_cycles: [2, 9, 99]
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

What this configures:

- Which dataset and split strategy to use
- Which features to extract and how to preprocess them
- Which labels to compute and how to transform them
- Which model to train and its hyperparameters

## Step 3: Feature Extraction

**Goal**: Extract meaningful numerical features from raw BatteryData.

The FeatureExtractor processes each cell and outputs `torch.Tensor` features.

Example — "Variance" feature:

1. Compute the QdLinear curve at cycle 10 and cycle 100
2. Calculate $$\Delta Q_{100-10}(V) = QdLinear_{100} - QdLinear_{10}$$
3. Compute the log-variance of this difference
4. Output as a scalar tensor

Example — Raw QdLinear matrix:

1. Compute QdLinear for cycles 1–100
2. Subtract the QdLinear at cycle 10 from each
3. Stack into a 2D tensor (cycles × voltage interpolation points)

## Step 4: Label Annotation

**Goal**: Automatically compute prediction targets from cycling data.

For RUL:

1. Traverse each cycle's discharge data
2. Calculate discharge capacity for each cycle
3. Find the cycle where capacity drops below 80% of nominal
4. Record that cycle number as the end-of-life
5. RUL = end-of-life cycle number

For SOH:

1. For each cycle, compute full discharge capacity
2. Divide by nominal capacity
3. Multiply by 100 to get percentage

For SOC:

1. At each time point within a cycle
2. Compute remaining capacity
3. Divide by current full capacity
4. Multiply by 100

## Step 5: Data Preprocessing

**Goal**: Transform features and labels for better model training.

Common transformations:

| Transformation | Formula | Purpose |
|----------------|---------|---------|
| Z-Score | $$\frac{x - \mu}{\sigma}$$ | Center and scale to unit variance |
| Min-Max | $$\frac{x - \min}{\max - \min}$$ | Scale to [0, 1] range |
| Log-Scale | $$\log(x)$$ | Compress large value ranges |
| Sequential | Chain of transforms | Apply multiple transformations in order |

Example chain: Label → Log-Scale → Z-Score

## Step 6: Train/Test Split

**Goal**: Divide battery cells into training and test sets.

Options:

- Standard splits: Follow published splits for MATR and HUST (reproducibility)
- Random splits: Randomly allocate cells with configurable proportions
- Custom splits: Implement custom logic for specific experimental needs

Important: The split is at the cell level — all cycles from a cell go into either
training or test, never both.

## Step 7: Model Training

**Goal**: Train the selected model on extracted features and labels.

```python
from batteryml.pipeline import Pipeline

pipeline = Pipeline(
    config_path='configs/baselines/sklearn/variance_model/matr_1.yaml',
    workspace='workspaces'
)

model, dataset = pipeline.train(device='cuda')
```

What happens:

- For statistical models: `model.fit(X_train, y_train)` is called
- For neural networks: Mini-batch gradient descent with PyTorch
- Each model is trained with 10 different random seeds
- Checkpoints are saved to the workspace

## Step 8: Evaluation & Visualization

**Goal**: Assess model performance and visualize results.

```python
# Evaluate
pipeline.evaluate(checkpoint='<checkpoint_path>')

# Visualize
prediction = model.predict(dataset, data_type='test').to('cpu')
ground_truth = dataset.test_data.label.to('cpu')
plot_result(ground_truth, prediction)
```

Primary metric: RMSE (Root Mean Squared Error)

Reporting: Results are averaged across 10 seeds, with standard deviation reported
as subscript for models sensitive to initialization.