# 🛒 Malaysia Grocery Price Index
**Indeks Harga Runcit Malaysia**

---

## 🚀 Live App

👉 **[Malaysia Grocery Price Index — Live App](https://ganeisraaj-malaysia-grocery-price-index.streamlit.app/)**

Compare a standard Malaysian grocery basket across 13 Peninsular states and federal territories and see what got more expensive between August 2022 and August 2026.

---

## Overview

Malaysia's headline inflation figures often mask what is actually happening at the market level. This project uses raw price data collected by KPDN across thousands of premises to answer one simple question:

**How much more does the same grocery basket cost in 2026 compared to 2022?**

The basket covers 10 essential items — chicken, eggs, rice, cooking oil, sugar, fish, vegetables, and condiments. Data comes from KPDN PriceCatcher, which collects daily prices from wet markets, supermarkets, and sundry shops across Malaysia.

This is a custom basket analysis based on PriceCatcher medians. It is not an official inflation index.

---

## Key Findings

- The same 10-item basket costs **RM5 to RM11 more** depending on which state you live in
- **W.P. Kuala Lumpur** saw the biggest increase at **+RM10.89 (+10.2%)**
- **Kelantan** saw the smallest increase at **+RM5.08 (+4.6%)**
- Same basket. Same four years. More than 2x the increase depending on where you live.
- **Tomato prices rose 50%** — from RM6.00 to RM9.00 per kg nationally
- **Beras Super Cap Rambutan 5% Import (10kg) rose 24.1%** — from RM29.00 to RM36.00
- Some items showed little or no price change — the basket includes controlled and subsidised staples such as 1kg packet cooking oil and refined white sugar
- **Cili merah minyak actually became cheaper** — down 23.5% from RM16.99 to RM12.99

---

## The Basket

| Item | Unit | Aug 2022 (RM) | Aug 2026 (RM) | Change |
|---|---|---|---|---|
| Ayam bersih | 1kg | 8.49 | 9.29 | +9.4% |
| Telur ayam Gred A | 30 biji | 13.50 | 14.70 | +8.9% |
| Beras Super Cap Rambutan 5% Import | 10kg | 28.99 | 35.99 | +24.1% |
| Minyak masak (paket) | 1kg | 2.50 | 2.50 | 0.0% |
| Gula putih bertapis halus | 1kg | 2.95 | 2.95 | 0.0% |
| Ikan kembung | 1kg | 16.00 | 16.00 | 0.0% |
| Kangkung | 1kg | 5.00 | 5.00 | 0.0% |
| Tomato | 1kg | 6.00 | 9.00 | +50.0% |
| Bawang besar import | 1kg | 3.50 | 3.19 | -8.9% |
| Cili merah minyak | 1kg | 16.99 | 12.99 | -23.5% |

---

## Data

| | |
|---|---|
| **Source** | KPDN PriceCatcher via data.gov.my |
| **Coverage** | 13 Peninsular states and federal territories |
| **Observations** | 2,664,356 (Aug 2022) + 1,933,285 (Aug 2026) = **4,597,641 total** |
| **Premise types** | Wet markets, supermarkets, hypermarkets, sundry shops |
| **Price metric** | Median price per state per item (state breakdown); median across all raw observations (national item figures) |

Sabah, Sarawak and Labuan were excluded because the selected 10kg rice item did not provide complete comparable coverage across both periods.

---

## Methods

- Median price used per state per item — robust to outliers from individual premises
- National item-level figures computed from all raw PriceCatcher observations, not from state medians
- Basket total per state = sum of median item prices across all 10 basket items
- Raw data pre-aggregated before deployment — 4.6 million rows condensed to 309 summary rows for the state comparison and 20 rows for the national item comparison
- This is a custom basket analysis, not an official inflation measure. data.gov.my explicitly notes that PriceCatcher is not designed as a substitute for CPI.

---

## Reproducing the Analysis

The raw data files are not tracked in this repository due to size. To reproduce the full analysis:

1. Download the following files from [data.gov.my](https://data.gov.my):
   - `pricecatcher_2022-08.csv`
   - `pricecatcher_2026-08.csv`
   - `lookup_item.csv`
   - `lookup_premise.csv`
2. Place them in the `data/` folder
3. Run `notebooks/01_analysis.ipynb`

The pre-aggregated output files (`basket_aggregated.csv` and `item_national_aggregated.csv`) used by the Streamlit app are already included in the `streamlit/` folder.

---

## Software

Python 3.12 · `pandas` · `numpy` · `matplotlib` · `streamlit`
