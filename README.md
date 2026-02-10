# 🧪 Aloe Vera Bioactive Extraction Optimizer: A Circular Bioeconomy Approach

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aloe-extraction-optimization.streamlit.app/)

## 💎 Project Overview & Intellectual Property
This project showcases the digital transformation of a **patented extraction process** (of which I am a co-inventor) designed to valorize *Aloe vera* processing by-products. By applying **Circular Economy** principles, we transform discarded Aloe rind into a high-value cosmetic ingredient.

### Key Innovations:
* **Patented Technology:** Co-inventor of the industrial method for standardized aloesin extraction.
   🔗 [**Open Patent**](https://bibliotecadigital.ipb.pt/entities/publication/8920c345-be5f-428e-a336-db9ca26c4b81)
* **Green Chemistry:** Optimized use of "Generally Recognized as Safe" (GRAS) alternative solvents: Ethanol, Propylene Glycol, and Glycerol.
* **Target Bioactivity:** Extracts optimized for skin-depigmenting formulations due to their potent **anti-tyrosinase activity**.

## 🌿 Scientific Background
The industrial processing of *Aloe vera* (L.) Burm. f. generates vast amounts of rind as a byproduct. This project uses **Response Surface Methodology (RSM)** to bridge the gap between laboratory research and industrial application.

> **Reference:** [Añibarro-Ortega, M., et al. (2021). *Biology*, 10(10), 951.](https://doi.org/10.3390/biology10100951)

## 📊 Technical Methodology
The optimization was performed using a Central Composite Circumscribed Design (CCRD) to maximize the recovery of Aloesin, which was precisely quantified using HPLC-DAD-ESI/MS$^n$.

Target Response:
Aloesin Content: Expressed in mg/g of extract.

Process Variables:
1. **Time** ($t$): 10–210 min
2. **Temperature** ($T$): 25–95 °C
3. **Solvent Concentration** ($S$): 0–100 % (w/w)

### Validated Optimization Models

| Solvent System | Time (min) | Temp (°C) | Solvent (%) | Max Yield<sub>(pred)</sub> (mg/g) | Max Yield<sub>(exp)</sub> (mg/g) | R<sup>2</sup><sub>adj</sub> |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ethanol/Water** | 92.9 | 55.9 | 0.0 | 48 &plusmn; 1 | 51 &plusmn; 1 | 0.9862 |
| **Propylene Glycol/Water** | 12.0 | 60.6 | 51.1 | 63 &plusmn; 1 | 65 &plusmn; 1 | 0.8976 |
| **Glycerol/Water** | 42.2 | 56.8 | 17.5 | 57 &plusmn; 1 | 61 &plusmn; 1 | 0.8699 |

## 🚀 Business & Industrial Impact
* **Waste Valorization:** Converts a low-cost byproduct into a high-margin cosmetic active.
* **Cost Reduction:** Identifies precise T/t thresholds to optimize ROI and energy consumption.
* **Proven Innovation:** Based on a patented process, ensuring a unique competitive advantage.

## 🛠️ Tech Stack
* **Python 3.x**
* **Streamlit** (Interactive Dashboard)
* **Statsmodels** (OLS Regression & Cubic Modeling)
* **Plotly** (3D Surface Visualization)
