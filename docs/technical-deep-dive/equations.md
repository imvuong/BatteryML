# Key Equations

BatteryML uses two primary equations to define battery health metrics,
which serve as prediction labels.

---

## Equation 1: State of Health (SOH)

### Formula

$$\text{SOH} = \frac{C_{\text{full}}}{C_{\text{nom}}} \times 100\%$$

### Variables

| Variable | Meaning | Unit |
|----------|---------|------|
| SOH | State of Health | Percentage (%) |
| $$C_{\text{full}}$$ | Full discharge capacity in the current cycle | Amp-hours (Ah) |
| $$C_{\text{nom}}$$ | Nominal (rated) capacity when new | Amp-hours (Ah) |

### Example Calculation

A battery with:
- Nominal capacity: **1.1 Ah**
- Current full discharge capacity: **0.88 Ah**

$$\text{SOH} = \frac{0.88}{1.1} \times 100\% = 80\%$$

This battery is at the typical **end-of-life threshold** (80%).

### Important Notes

- $$C_{\text{full}}$$ should ideally be measured under the **same discharge protocol** as the nominal
  capacity (Reference Performance Test conditions)
- In practice, RPT conditions are often **unavailable**, requiring approximations
- SOH decreases monotonically over a battery's lifetime (with noise)

---

## Equation 2: State of Charge (SOC)

### Formula

$$\text{SOC} = \frac{C_{\text{curr}}}{C_{\text{full}}} \times 100\%$$

### Variables

| Variable | Meaning | Unit |
|----------|---------|------|
| SOC | State of Charge | Percentage (%) |
| $$C_{\text{curr}}$$ | Remaining capacity at the current moment | Amp-hours (Ah) |
| $$C_{\text{full}}$$ | Current full capacity of the battery | Amp-hours (Ah) |

### Example Calculation

A battery with:
- Current full capacity: **0.88 Ah**
- Remaining capacity right now: **0.44 Ah**

$$\text{SOC} = \frac{0.44}{0.88} \times 100\% = 50\%$$

The battery is **half charged**.

### Important Notes

- When depth of discharge is 100% and BMS has recorded discharged capacity,
  SOC is equivalent to SOH
- Estimation becomes more challenging with **partial discharge** (DOD < 100%)
- Requires **real-time** prediction capabilities

---

## Relationship Between SOH and SOC

SOH tells you:  "The battery's MAXIMUM capacity has degraded from 1.1 Ah to 0.88 Ah"
SOC tells you:  "Of that 0.88 Ah, you currently have 0.44 Ah remaining"

SOC depends on SOH — you need to know the current full capacity to compute
the charge percentage.

---

## RUL Definition

While not expressed as a single equation, RUL is defined as:

$$\text{RUL} = \text{Cycle}_{\text{EOL}} - \text{Cycle}_{\text{current}}$$

Where $$\text{Cycle}_{\text{EOL}}$$ is the cycle number when SOH first drops below the threshold
(typically 80% of nominal capacity).

### Typical Thresholds

| Application | SOH Threshold | Justification |
|------------|---------------|---------------|
| Standard RUL | 80% | Industry convention |
| CRUSH dataset | 90% | Earlier prediction point |
| Custom | User-defined | Application-specific |