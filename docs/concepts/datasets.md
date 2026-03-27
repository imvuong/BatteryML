# Datasets

BatteryML benchmarks are built on **seven publicly accessible battery datasets** spanning
different chemistries, form factors, and testing conditions.

## Dataset Overview

| Dataset | Chemistry | Cells | Nominal Capacity | Voltage Range | Avg RUL | Form |
|---------|-----------|-------|-----------------|---------------|---------|------|
| **CALCE** | LCO/graphite | 13 | 1.1 Ah | 2.7–4.2V | 566±106 | Prismatic |
| **MATR** | LFP/graphite | 180 | 1.1 Ah | 2.0–3.6V | 823±368 | Cylindrical 18650 |
| **HUST** | LFP/graphite | 77 | 1.1 Ah | 2.0–3.6V | 1899±389 | Cylindrical 18650 |
| **HNEI** | NMC_LCO/graphite | 14 | 2.8 Ah | 3.0–4.3V | 248±15 | Cylindrical 18650 |
| **RWTH** | NMC/carbon | 48 | 1.11 Ah | 3.5–3.9V | 658±64 | Cylindrical 18650 |
| **SNL** | NCA,NMC,LFP/graphite | 61 | 1.1 Ah | 2.0–3.6V | 1256±1321 | Cylindrical 18650 |
| **UL_PUR** | NCA/graphite | 10 | 3.4 Ah | 2.7–4.2V | 209±50 | Pouch |

## Individual Dataset Details

### CALCE
- **Source**: Center for Advanced Life Cycle Engineering
- **Batteries**: CS2 and CX2 prismatic cells with LCO cathode
- **Charging protocol**: CC/CV — 0.5C to 4.2V, then hold 4.2V until current < 0.05A
- **Cutoff voltage**: 2.7V

### MATR (Largest Public Dataset)
- **Source**: Severson et al. (2019) and Attia et al. (2020)
- **Size**: 180 cells — the largest publicly available complete cycling dataset
- **Batteries**: Commercial 18650 LFP cells
- **Conditions**: 30°C forced convection, same discharge but different fast-charging strategies
- **End criteria**: Discharge capacity < 80% of rated capacity
- **Split into**: MATR1 (same charging policies in train/test), MATR2 (unseen policies in test), CLO (random split)

### HUST
- **Source**: Ma et al. (2022)
- **Batteries**: 77 LFP cells, same model as MATR
- **Protocol**: Same charging, different multi-stage discharge protocols
- **Conditions**: 30°C constant temperature

### HNEI
- **Source**: Devie et al. (2018)
- **Batteries**: 18650 cells with NMC+LCO blended cathode
- **Protocol**: 1.5C cycling to 100% DOD, >1000 cycles at room temperature

### SNL
- **Source**: Preger et al. (2020)
- **Batteries**: 18650 cells in NCA, NMC, and LFP
- **Focus**: Impact of temperature, DOD, and discharge current on degradation
- **Protocol**: Capacity check cycles (3× charge/discharge at 0.5C) between cycling rounds

### UL_PUR
- **Source**: Juarez-Robles et al. (2020, 2021)
- **Batteries**: Commercial NCA pouch cells
- **Protocol**: 1C cycling, 2.7–4.2V, room temperature, until 10–20% capacity fade

### RWTH
- **Source**: Li et al. (2021)
- **Batteries**: 48 Sanyo/Panasonic UR18650E NMC cells
- **Protocol**: All cells aged under identical conditions
- **Special**: Begin-of-Life (BOL) test and regular Aging Reference Parameter Tests (RPT)

## Combined Datasets

For RUL tasks, the authors created combined datasets to test cross-chemistry generalization:

| Combined Dataset | Composition | Purpose |
|-----------------|-------------|---------|
| **CRUH** | CALCE + RWTH + UL_PUR + HNEI | Small datasets combined |
| **CRUSH** | CALCE + RWTH + UL_PUR + SNL + HNEI | Includes short-life batteries; predicts 90% SOH from first 20 cycles |
| **MIX** | All datasets combined | Largest battery degradation dataset with complete cycling records |

## How to Access Datasets

```bash
# Download a dataset
batteryml download MATR /path/to/save/raw/data

# Convert to unified format
batteryml preprocess MATR /path/to/save/raw/data /path/to/save/processed/data
```