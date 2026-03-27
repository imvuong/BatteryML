# Core Terminology

This chapter defines the essential terms you'll encounter throughout BatteryML and
battery degradation research.

---

## Battery Health Metrics

### SOH — State of Health

> **Simple**: "How healthy is this battery compared to when it was new?"

**Technical Definition**: The ratio of a battery's current full discharge capacity to its
original nominal capacity, expressed as a percentage.

$$SOH = \frac{C_{full}}{C_{nom}} \times 100\%$$
Where:
- $$C_{full}$$: Full discharge capacity in the current cycle
- $$C_{nom}$$: Nominal (rated) capacity when the battery was new

**Example**: A battery with 1.1 Ah nominal capacity currently delivering 0.88 Ah has
$$SOH = \frac{0.88}{1.1} \times 100\% = 80\%$$

**Key characteristics**:
- Measured per cycle
- Decreases monotonically over time (with some noise)
- Battery is typically considered "end of life" when SOH drops below 80%

### SOC — State of Charge

> **Simple**: "How much juice is left in the battery right now?"

**Technical Definition**: The ratio of remaining capacity to the current full capacity,
expressed as a percentage.

$$SOC = \frac{C_{curr}}{C_{full}} \times 100\%$$
Where:
- $$C_{curr}$$: Remaining capacity at a given moment
- $$C_{full}$$: Current full capacity of the battery

**Example**: A battery with 0.88 Ah full capacity and 0.44 Ah remaining has
$$SOC = \frac{0.44}{0.88} \times 100\% = 50\%$$

**Key characteristics**:
- Changes moment-to-moment during use
- Requires real-time prediction
- More challenging when depth of discharge is less than 100%

### RUL — Remaining Useful Life

> **Simple**: "How many more charge cycles until the battery is dead?"

**Technical Definition**: The number of charge-discharge cycles remaining until the
battery's SOH drops below a defined threshold (typically 80%).

**Key characteristics**:
- A single value per battery (or per prediction point)
- Critical for battery management, second-hand EV evaluation, and warranty planning
- Predicted using early-cycle data (e.g., first 100 cycles)

---

## Battery Science Terms

### Cycle
A single complete **charge and discharge** of a battery. Each cycle is recorded as a
time-series containing voltage, current, capacity, temperature, and resistance measurements.

### Nominal Capacity
The manufacturer-specified capacity of a battery under standard conditions, measured in
**Amp-hours (Ah)**. For example, 1.1 Ah means the battery can theoretically deliver 1.1 amps
for one hour.

### Cathode Materials

| Abbreviation | Full Name | Formula |
|--------------|-----------|---------|
| LFP | Lithium Iron Phosphate | LiFePO₄ |
| NMC | Lithium Nickel Manganese Cobalt Oxide | LiNiMnCoO₂ |
| NCA | Lithium Nickel Cobalt Aluminum Oxide | LiNiCoAlO₂ |
| LCO | Lithium Cobalt Oxide | LiCoO₂ |

Different cathode materials exhibit **different degradation patterns**, which is a key
source of data heterogeneity.

### Degradation Mechanisms

| Mechanism | Description |
|-----------|-------------|
| SEI Growth | Solid Electrolyte Interphase film forms on the anode, consuming lithium ions |
| Lithium Plating | Metallic lithium deposits on the anode surface |
| Active Material Loss | Electrode materials physically degrade (e.g., graphite delamination) |
| Electrolyte Decomposition | The liquid electrolyte breaks down chemically |
| Internal Resistance Increase | The battery's opposition to current flow grows |

### Coulombic Efficiency
The ratio of discharge capacity to charge capacity in a single cycle. A perfect battery
would have 100% Coulombic efficiency. Lower efficiency indicates irreversible side reactions.
$$CE = \frac{Q_{discharge}}{Q_{charge}}$$
### QdLinear
A key feature in battery modeling. It is obtained by **linear interpolation** of the
discharge capacity-voltage curve, creating a standardized representation that can be
compared across cycles.

### Internal Resistance
The opposition to current flow inside a battery. Measured using voltage and current signals.
Increases as the battery degrades.

### Depth of Discharge (DOD)
The percentage of battery capacity that has been discharged. 100% DOD means fully
discharged; 50% DOD means half-discharged.

---

## Machine Learning Terms

### Feature Extraction
The process of converting raw battery data into meaningful numerical inputs for ML models.

### Label Annotation
The process of computing the prediction target (e.g., RUL, SOH, SOC) from raw cycling data.

### RMSE — Root Mean Squared Error
The primary evaluation metric used in BatteryML:

$$RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^n (y_i - \hat{y}_i)^2}$$

Where:
- $$y_i$$: Actual value
- $$\hat{y}_i$$: Predicted value
- $$n$$: Number of samples

Lower RMSE = better predictions.

### Transfer Learning
Training a model on one dataset and applying it to a different (but related) dataset.
BatteryML's unified format makes this possible across battery chemistries.