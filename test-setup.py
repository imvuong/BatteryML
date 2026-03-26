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