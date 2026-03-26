# Environment Setup

## Overview

In this section, you'll set up your development environment for working with BatteryML. A proper setup ensures smooth learning and prevents common technical issues. We'll install Python, required libraries, set up a virtual environment, and verify everything works correctly.

## Why This Matters

A well-configured environment is crucial because:
- **Reproducibility:** Ensures your code runs the same way every time
- **Isolation:** Prevents package conflicts with other projects
- **Professionalism:** Mirrors industry best practices
- **Debugging:** Makes troubleshooting much easier

Think of environment setup like preparing a kitchen before cooking—it's not glamorous, but it's essential!

## Key Concepts

### Virtual Environments

A **virtual environment** is an isolated Python installation that keeps project dependencies separate. This prevents the classic "it works on my machine" problem.

**Why use them?**
- Different projects need different package versions
- Avoid polluting your system Python installation
- Easy to recreate and share with others

### Package Managers

- **pip:** Python's default package installer
- **conda:** Alternative package manager (includes non-Python dependencies)

For BatteryML, we'll primarily use **pip**.

### Dependencies

Dependencies are external libraries your project needs. BatteryML depends on:
- **NumPy:** Numerical computing
- **Pandas:** Data manipulation
- **Scikit-learn:** Traditional ML algorithms
- **PyTorch/TensorFlow:** Deep learning (optional for later phases)
- **Matplotlib/Seaborn:** Visualization

## Prerequisites

Before starting, ensure you have:
- A computer with 8GB+ RAM
- 5GB free disk space
- Stable internet connection
- Administrator/sudo access (for installations)

## Step-by-Step Guide

### Step 1: Install Python

#### Check Current Python Version

```bash
python --version
# or
python3 --version
```

Required: Python 3.7 or higher (3.8+ recommended)

Installation Instructions
macOS:

```bash
# Using Homebrew (recommended)
brew install python@3.11

# Verify installation
python3 --version
```

Ubuntu/Debian Linux:

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Verify installation
python3 --version
```

Windows:

1. Download from python.org
2. Run installer
3. ✅ Important: Check "Add Python to PATH"
4. Choose "Install Now"

```bash
# Verify installation (Command Prompt)
python --version
```

Step 2: Install Git
Git is essential for cloning BatteryML and version control.

macOS:

```bash
# Using Homebrew
brew install git
```

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install git
```

Windows:
Download from git-scm.com

Verify:
```bash
git --version
```

Step 3: Clone BatteryML Repository

```bash
# Navigate to your projects directory
cd ~/projects  # or wherever you keep code

# Clone the repository
git clone https://github.com/battery-ml/batteryml.git

# Enter the directory
cd batteryml

# Check the contents
ls -la
```
Expected structure:
```bash
batteryml/
├── README.md
├── setup.py
├── requirements.txt
├── configs/
├── data/
├── models/
├── features/
└── utils/
```
Step 4: Create Virtual Environment
Using venv (Recommended)
```bash
# Inside the batteryml directory
python3 -m venv venv

# Activate the environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```
You should see (venv) prefix in your terminal:
```bash
(venv) user@computer:~/projects/batteryml$
```
Using conda (Alternative)
```bash
# Create environment
conda create -n batteryml python=3.11

# Activate
conda activate batteryml
```
Step 5: Install BatteryML Dependencies
```bash
# Ensure you're in the batteryml directory with venv activated
(venv) $ pwd
# Should show: .../batteryml

# Upgrade pip (important!)
pip install --upgrade pip

# Install BatteryML in editable mode
pip install -e .

# This installs:
# - BatteryML package itself
# - All required dependencies from setup.py
```
Expected output:
```text
Successfully installed batteryml-0.1.0 numpy-1.24.0 pandas-2.0.0 ...
```
Verify Installation
```bash
# Check installed packages
pip list

# Should include:
# numpy, pandas, scikit-learn, matplotlib, seaborn, pyyaml, etc.
```
Step 6: Install Optional Dependencies
For deep learning (Phase 4):
```bash
# PyTorch (CPU version - good for learning)
pip install torch torchvision torchaudio

# OR TensorFlow
pip install tensorflow

# For GPU support, see official docs (requires CUDA)
```
For Jupyter notebooks (recommended):
```bash
pip install jupyter notebook jupyterlab

# Test installation
jupyter notebook
# Opens browser with Jupyter interface
```
Step 7: Download Sample Data
BatteryML may require downloading datasets:
```bash
# From the batteryml directory
python scripts/download_data.py

# Or manually download from the repository's data documentation
```
Data location: Usually stored in batteryml/data/

Step 8: Verify Installation
Create a test script to verify everything works:
```bash
# Create test file
touch test_setup.py
```
Edit test_setup.py:
```bash
"""Test BatteryML installation."""

import sys
print(f"Python version: {sys.version}")

# Test imports
try:
    import numpy as np
    print(f"✓ NumPy {np.__version__}")
except ImportError:
    print("✗ NumPy not found")

try:
    import pandas as pd
    print(f"✓ Pandas {pd.__version__}")
except ImportError:
    print("✗ Pandas not found")

try:
    import sklearn
    print(f"✓ Scikit-learn {sklearn.__version__}")
except ImportError:
    print("✗ Scikit-learn not found")

try:
    import matplotlib
    print(f"✓ Matplotlib {matplotlib.__version__}")
except ImportError:
    print("✗ Matplotlib not found")

try:
    import batteryml
    print(f"✓ BatteryML installed")
except ImportError:
    print("✗ BatteryML not found")

print("\n✅ Setup complete! Ready to start learning.")
```
Run the test:
```bash
python test_setup.py
```
Expected output:
```bash
Python version: 3.11.0 ...
✓ NumPy 1.24.0
✓ Pandas 2.0.0
✓ Scikit-learn 1.3.0
✓ Matplotlib 3.7.0
✓ BatteryML installed

✅ Setup complete! Ready to start learning.
```

Step 9: Configure Your Text Editor
VS Code (Recommended)
Install VS Code: code.visualstudio.com

Install Python Extension:

Open VS Code
Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
Search "Python"
Install official Microsoft Python extension
Select Python Interpreter:

Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
Type "Python: Select Interpreter"
Choose the venv interpreter: .../batteryml/venv/bin/python
Recommended Extensions:

Pylance (Python language server)
Jupyter (for notebooks)
GitLens (Git integration)
autoDocstring (documentation)
PyCharm (Alternative)
Open the batteryml folder as a project
Configure Python interpreter: Settings → Project → Python Interpreter
Select the venv interpreter
Step 10: Set Up Git Configuration
```bash
# Configure your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Recommended settings
git config --global core.editor "code --wait"  # Use VS Code for commits
git config --global init.defaultBranch main
```
BatteryML Connection
Directory Structure Explained
```graphql
batteryml/
│
├── configs/              # Configuration files (YAML)
│   ├── baseline.yaml     # Default configuration
│   ├── xgboost.yaml      # XGBoost-specific config
│   └── lstm.yaml         # LSTM neural network config
│
├── data/                 # Dataset storage
│   ├── raw/              # Original data files
│   └── processed/        # Preprocessed data
│
├── batteryml/            # Main package
│   ├── __init__.py
│   ├── data/             # Data loading modules
│   ├── features/         # Feature engineering
│   ├── models/           # Model implementations
│   ├── training/         # Training loops
│   └── evaluation/       # Metrics and evaluation
│
├── notebooks/            # Jupyter notebooks for exploration
│   └── exploratory_analysis.ipynb
│
├── scripts/              # Utility scripts
│   ├── download_data.py
│   └── train_model.py
│
├── tests/                # Unit tests
│
├── requirements.txt      # Python dependencies
├── setup.py              # Package installation script
└── README.md             # Project documentation
```
Key Configuration Files
configs/baseline.yaml - Your first configuration file:
```yaml
data:
  dataset: "severson"  # Which dataset to use
  train_split: 0.8     # 80% training, 20% testing
  
preprocessing:
  normalization: "standard"  # z-score normalization
  handle_missing: "drop"     # Drop rows with missing values

features:
  type: "statistical"        # Use statistical features
  include: ["mean", "std", "min", "max"]

model:
  type: "random_forest"      # Algorithm choice
  n_estimators: 100          # Number of trees
  max_depth: 10              # Tree depth

training:
  random_seed: 42            # Reproducibility
  verbose: true              # Print training info
```

You'll modify these configurations throughout your learning!

Hands-On Exercises
Exercise 1: Environment Verification (10 minutes)
Complete the setup verification checklist:
```bash
# 1. Check Python version
python --version
# Should be 3.7+

# 2. Check virtual environment is activated
which python
# Should point to .../batteryml/venv/bin/python

# 3. Verify BatteryML installation
python -c "import batteryml; print('Success!')"

# 4. Check Git configuration
git config --list | grep user

# 5. List installed packages
pip list | grep -E "(numpy|pandas|sklearn)"
```
Document your results in your learning journal.

Exercise 2: First Code Run (15 minutes)
Create and run a simple data loading script:
```python
# File: exercises/ex1_load_data.py
"""Exercise 1: Load and explore battery data."""

import pandas as pd
import numpy as np

# Simulate battery data (we'll use real data in Phase 1)
np.random.seed(42)
data = {
    'cycle': range(1, 101),
    'voltage': np.random.uniform(3.0, 4.2, 100),
    'current': np.random.uniform(-2.0, 2.0, 100),
    'temperature': np.random.uniform(20, 35, 100)
}

df = pd.DataFrame(data)

print("Battery Data Preview:")
print(df.head())

print("\nData Statistics:")
print(df.describe())

print("\nData Types:")
print(df.dtypes)

print("\n✅ Successfully loaded and explored battery data!")
```
Run it:
```bash
python exercises/ex1_load_data.py
```

Exercise 3: Configuration Exploration (10 minutes)
Explore the BatteryML configuration system:
```bash
# 1. List all available configs
ls configs/

# 2. View the baseline config
cat configs/baseline.yaml

# 3. Copy it for modification
cp configs/baseline.yaml configs/my_first_config.yaml

# 4. Open in your editor
code configs/my_first_config.yaml
```
Task: Modify one parameter (e.g., change n_estimators to 50) and save the file.

Exercise 4: Jupyter Notebook Setup (15 minutes)
Set up and test Jupyter:

```bash
# Start Jupyter
jupyter notebook

# This opens your browser
# Navigate to notebooks/ directory
# Create a new notebook: "my_first_notebook.ipynb"
```
In the notebook, test:
```python
# Cell 1: Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Cell 2: Create sample data
cycles = np.arange(1, 101)
capacity = 1.0 - 0.002 * cycles + np.random.normal(0, 0.02, 100)

# Cell 3: Plot
plt.figure(figsize=(10, 6))
plt.plot(cycles, capacity)
plt.xlabel('Cycle Number')
plt.ylabel('Normalized Capacity')
plt.title('Battery Capacity Degradation')
plt.grid(True)
plt.show()
```
Save the notebook—you'll use it for exploratory analysis!

Additional Resources
Documentation
Python venv: docs.python.org/3/library/venv.html
pip user guide: pip.pypa.io/en/stable/user_guide/
Git documentation: git-scm.com/doc
Video Tutorials
"Python Virtual Environments" by Corey Schafer (YouTube)
"VS Code Python Setup" by Programming with Mosh (YouTube)
Tools
pyenv: Manage multiple Python versions
direnv: Auto-activate virtual environments
Poetry: Advanced dependency management (optional)
Quick Summary
✅ Install Python 3.7+ and Git
✅ Clone BatteryML repository
✅ Create and activate virtual environment
✅ Install dependencies with pip install -e .
✅ Verify installation with test script
✅ Configure text editor (VS Code recommended)
✅ Always activate venv before working
✅ Keep dependencies up to date
✅ Use configuration files to control behavior
Next Steps
Your environment is ready! 🎉

Now let's run your first ML model:

→ Running BatteryML