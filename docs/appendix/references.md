# References

Key papers and resources cited in the BatteryML paper, organized by topic.

---

## The BatteryML Paper

- **Zhang, H., Gui, X., Zheng, S., Lu, Z., Li, Y., & Bian, J.** (2024).
  BatteryML: An Open-Source Platform for Machine Learning on Battery Degradation.
  *International Conference on Learning Representations (ICLR)*.
  [arXiv:2310.14714](https://arxiv.org/abs/2310.14714)
  [GitHub](https://github.com/microsoft/BatteryML)

---

## Foundational Battery ML Papers

| Paper | Year | Key Contribution |
|-------|------|------------------|
| Severson et al. "Data-driven prediction of battery cycle life before capacity degradation" | 2019 | Introduced the MATR dataset and key features (Variance, Discharge models) |
| Attia et al. "Statistical learning for accurate and interpretable battery lifetime prediction" | 2021 | Feature engineering for battery life prediction; QdLinear features |
| Attia et al. "Closed-loop optimization of fast-charging protocols for batteries with machine learning" | 2020 | Demonstrated ML-driven battery optimization |
| Ma et al. "Real-time personalized health status prediction of lithium-ion batteries using deep transfer learning" | 2022 | HUST dataset; transfer learning for battery health |

---

## Battery Degradation Science

| Paper | Year | Key Contribution |
|-------|------|------------------|
| Edge et al. "Lithium ion battery degradation: what you need to know" | 2021 | Comprehensive review of degradation mechanisms |
| Hu et al. "Battery lifetime prognostics" | 2020 | Review of battery lifetime prediction approaches |
| Pop et al. "Battery aging and its influence on the electromotive force" | 2007 | Fundamental aging mechanisms |
| Dubarry et al. "Synthesize battery degradation modes via a diagnostic and prognostic model" | 2012 | Degradation mode analysis |
| Palacín. "Understanding ageing in Li-ion batteries: a chemical issue" | 2018 | Chemical perspective on battery aging |

---

## Datasets

| Paper | Year | Dataset |
|-------|------|---------|
| Xing et al. | 2013 | CALCE |
| He et al. | 2011 | CALCE |
| Severson et al. | 2019 | MATR (batches 1-2) |
| Attia et al. | 2020 | MATR (CLO batch) |
| Ma et al. | 2022 | HUST |
| Devie et al. | 2018 | HNEI |
| Preger et al. | 2020 | SNL |
| Juarez-Robles et al. | 2020, 2021 | UL_PUR |
| Li et al. | 2021 | RWTH |

---

## Machine Learning Methods

### Linear & Statistical Models
| Paper | Year | Method |
|-------|------|--------|
| Hoerl & Kennard | 2000 | Ridge Regression |
| Tipping & Bishop | 1999 | Principal Component Regression |
| Geladi & Kowalski | 1986 | Partial Least Squares Regression |
| Williams & Rasmussen | 2006 | Gaussian Process |
| Zou & Hastie | 2005 | Elastic Net |

### Tree-Based Models
| Paper | Year | Method |
|-------|------|--------|
| Chen & Guestrin | 2016 | XGBoost |
| Ke et al. | 2017 | LightGBM |
| Breiman | 2001 | Random Forest |
| Geurts et al. | 2006 | Extremely Randomized Trees |

### Neural Networks
| Paper | Year | Method |
|-------|------|--------|
| Haykin | 1994 | Multi-Layer Perceptron |
| Krizhevsky et al. | 2012 | Convolutional Neural Networks |
| Hochreiter & Schmidhuber | 1997 | Long Short-Term Memory (LSTM) |
| Cho et al. | 2014 | Gated Recurrent Unit (GRU) |
| Vaswani et al. | 2017 | Transformer |

### Frameworks
| Paper | Year | Tool |
|-------|------|------|
| Pedregosa et al. | 2011 | scikit-learn |
| Paszke et al. | 2019 | PyTorch |

---

## Related Platforms

| Paper | Year | Platform |
|-------|------|----------|
| Herring et al. "BEEP: A Python library for battery evaluation and early prediction" | 2020 | BEEP |

---

## Battery SOH/SOC/RUL Estimation

| Paper | Year | Focus |
|-------|------|-------|
| Lipu et al. | 2018 | Review of SOH and RUL methods for EVs |
| Ng et al. | 2020 | Data-driven SOC and SOH prediction |
| Chemali et al. | 2018 | Deep neural networks for SOC estimation |
| Lu et al. | 2023 | Deep learning for SOH without degradation experiments |
| Rauf et al. | 2022 | ML in SOH and RUL estimation review |
| Li et al. | 2019 | Data-driven health estimation and lifetime prediction review |
| Meng & Li | 2019 | Prognostics and health management review |

---

## Data-Driven Battery Modeling

| Paper | Year | Focus |
|-------|------|-------|
| Zhang et al. | 2020 | Identifying degradation from impedance spectroscopy using ML |
| Zhang et al. | 2018 | LSTM for RUL prediction |
| Wu et al. | 2018 | Artificial neural networks for lithium-ion battery design |
| Ren et al. | 2018 | Deep learning for RUL prediction |
| Li et al. | 2020 | Data-driven battery modeling with aging phenomena |
| Hong et al. | 2020 | End-to-end deep learning for RUL prediction |

---

## Physical and Semi-Empirical Models

| Paper | Year | Focus |
|-------|------|-------|
| Das et al. | 2019 | Electrochemical kinetics of SEI growth |
| Doyle et al. | 1993 | Galvanostatic charge/discharge modeling |
| Plett | 2004 | Extended Kalman filtering for BMS |
| Wang et al. | 2011 | Cycle-life model for graphite-LiFePO₄ cells |
| Waldmann et al. | 2014, 2015 | Mechanical aging mechanisms |