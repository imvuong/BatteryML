# Pipeline API

The `Pipeline` class is the primary interface for running experiments in BatteryML. It orchestrates the entire workflow from configuration to evaluation.

## Basic Usage

```python
from batteryml.pipeline import Pipeline
from batteryml.visualization.plot_helper import plot_result

# Step 1: Create a pipeline from a config file
pipeline = Pipeline(
    config_path='configs/baselines/sklearn/variance_model/matr_1.yaml',
    workspace='workspaces'
)

# Step 2: Train the model
model, dataset = pipeline.train(device='cuda')

# Step 3: Evaluate (optionally with a saved checkpoint)
pipeline.evaluate(checkpoint='<your checkpoint path>')

# Step 4: Visualize results
prediction = model.predict(dataset, data_type='test').to('cpu')
ground_truth = dataset.test_data.label.to('cpu')
plot_result(ground_truth, prediction)
```

## Pipeline Lifecycle

### Initialization

```python
pipeline = Pipeline(config_path='path/to/config.yaml', workspace='workspaces')
```

What happens:

1. YAML config file is parsed
2. All components are instantiated based on the config:
   - Train/test splitter
   - Feature extractor
   - Label annotator
   - Data preprocessors (feature + label transformations)
   - Model
3. Workspace directory is created for checkpoints and results

### Training

```python
model, dataset = pipeline.train(device='cuda')
```

What happens:

1. Raw BatteryData is loaded from the specified path
2. Train/test split is applied at the cell level
3. Features are extracted for all cells
4. Labels are annotated for all cells
5. Feature and label transformations are fitted on training data and applied
6. Model is trained:
   - Statistical models: `model.fit(X_train, y_train)`
   - Neural networks: Mini-batch gradient descent loop
7. Checkpoints are saved to the workspace
8. Trained model and dataset objects are returned

### Evaluation

```python
pipeline.evaluate(checkpoint='<path>')
```

What happens:

1. Model is loaded from the checkpoint
2. Test features are transformed using fitted transformations
3. Predictions are generated: `model.predict(X_test)`
4. Labels are inverse-transformed back to original scale
5. RMSE is computed and saved to the workspace

#### Root Mean Square Error (RMSE)

The RMSE is calculated using the following formula:

$$RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$

Where:
- $$n$$ is the number of samples
- $$y_i$$ is the true value
- $$\hat{y}_i$$ is the predicted value

## Device Support

```python
# Train on GPU
model, dataset = pipeline.train(device='cuda')

# Train on CPU
model, dataset = pipeline.train(device='cpu')
```

- Neural network models benefit from GPU acceleration
- Statistical models (scikit-learn) run on CPU regardless

## Workspace Structure

After training, the workspace contains:

```
workspaces/
├── <experiment_name>/
│   ├── config.yaml          # Copy of the configuration
│   ├── checkpoints/         # Saved model weights
│   ├── results/             # Evaluation metrics
│   └── logs/                # Training logs
```