from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

APP_DIR = Path(__file__).resolve().parent

PENINSULAR = [
    "Johor","Kedah","Kelantan","Melaka","Negeri Sembilan",
    "Pahang","Perak","Perlis","Pulau Pinang","Selangor",
    "Terengganu","W.P. Kuala Lumpur","W.P. Putrajaya"
]

BASKET = [
    "Ayam bersih 1kg",
    "Telur ayam Gred A (30 biji)",
    "Beras Super Cap Rambutan 5% Import, 10kg",
    "Minyak masak 1kg",
    "Gula putih 1kg",
    "Ikan kembung 1kg",
    "Kangkung 1kg",
    "Tomato 1kg",
    "Bawang besar 1kg",
    "Cili merah minyak, 1kg",
]

@st.cache_data
def load_data():
    basket = pd.read_csv(APP_DIR / "basket_aggregated.csv")
    items = pd.read_csv(APP_DIR / "item_national_aggregated.csv")
    return basket, items

basket_df, item_df = load_data()

df22 = basket_df[basket_df["year"]==2022]
df26 = basket_df[basket_df["year"]==2026]

# Basket totals by state
def basket_totals(df, states):
    pivot = df[df["state"].isin(states)].pivot(index="state", columns="item", values="price")
    pivot["TOTAL"] = pivot.sum(axis=1)
    return pivot

b22 = basket_totals(df22, PENINSULAR)
b26 = basket_totals(df26, PENINSULAR)

comp = pd.DataFrame({
    "Aug 2022 (RM)": b22["TOTAL"],
    "Aug 2026 (RM)": b26["TOTAL"],
}).dropna()
comp["Naik (RM)"] = (comp["Aug 2026 (RM)"] - comp["Aug 2022 (RM)"]).round(2)
comp["Naik (%)"] = (comp["Naik (RM)"] / comp["Aug 2022 (RM)"] * 100).round(1)
comp = comp.sort_values("Naik (RM)", ascending=False).round(2)

## App
st.title("🛒 Malaysia Grocery Price Index")
st.markdown(
    "How much more does a standard Malaysian grocery basket cost in August 2026 vs August 2022? "
    "Based on **4.6 million KPDN PriceCatcher records** from August 2022 and August 2026, "
    "across 13 Peninsular states and federal territories. "
    "This is a custom basket analysis, not an official inflation index."
)

national_22 = comp["Aug 2022 (RM)"].mean()
national_26 = comp["Aug 2026 (RM)"].mean()
national_chg = national_26 - national_22

col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg basket Aug 2022", f"RM{national_22:.2f}")
col2.metric("Avg basket Aug 2026", f"RM{national_26:.2f}")
col3.metric("Average increase", f"+RM{national_chg:.2f}")
col4.metric("Biggest mover", "Tomato +50%")

st.divider()

st.header("🗺️ By State — Which state felt it most?")

fig1, ax1 = plt.subplots(figsize=(10, 6))
comp_sorted = comp.sort_values("Naik (RM)")
ax1.barh(comp_sorted.index, comp_sorted["Naik (RM)"], color="tomato")
ax1.set_xlabel("Increase in basket cost (RM)")
for i, (state, row) in enumerate(comp_sorted.iterrows()):
    ax1.text(row["Naik (RM)"] + 0.1, i, f'+RM{row["Naik (RM)"]:.2f}', va="center", fontsize=9)
plt.tight_layout()
st.pyplot(fig1)

st.dataframe(
    comp.rename(columns={"Naik (RM)": "Increase (RM)", "Naik (%)": "Increase (%)"}),
    use_container_width=True
)

st.divider()

st.header("🧺 By Item — What got more expensive?")
st.markdown(
    "Some items in this basket showed little or no price change over this period. "
    "The basket includes controlled or subsidised staples such as 1kg packet cooking oil and refined white sugar."
)

fig2, ax2 = plt.subplots(figsize=(10, 6))
item_sorted = item_df.sort_values("change_pct")
colors = ["tomato" if x > 0 else "steelblue" for x in item_sorted["change_pct"]]
ax2.barh(item_sorted["item"], item_sorted["change_pct"], color=colors)
ax2.axvline(0, color="black", linewidth=0.8)
ax2.set_xlabel("Price change (%)")
for i, row in enumerate(item_sorted.itertuples()):
    label = f'{row.change_pct:+.1f}%'
    x = row.change_pct + 0.5 if row.change_pct >= 0 else row.change_pct - 0.5
    ha = "left" if row.change_pct >= 0 else "right"
    ax2.text(x, i, label, va="center", fontsize=9, ha=ha)
plt.tight_layout()
st.pyplot(fig2)

st.dataframe(
    item_df[["item","Aug 2022 (RM)","Aug 2026 (RM)","change_rm","change_pct"]].rename(columns={
        "change_rm": "Change (RM)", "change_pct": "Change (%)"
    }),
    hide_index=True,
    use_container_width=True
)

st.divider()

st.header("🔍 State Deep Dive")
selected_state = st.selectbox("Select a state", PENINSULAR)

state_22 = df22[df22["state"]==selected_state].set_index("item")["price"]
state_26 = df26[df26["state"]==selected_state].set_index("item")["price"]

state_items = list(state_22.index.union(state_26.index))

state_df = pd.DataFrame({
    "Item": state_items,
    "Aug 2022 (RM)": [state_22.get(k, np.nan) for k in state_items],
    "Aug 2026 (RM)": [state_26.get(k, np.nan) for k in state_items],
})
state_df["Change (RM)"] = (state_df["Aug 2026 (RM)"] - state_df["Aug 2022 (RM)"]).round(2)
state_df["Change (%)"] = (state_df["Change (RM)"] / state_df["Aug 2022 (RM)"] * 100).round(1)

total_22 = state_df["Aug 2022 (RM)"].sum()
total_26 = state_df["Aug 2026 (RM)"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Basket Aug 2022", f"RM{total_22:.2f}")
col2.metric("Basket Aug 2026", f"RM{total_26:.2f}")
col3.metric("Total increase", f"+RM{total_26-total_22:.2f}",
            f"+{(total_26-total_22)/total_22*100:.1f}%")

st.dataframe(state_df, hide_index=True, use_container_width=True)

st.caption(
    "Data: KPDN PriceCatcher via data.gov.my, August 2022 and August 2026. "
    "Prices are median values from raw PriceCatcher observations. "
    "State basket totals use median price per item per state. "
    "National item figures use median across all raw observations. "
    "Sabah, Sarawak and Labuan excluded: the selected 10kg rice item did not provide "
    "complete comparable coverage across both periods. "
    "This is a custom basket analysis, not an official inflation measure."
)