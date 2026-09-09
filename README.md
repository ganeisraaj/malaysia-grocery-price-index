# Malaysia Grocery Price Index

A starter project for exploring Malaysia PriceCatcher grocery prices across August 2022 and August 2026.

## Project layout

- `streamlit/`: Streamlit app, dependencies, and local CSV data files
- `notebooks/01_analysis.ipynb`: Initial data loading and summary analysis
- `data/`: Reserved for source data and ignored by Git

The CSV files are intentionally ignored because they are large. The app reads them directly from `streamlit/`.

## Run the Streamlit app

From the project root:

```powershell
cd streamlit
python -m pip install -r requirements.txt
streamlit run app.py
```

The app expects these files beside `app.py`:

- `pricecatcher_2022-08.csv`
- `pricecatcher_2026-08.csv`
- `lookup_item.csv`
- `lookup_premise.csv`
