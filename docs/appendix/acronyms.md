# Acronyms & Abbreviations

A comprehensive glossary of all acronyms and abbreviations used throughout the
BatteryML project, paper, and documentation.

---

## Quick Reference Table

| Acronym | Full Form | Category |
|---------|-----------|----------|
| [BMS](#bms) | Battery Management System | Battery Systems |
| [BOL](#bol) | Begin-Of-Life | Battery Testing |
| [CALCE](#calce) | Center for Advanced Life Cycle Engineering | Dataset |
| [CC](#cc) | Constant Current | Charging Protocol |
| [CC/CV](#cccv) | Constant Current / Constant Voltage | Charging Protocol |
| [CE](#ce) | Coulombic Efficiency | Battery Metric |
| [CLO](#clo) | Closed-Loop Optimization | Dataset |
| [CNN](#cnn) | Convolutional Neural Network | Machine Learning |
| [CRUH](#cruh) | CALCE + RWTH + UL_PUR + HNEI | Combined Dataset |
| [CRUSH](#crush) | CALCE + RWTH + UL_PUR + SNL + HNEI | Combined Dataset |
| [CSV](#csv) | Comma-Separated Values | Data Format |
| [CUDA](#cuda) | Compute Unified Device Architecture | Computing |
| [CV](#cv) | Constant Voltage | Charging Protocol |
| [DOD](#dod) | Depth of Discharge | Battery Metric |
| [EDS](#eds) | Energy Dispersive Spectroscopy | Characterization |
| [EIS](#eis) | Electrochemical Impedance Spectroscopy | Characterization |
| [ELI5](#eli5) | Explain Like I'm 5 | Documentation |
| [EOL](#eol) | End-Of-Life | Battery Lifecycle |
| [EV](#ev) | Electric Vehicle | Application |
| [GP](#gp) | Gaussian Process | Machine Learning |
| [GPR](#gpr) | Gaussian Process Regression | Machine Learning |
| [GPU](#gpu) | Graphics Processing Unit | Computing |
| [GRU](#gru) | Gated Recurrent Unit | Machine Learning |
| [HDF5](#hdf5) | Hierarchical Data Format version 5 | Data Format |
| [HNEI](#hnei) | Hawaii Natural Energy Institute | Dataset |
| [HUST](#hust) | Huazhong University of Science and Technology | Dataset |
| [ICLR](#iclr) | International Conference on Learning Representations | Venue |
| [IR](#ir) | Internal Resistance | Battery Metric |
| [LCO](#lco) | Lithium Cobalt Oxide (LiCoO₂) | Cathode Material |
| [LFP](#lfp) | Lithium Iron Phosphate (LiFePO₄) | Cathode Material |
| [LGBM](#lgbm) | Light Gradient Boosting Machine | Machine Learning |
| [LSTM](#lstm) | Long Short-Term Memory | Machine Learning |
| [MATR](#matr) | Massachusetts / Toyota Research | Dataset |
| [MIX](#mix) | All Combined Datasets | Combined Dataset |
| [ML](#ml) | Machine Learning | General |
| [MLP](#mlp) | Multi-Layer Perceptron | Machine Learning |
| [NCA](#nca) | Lithium Nickel Cobalt Aluminum Oxide (LiNiCoAlO₂) | Cathode Material |
| [NMC](#nmc) | Lithium Nickel Manganese Cobalt Oxide (LiNiMnCoO₂) | Cathode Material |
| [PCA](#pca) | Principal Component Analysis | Machine Learning |
| [PCR](#pcr) | Principal Component Regression | Machine Learning |
| [PHM](#phm) | Prognostics and Health Management | Battery Systems |
| [PLSR](#plsr) | Partial Least Squares Regression | Machine Learning |
| [QdLinear](#qdlinear) | Linearized Discharge Capacity | Feature |
| [RF](#rf) | Random Forest | Machine Learning |
| [RMSE](#rmse) | Root Mean Squared Error | Evaluation Metric |
| [RNN](#rnn) | Recurrent Neural Network | Machine Learning |
| [RPT](#rpt) | Reference Performance Test | Battery Testing |
| [RUL](#rul) | Remaining Useful Life | Battery Metric |
| [RWTH](#rwth) | Rheinisch-Westfälische Technische Hochschule Aachen | Dataset |
| [SEI](#sei) | Solid Electrolyte Interphase | Degradation Mechanism |
| [SNL](#snl) | Sandia National Laboratories | Dataset |
| [SOC](#soc) | State of Charge | Battery Metric |
| [SOH](#soh) | State of Health | Battery Metric |
| [SVM](#svm) | Support Vector Machine | Machine Learning |
| [SVR](#svr) | Support Vector Regression | Machine Learning |
| [UL_PUR](#ul_pur) | Underwriters Laboratories / Purdue University | Dataset |
| [YAML](#yaml) | YAML Ain't Markup Language | Configuration |

---

## Detailed Definitions

### Battery Metrics & States

#### BMS
**Battery Management System**

An electronic system that manages a rechargeable battery by monitoring its state,
calculating secondary data, reporting that data, controlling its environment, and
balancing it. BMS uses SOH, SOC, and RUL predictions for operational decisions.

#### CE
**Coulombic Efficiency**

The ratio of the total charge extracted from a battery to the total charge put into
the battery over a single cycle. Expressed as a percentage:

$$CE = \frac{Q_{discharge}}{Q_{charge}} \times 100\%$$

A perfect battery would have CE = 100%. Lower values indicate irreversible side
reactions consuming lithium ions.

#### DOD
**Depth of Discharge**

The percentage of total battery capacity that has been discharged. For example,
if a 1.1 Ah battery has discharged 0.55 Ah, the DOD is 50%. A DOD of 100% means
the battery is fully discharged.

#### IR
**Internal Resistance**

The opposition to the flow of electric current within a battery cell. Measured
in ohms (Ω). Internal resistance increases as a battery ages, reducing power
delivery capability and increasing heat generation.

#### RUL
**Remaining Useful Life**

The number of charge-discharge cycles remaining until a battery's State of Health
(SOH) drops below a defined threshold. In most BatteryML benchmarks, this threshold
is **80%** of nominal capacity.

$$RUL = Cycle_{EOL} - Cycle_{current}$$

#### SOC
**State of Charge**

The ratio of a battery's remaining capacity to its current full capacity, expressed
as a percentage. Analogous to a fuel gauge in a car.

$$SOC = \frac{C_{curr}}{C_{full}} \times 100\%$$

Requires **real-time** prediction during battery operation.

#### SOH
**State of Health**

The ratio of a battery's current full discharge capacity to its nominal capacity
when new, expressed as a percentage.

$$SOH = \frac{C_{full}}{C_{nom}} \times 100\%$$

A battery is typically considered end-of-life when SOH drops below **80%**.

---

### Battery Chemistry

#### LCO
**Lithium Cobalt Oxide** — LiCoO₂

A cathode material widely used in consumer electronics (smartphones, laptops).
Offers high energy density but lower thermal stability. Used in the **CALCE** and
**HNEI** datasets.

#### LFP
**Lithium Iron Phosphate** — LiFePO₄

A cathode material known for long cycle life, thermal stability, and safety.
Lower energy density than NMC or NCA. Used in the **MATR**, **HUST**, and some
**SNL** cells.

#### NCA
**Lithium Nickel Cobalt Aluminum Oxide** — LiNiCoAlO₂

A cathode material offering high energy density. Used extensively in Tesla vehicles.
Present in the **SNL** and **UL_PUR** datasets.

#### NMC
**Lithium Nickel Manganese Cobalt Oxide** — LiNiMnCoO₂

A cathode material balancing energy density, power, and cycle life. The most
common chemistry for EV batteries. Used in the **HNEI**, **RWTH**, and some
**SNL** cells.

---

### Degradation Mechanisms

#### SEI
**Solid Electrolyte Interphase**

A thin film that forms on the anode surface during the first few charge cycles and
continues to grow throughout battery life. SEI growth consumes lithium ions, reducing
available capacity. It is one of the primary degradation mechanisms in lithium-ion
batteries.

---

### Battery Testing & Lifecycle

#### BOL
**Begin-Of-Life**

The initial state of a battery before cycling begins. BOL tests measure the fresh
performance characteristics including capacity, resistance, and impedance as reference
baselines. Used in the **RWTH** dataset.

#### CC
**Constant Current**

A charging or discharging mode where the current is maintained at a fixed level.
For example, charging at 1C means charging at a rate that would theoretically fill
the battery in one hour.

#### CC/CV
**Constant Current / Constant Voltage**

The standard charging protocol for lithium-ion batteries:
1. **CC phase**: Charge at constant current until voltage limit is reached
2. **CV phase**: Hold voltage constant until current drops below a cutoff threshold

Example from CALCE: Charge at 0.5C to 4.2V, then hold 4.2V until current < 0.05A.

#### CV
**Constant Voltage**

A charging or discharging mode where the voltage is maintained at a fixed level.
Used in the second phase of CC/CV charging.

#### EOL
**End-Of-Life**

The point at which a battery is considered no longer suitable for its intended
application. Typically defined as when SOH drops below **80%** of nominal capacity,
though the threshold varies by application.

#### RPT
**Reference Performance Test**

A standardized test protocol used to measure a battery's true capacity under
controlled conditions. RPT involves charging and discharging at specific rates
and temperatures to produce comparable measurements across time. RPT data is
**often unavailable** in public datasets, requiring BatteryML to use approximate labels.

---

### Datasets

#### CALCE
**Center for Advanced Life Cycle Engineering**

A research center at the University of Maryland. Provides the CALCE dataset containing
**13 prismatic LCO cells** with full lifecycle data. Batteries cycled at 0.5C charge
rate to 4.2V.

#### CLO
**Closed-Loop Optimization**

A dataset derived from the MATR data source, specifically from the cells in
Attia et al. (2020). Contains LFP cells with various fast-charging strategies
optimized through closed-loop machine learning.

#### CRUH
**CALCE + RWTH + UL_PUR + HNEI** (Combined Dataset)

A combined dataset merging four smaller data sources to increase training data volume.
Contains cells from multiple chemistries (LCO, NMC, NCA).

#### CRUSH
**CALCE + RWTH + UL_PUR + SNL + HNEI** (Combined Dataset)

An extended combined dataset that includes SNL cells. In CRUSH, models predict the
**90% SOH point** from only the first **20 cycles**, a more challenging early
prediction task.

#### HNEI
**Hawaii Natural Energy Institute**

A research institute at the University of Hawaii. Provides a dataset of **14 commercial
18650 cells** with NMC+LCO blended cathode, cycled at 1.5C to 100% DOD.

#### HUST
**Huazhong University of Science and Technology**

A Chinese university. Provides a dataset of **77 LFP cells** (same model as MATR)
with identical charging but different multi-stage discharge protocols at 30°C.

#### MATR
**Massachusetts / Toyota Research** (informal name)

The largest publicly available battery cycling dataset, containing **180 commercial
18650 LFP cells**. Provided by Severson et al. (2019) and Attia et al. (2020). Split
into three sub-datasets:
- **MATR1**: Same charging policies in train and test (from Severson et al.)
- **MATR2**: Unseen charging policies in test (from Severson et al.)
- **CLO**: Random split across all MATR cells (from Attia et al.)

#### MIX
**All Datasets Combined**

The largest battery degradation dataset in BatteryML, combining cells from **all seven
data sources** (CALCE, MATR, HUST, HNEI, RWTH, SNL, UL_PUR). Used to test model
generalization across the widest range of chemistries and conditions.

#### RWTH
**Rheinisch-Westfälische Technische Hochschule Aachen**

A German university. Provides cycling records of **48 NMC/carbon cells**
(Sanyo/Panasonic UR18650E) aged under identical profiles with regular RPT measurements.

#### SNL
**Sandia National Laboratories**

A US Department of Energy research laboratory. Provides a dataset of **61 commercial
18650 cells** in NCA, NMC, and LFP chemistries, evaluating the impact of temperature,
DOD, and discharge current on degradation.

#### UL_PUR
**Underwriters Laboratories / Purdue University**

A collaboration providing **10 commercial NCA pouch cells** cycled at 1C within
2.7–4.2V at room temperature until 10–20% capacity fade.

---

### Machine Learning Methods

#### CNN
**Convolutional Neural Network**

A deep learning architecture originally designed for image recognition. In BatteryML,
it treats battery cycling data (cycles × voltage interpolation points) as a 2D
"image" to detect local degradation patterns. **Highly sensitive to random initialization.**

#### GP / GPR
**Gaussian Process / Gaussian Process Regression**

A non-parametric Bayesian machine learning approach that models data as samples from
a multivariate Gaussian distribution. Provides both predictions and **uncertainty
estimates**. Implemented via `GaussianProcessRegressor` in scikit-learn.

#### GRU
**Gated Recurrent Unit**

A type of recurrent neural network (RNN) designed to capture temporal dependencies.
Similar to LSTM but with a simpler architecture (fewer parameters). Features gating
mechanisms to control information flow without separate memory cells.

#### LGBM
**Light Gradient Boosting Machine** (LightGBM)

An efficient gradient boosted decision tree algorithm developed by Microsoft. Designed
for speed and low memory usage. **State-of-the-art for SOC prediction** in BatteryML
benchmarks. Supports both continuous and categorical features.

#### LSTM
**Long Short-Term Memory**

A type of recurrent neural network capable of learning long-term dependencies in
sequential data. Uses memory cells and gating mechanisms (input, forget, output gates)
to selectively remember or forget information. In BatteryML, an LSTM layer is followed
by a linear output layer. **Most robust neural network** in the benchmarks.

#### ML
**Machine Learning**

A branch of artificial intelligence focused on building systems that learn from data
to make predictions or decisions without being explicitly programmed.

#### MLP
**Multi-Layer Perceptron**

A class of feedforward artificial neural network consisting of multiple fully-connected
layers of neurons. The simplest deep learning architecture. In BatteryML, used as a
baseline neural model for battery degradation prediction.

#### PCA
**Principal Component Analysis**

A dimensionality reduction technique that transforms data into a set of orthogonal
(uncorrelated) components ordered by the amount of variance they explain. Used in
PCR to reduce feature dimensionality before regression.

#### PCR
**Principal Component Regression**

A regression method that combines PCA for dimensionality reduction with linear
regression. Focuses the regression on the most significant data variations. In BatteryML,
implemented as a pipeline of PCA + LinearRegression in scikit-learn. **Best on MATR1**
(RMSE = 90).

#### PLSR
**Partial Least Squares Regression**