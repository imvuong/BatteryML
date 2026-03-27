# Platform Architecture

## Overview

BatteryML follows a **modular pipeline architecture** that separates concerns into independent, configurable components.

## Architecture Diagram

```
Data Sources → BatteryData (Unified Format) → BatteryML Pipeline → ML Tools
│
┌───────────────┼───────────────────┐
│               │                   │
FeatureExtractor  LabelExtractor   DataPreprocessor
│               │                   │
└───────┬───────┘         (Smoothing, Normalization)
        │
TrainTestSplitter
        │
┌────────┴────────┐
│                 │
Training          Evaluation
```

## The Three Layers

### Layer 1: Data Sources (Input)

Battery data originates from:
- **Battery testers** (Arbin, MACCOR, Neware, etc.)
- **Public datasets** (CALCE, MATR, HUST, HNEI, RWTH, SNL, UL_PUR)

Data arrives in various formats (CSV, MATLAB, HDF5, etc.) with inconsistent fields and terminology.

### Layer 2: BatteryML Pipeline (Processing)

The core of the platform, consisting of five modules:

#### Module 1: Train-Test Split

**Purpose**: Divides battery cells into training and test sets.

**Capabilities**:
- Random split with configurable proportions
- Standard splits for published datasets (MATR, HUST) for reproducibility
- Custom partitioning logic

#### Module 2: Feature Extractor

**Purpose**: Converts raw battery data into numerical feature tensors.

**Capabilities**:
- Within-cycle features (QdLinear, Coulombic efficiency, internal resistance)
- Between-cycle features (variance of QdLinear differences, capacity decay dynamics)
- Raw signal extraction for neural networks
- Extensible to custom features

#### Module 3: Label Extractor

**Purpose**: Automatically computes prediction targets.

**Capabilities**:
- RUL annotation (cycles until SOH < threshold)
- SOH computation (capacity ratio per cycle)
- SOC computation (remaining charge ratio per moment)

#### Module 4: Data Preprocessor

**Purpose**: Transforms features and labels before training.

**Capabilities**:
- Z-score normalization
- Min-Max normalization
- Log-scale transformation
- Sequential (chained) transformations
- Data augmentation

#### Module 5: Model Module

**Purpose**: Defines model architecture and training parameters.

**Capabilities**:
- Linear models (Ridge, PLSR, PCR, Elastic Net)
- Tree-based models (Random Forest, XGBoost, LightGBM)
- Neural networks (MLP, CNN, LSTM, GRU, Transformer)
- Custom model integration via registry pattern

### Layer 3: ML Tools (Output)

The trained models support multiple learning paradigms:
- **Supervised learning** — Standard training with labeled data
- **Transfer learning** — Applying models across datasets
- **Unsupervised learning** — Potential future extension

## Design Principles

### Modularity
Each component can be swapped independently. Changing the model doesn't require changing the feature extractor, and vice versa.

### Configuration-Driven
All experiments are defined via YAML configuration files. No code changes needed to switch models, features, or datasets.

### Registry Pattern
New components register themselves via decorators:

```python
@FEATURE_EXTRACTORS.register()
@MODELS.register()
@DATA_TRANSFORMATIONS.register()
```

This allows automatic discovery and usage through configuration files.

### Scikit-learn Convention
All models (including neural networks) expose `fit()` and `predict()` methods, ensuring consistent behavior across the pipeline.

### Tensor-Based
All features and labels are `torch.Tensor` objects, enabling seamless integration with deep learning frameworks.