# Features & Labels

BatteryML organizes features into two categories and supports automatic label annotation
for three major prediction tasks.

---

## Feature Categories

### Within-Cycle Features

Features observed **within individual charge/discharge cycles**. They capture the
electrochemical behavior of the battery at a specific point in its life.

| Feature | Description | What It Captures |
|---------|-------------|-----------------|
| **QdLinear** | Linear interpolation of the capacity-voltage curve during discharge | Shape of the discharge profile |
| **Coulombic Efficiency** | Ratio of discharge to charge capacity | Energy conversion efficiency |
| **Internal Resistance** | Calculated from voltage and current signals | Opposition to current flow |

### Between-Cycle Features

Features that capture **degradation patterns across multiple cycles**. They describe
how the battery changes over its lifetime.

| Feature | Description | What It Captures |
|---------|-------------|-----------------|
| **Variance of ΔQdLinear** | Variance of the difference of QdLinear curves between cycles | Speed of degradation |
| **Capacity Decay Dynamics** | Slope of capacity decay fitted in early cycles | Rate of capacity loss |
| **Average Charging Time** | Mean time to charge across cycles | Irreversible structural changes (lithium plating, SEI growth) |
| **Temperature Dynamics** | Changes in temperature patterns | Intensity of electrochemical reactions |
| **Minimal Internal Resistance** | Lowest recorded internal resistance | Upper bound of battery health |

### Expert-Designed Feature Sets

The paper references three feature sets designed by Severson et al. (2019):

| Feature Set | Components | Use Case |
|-------------|------------|----------|
| **"Variance"** | Log variance of ΔQ₁₀₀₋₁₀(V) during discharge | Simple, single-feature baseline |
| **"Discharge"** | Multiple features from the discharge process | Richer discharge characterization |
| **"Full"** | Features from both charging and discharging, including temperature | Most comprehensive expert features |

### Tensor Representation

All features are output as `torch.Tensor` objects, making them directly compatible
with modern ML frameworks:

```python
def process_cell(self, cell_data: BatteryData) -> torch.Tensor:
    # Extract features and return as tensor
    return feature_tensor
```

## Label Definitions

### RUL Label (Remaining Useful Life)

**Task type**: One prediction per battery cell (offline)

The RUL label is the number of cycles until SOH drops below a threshold (typically 80%):

$$ \text{RUL} = \text{cycle\_at\_80\%\_SOH} - \text{current\_cycle} $$
### SOH Label (State of Health)

**Task type**: One prediction per cycle (online)

The SOH label measures the battery's current health relative to its original capacity:
$$ \text{SOH} = \frac{C_\text{full}}{C_\text{nom}} \times 100\% $$
- Requires a prediction at **every cycle**
- In practice, true SOH requires Reference Performance Tests (RPT) under standardized
  conditions, which are often unavailable
- BatteryML approximates SOH using observed discharge capacity

### SOC Label (State of Charge)

**Task type**: One prediction per moment during charge/discharge (online, real-time)

The SOC label measures remaining charge at any instant:
$$ \text{SOC} = \frac{C_\text{curr}}{C_\text{full}} \times 100\% $$

- Requires **real-time** prediction during operation
- More demanding than SOH in terms of model latency
- Depends on both instantaneous discharge capacity and current SOH
- BatteryML predicts SOC under realistic workload conditions

### Relationship Between Tasks

```
Granularity:  Coarsest ──────────────────────────────> Finest

                RUL                SOH                  SOC
            (per battery)      (per cycle)          (per moment)

Timeline:   Offline            Online               Real-time
```
### Automatic Label Annotation

BatteryML automates label computation by:
1. Sequentially traversing each cycle's charge/discharge data
2. Calculating capacity values from raw signals
3. Computing the appropriate metric (RUL, SOH, or SOC)
4. Outputting labels as `torch.Tensor` for training

This **eliminates the need for manual annotation** and reduces the domain knowledge
barrier for ML engineers.

---

## Feature-Label Summary Table

| Task | Features Used | Label | Prediction Frequency |
|------|--------------|-------|---------------------|
| **RUL** | Between-cycle features from first 100 cycles | Cycle count until 80% SOH | Once per battery |
| **SOH** | Current cycle charging signal + history | $$C_\text{full} / C_\text{nom} \times 100$$ | Once per cycle |
| **SOC** | Current, voltage, time + capacity curves from previous cycles | $$C_\text{curr} / C_\text{full} \times 100$$ | Continuously |