# BatteryData Format

The `BatteryData` unified data representation is the **core abstraction** of BatteryML.
It standardizes how battery data from diverse sources is stored and accessed.

---

## Why a Unified Format?

Battery data arrives in many forms:
- Different testing equipment produces different file formats
- Labs use different terminology for the same measurements
- Sampling rates and recorded fields vary
- Some datasets include temperature; others don't

`BatteryData` resolves this by defining a **single, comprehensive schema** that all
data is converted into.

---

## Structure Overview

Each `BatteryData` instance represents **a single battery cell** and contains three
components:

```
BatteryData
├── Meta Information (cell-level attributes)
├── Cycle Data (list of CycleData records)
└── Cycling Protocols (charge/discharge specifications)
```

---

## Component 1: Meta Information

Static attributes describing the battery cell.

| Attribute | Example | Description |
|-----------|---------|-------------|
| `cell_id` | `MATR_b1c1` | Unique identifier |
| `form_factor` | `cylindrical_18650` | Physical form |
| `anode_material` | `graphite` | Anode chemistry |
| `cathode_material` | `LFP` | Cathode chemistry |
| `electrolyte_material` | `None` | Electrolyte type (if known) |
| `nominal_capacity_in_Ah` | `1.1` | Rated capacity |
| `depth_of_charge` | `1.0` | Charge depth fraction |
| `depth_of_discharge` | `1.0` | Discharge depth fraction |
| `already_spent_cycles` | `0` | Prior usage cycles |
| `max_voltage_limit_in_V` | `3.5` | Upper voltage cutoff |
| `min_voltage_limit_in_V` | `2.0` | Lower voltage cutoff |
| `max_current_limit_in_A` | `4.0` | Maximum current |
| `min_current_limit_in_A` | `0.0` | Minimum current |
| `description` | `cell data of MATR dataset` | Free-text description |

---

## Component 2: Cycle Data

A **list of `CycleData` records**, each representing one charge-discharge cycle.

| Attribute | Type | Example |
|-----------|------|---------|
| `cycle_number` | int | `1` |
| `voltage_in_V` | list[float] | `[2.022, 2.034, 2.046...]` |
| `current_in_A` | list[float] | `[0.0, 0.216, 0.360...]` |
| `charge_capacity_in_Ah` | list[float] | `[0.0, 1.04e-06, ...]` |
| `discharge_capacity_in_Ah` | list[float] | `[0.0, 6.39e-10, ...]` |
| `time_in_s` | list[float] | `[0.0, 0.002659, ...]` |
| `temperature_in_C` | list[float] | `[31.37, 31.37, ...]` |
| `internal_resistance_in_ohm` | float | `0.01703` |

> **Note**: The default fields focus on electrical data due to its high accessibility.
> Additional data types (mass, pressure, etc.) can be added as needed.

---

## Component 3: Cycling Protocols

Specifications for how the battery was charged and discharged.

| Attribute | Example | Description |
|-----------|---------|-------------|
| `rate_in_C` | `4.0` | C-rate of the protocol |
| `current_in_A` | `None` | Absolute current (if specified) |
| `voltage_in_V` | `None` | Voltage target (if specified) |
| `power_in_W` | `None` | Power target (if specified) |
| `start_voltage_in_V` | `None` | Starting voltage |
| `start_soc` | `1.0` | Starting state of charge |
| `end_voltage_in_V` | `None` | Ending voltage |
| `end_soc` | `0.0` | Ending state of charge |

---

## Converting Data to BatteryData

### Command Line Interface

```bash
# Install BatteryML
pip install -r requirements.txt
pip install .

# Download raw data
batteryml download MATR /path/to/save/raw/data

# Convert to unified format
batteryml preprocess MATR /path/to/save/raw/data /path/to/save/processed/data
```

### Supported Sources

BatteryML provides automated conversion for all seven benchmark datasets:

* CALCE, MATR, HUST, HNEI, RWTH, SNL, UL_PUR

### Custom Data

For custom battery data, users can implement their own preprocessing script that outputs
`BatteryData` objects. The platform supports converting output from various battery
cycler systems (Arbin, MACCOR, Neware, etc.) out of the box.

---

## Visualization Support

BatteryData enables flexible visualization:

1. **Cell-level**: Capacity degradation curves across all cycles
2. **Cycle-level**: Voltage trajectory across successive cycles
3. **Feature-level**: Evolution of Coulombic efficiency or internal resistance

These visualizations help users understand degradation patterns before designing
features and models.

---

## Mathematical Representations

### State of Charge (SOC)

The State of Charge (SOC) is typically calculated as:

$$ SOC = \frac{Q_{remaining}}{Q_{nominal}} \times 100\% $$
Where:
- $$Q_{remaining}$$ is the remaining charge capacity
- $$Q_{nominal}$$ is the nominal capacity of the battery

### Depth of Discharge (DOD)

Depth of Discharge (DOD) is related to SOC:

$$ DOD = 1 - SOC $$
### C-rate

The C-rate is defined as:

$$ C\text{-rate} = \frac{I}{Q_{nominal}} $$
Where:
- $$I$$ is the current in amperes
- $$Q_{nominal}$$ is the nominal capacity in ampere-hours

### Internal Resistance

Internal resistance can be calculated using Ohm's law:

$$ R_{internal} = \frac{\Delta V}{\Delta I} $$
Where:
- $$\Delta V$$ is the change in voltage
- $$\Delta I$$ is the change in current

### Coulombic Efficiency

Coulombic efficiency (CE) is calculated as:

$$ CE = \frac{Q_{discharge}}{Q_{charge}} \times 100\% $$

Where:
- $$Q_{discharge}$$ is the discharge capacity
- $$Q_{charge}$$ is the charge capacity

These mathematical representations provide a foundation for understanding key battery metrics within the BatteryData format.