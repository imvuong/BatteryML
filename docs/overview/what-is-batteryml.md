# What is BatteryML?

## Simple Explanation

BatteryML is a **"one-stop shop" toolbox** that lets researchers predict how and when
batteries will wear out using machine learning — without needing to be an expert in
*both* batteries and ML.

## Technical Definition

BatteryML is an **open-source Python platform** that provides an integrated, end-to-end
pipeline for battery degradation modeling. It encompasses:

- **Unified data representation** for heterogeneous battery datasets
- **Feature engineering** modules (within-cycle and between-cycle)
- **Automatic label annotation** for supervised learning tasks
- **A comprehensive model library** from linear regression to Transformers
- **An end-to-end pipeline** from raw data ingestion to evaluation and visualization

## Key Characteristics

### 🔓 Open Source
- Hosted on GitHub: [github.com/microsoft/BatteryML](https://github.com/microsoft/BatteryML)
- Freely available for research and commercial use

### 📦 All-Encompassing
- Covers the complete ML workflow: data → features → labels → training → evaluation
- No need to stitch together separate tools

### 🔌 Modular
- Each component (features, models, preprocessing) can be swapped independently
- New components can be added via a registry pattern without modifying core code

### 🌐 Universal
- Supports multiple battery chemistries (LFP, NMC, NCA, LCO)
- Handles data from various testing equipment and labs
- Covers three major battery tasks: RUL, SOH, and SOC prediction

## How It Differs from Existing Tools

The paper compares BatteryML to **BEEP** (Battery Evaluation and Early Prediction),
the main existing tool:

| Feature | BEEP | BatteryML |
|---------|------|-----------|
| **Target audience** | Battery experts with coding skills | Both battery experts AND ML professionals |
| **Model support** | Linear models | Linear, tree-based, and deep learning models |
| **Data format** | File-system organization | Unified tensor-based representation |
| **Deep learning** | Not natively supported | Native PyTorch integration |
| **Transfer learning** | Not supported | Supported via unified data representation |
| **Modularity** | Coupled design | Decoupled modules with registry pattern |