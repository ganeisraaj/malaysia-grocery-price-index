# 🛒 Malaysia Grocery Price Index
**Indeks Harga Runcit Malaysia**

---

## 🚀 Live App

👉 **[Malaysia Grocery Price Index — Live App](https://ganeisraaj-malaysia-grocery-price-index.streamlit.app/)**

Compare a standard Malaysian grocery basket across 13 Peninsular states and see what got more expensive between August 2022 and August 2026.

---

## Overview

Malaysia's headline inflation figures often mask what is actually happening at the market level. This project uses raw price data collected by KPDN across thousands of premises to answer one simple question:

**How much more does the same grocery basket cost in 2026 compared to 2022?**

The basket covers 10 essential items — chicken, eggs, rice, cooking oil, sugar, fish, vegetables, and condiments. Data comes from KPDN PriceCatcher, which collects daily prices from wet markets, supermarkets, and sundry shops across Malaysia.

---

## Key Findings

- The same 10-item basket costs **RM5 to RM11 more** depending on which state you live in
- **W.P. Kuala Lumpur** saw the biggest increase at **+RM10.89 (+10.2%)**
- **Kelantan** saw the smallest increase at **+RM5.08 (+4.6%)**
- **Tomato prices rose 50%** — from RM6.00 to RM9.00 per kg nationally
- **Beras (rice) rose 24.1%** — from RM29.00 to RM36.00 for 10kg
- **4 items showed zero price change** — minyak masak, gula putih, ikan kembung, and kangkung are government price-controlled
- **Cili merah actually became cheaper** — down 23.5% from RM16.99 to RM12.99

---

## The Basket

| Item | Unit | Aug 2022 (RM) | Aug 2026 (RM) | Change |
|---|---|---|---|---|
| Ayam bersih | 1kg | 8.49 | 9.29 | +9.4% |
| Telur ayam Gred A | 30 biji | 13.50 | 14.70 | +8.9% |
| Beras | 10kg | 28.99 | 35.99 | +24.1% |
| Minyak masak | 1kg | 2.50 | 2.50 | 0.0% ✓ |
| Gula putih | 1kg | 2.95 | 2.95 | 0.0% ✓ |
| Ikan kembung | 1kg | 16.00 | 16.00 | 0.0% ✓ |
| Kangkung | 1kg | 5.00 | 5.00 | 0.0% ✓ |
| Tomato | 1kg | 6.00 | 9.00 | +50.0% |
| Bawang besar | 1kg | 3.50 | 3.19 | -8.9% |
| Cili merah | 1kg | 16.99 | 12.99 | -23.5% |

✓ Government price-controlled items

---

## Data

| | |
|---|---|
| **Source** | KPDN PriceCatcher via data.gov.my |
| **Coverage** | 13 Peninsular Malaysian states |
| **Observations** | 2,664,356 (Aug 2022) + 1,933,285 (Aug 2026) |
| **Premise types** | Wet markets, supermarkets, hypermarkets, sundry shops |
| **Price metric** | Median price per state per item |

East Malaysia (Sabah, Sarawak, Labuan) excluded due to incomplete beras data in the dataset.

---

## Methods

- Median price used per state per item — robust to outliers from individual premises
- Peninsular states only for comparability
- Basket total computed as sum of median prices across all 10 items
- Raw data pre-aggregated before deployment — 4.6 million rows condensed to 309 summary rows
- Price-controlled items confirmed by KPDN official price control list

---

## Software

Python 3.12 · `pandas` · `numpy` · `matplotlib` · `streamlit`
