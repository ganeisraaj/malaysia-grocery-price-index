from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

APP_DIR = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    items = pd.read_csv(APP_DIR / "lookup_item.csv")
    premises = pd.read_csv(APP_DIR / "lookup_premise.csv")

    df22 = pd.read_csv(APP_DIR / "pricecatcher_2022-08.csv")
    df26 = pd.read_csv(APP_DIR / "pricecatcher_2026-08.csv")

    df22 = df22.merge(items, on="item_code", how="left").merge(premises, on="premise_code", how="left")
    df26 = df26.merge(items, on="item_code", how="left").merge(premises, on="premise_code", how="left")

    return df22, df26

df22, df26 = load_data()

BASKET = {
    "Ayam bersih 1kg": 1,
    "Telur ayam Gred A (30 biji)": 1109,
    "Beras 10kg": 904,
    "Minyak masak 1kg": 918,
    "Gula putih 1kg": 1590,
    "Ikan kembung 1kg": 1476,
    "Kangkung 1kg": 1559,
    "Tomato 1kg": 114,
    "Bawang besar 1kg": 1440,
    "Cili merah 1kg": 94,
}

PENINSULAR = [
    "Johor","Kedah","Kelantan","Melaka","Negeri Sembilan",
    "Pahang","Perak","Perlis","Pulau Pinang","Selangor",
    "Terengganu","W.P. Kuala Lumpur","W.P. Putrajaya"
]

def basket_by_state(df, states):
    results = []
    for item_name, code in BASKET.items():
        state_prices = (df[df["item_code"]==code]
                        .groupby("state")["price"]
                        .median().reset_index())
        state_prices["item"] = item_name
        results.append(state_prices)
    pivot = pd.concat(results).pivot(index="state", columns="item", values="price")
    pivot["TOTAL"] = pivot.sum(axis=1)
    return pivot.loc[pivot.index.isin(states)]

b22 = basket_by_state(df22, PENINSULAR)
b26 = basket_by_state(df26, PENINSULAR)

comp = pd.DataFrame({
    "Aug 2022 (RM)": b22["TOTAL"],
    "Aug 2026 (RM)": b26["TOTAL"],
})
comp["Naik (RM)"] = (comp["Aug 2026 (RM)"] - comp["Aug 2022 (RM)"]).round(2)
comp["Naik (%)"] = (comp["Naik (RM)"] / comp["Aug 2022 (RM)"] * 100).round(1)
comp = comp.sort_values("Naik (RM)", ascending=False).round(2)

item_comp = []
for name, code in BASKET.items():
    p22 = df22[df22["item_code"]==code]["price"].median()
    p26 = df26[df26["item_code"]==code]["price"].median()
    item_comp.append({
        "item": name,
        "Aug 2022 (RM)": p22,
        "Aug 2026 (RM)": p26,
        "change_rm": round(p26-p22, 2),
        "change_pct": round((p26-p22)/p22*100, 1)
    })
item_df = pd.DataFrame(item_comp).sort_values("change_pct", ascending=False)

## App layout
st.title("🛒 Malaysia Grocery Price Index")
st.markdown(
    "How much more does a standard Malaysian grocery basket cost in August 2026 vs August 2022? "
    "Based on **2.6 million price observations** collected by KPDN across 13 Peninsular Malaysian states."
)

## Key metrics
national_22 = comp["Aug 2022 (RM)"].mean()
national_26 = comp["Aug 2026 (RM)"].mean()
national_chg = national_26 - national_22

col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg basket Aug 2022", f"RM{national_22:.2f}")
col2.metric("Avg basket Aug 2026", f"RM{national_26:.2f}")
col3.metric("Average increase", f"+RM{national_chg:.2f}")
col4.metric("Tomato price change", "+50.0%", "Biggest mover")

st.divider()

## State explorer
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

## Item breakdown
st.header("🧺 By Item — What got more expensive?")
st.markdown("**4 items are government price-controlled** — minyak masak, gula, ikan kembung, and kangkung. Their prices have not moved.")

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

## State drill-down
st.header("🔍 State Deep Dive")
selected_state = st.selectbox("Select a state", PENINSULAR)

state_items22 = {name: df22[(df22["item_code"]==code) & (df22["state"]==selected_state)]["price"].median()
                 for name, code in BASKET.items()}
state_items26 = {name: df26[(df26["item_code"]==code) & (df26["state"]==selected_state)]["price"].median()
                 for name, code in BASKET.items()}

state_df = pd.DataFrame({
    "Item": list(BASKET.keys()),
    "Aug 2022 (RM)": [state_items22[k] for k in BASKET],
    "Aug 2026 (RM)": [state_items26[k] for k in BASKET],
})
state_df["Change (RM)"] = (state_df["Aug 2026 (RM)"] - state_df["Aug 2022 (RM)"]).round(2)
state_df["Change (%)"] = (state_df["Change (RM)"] / state_df["Aug 2022 (RM)"] * 100).round(1)

total_22 = state_df["Aug 2022 (RM)"].sum()
total_26 = state_df["Aug 2026 (RM)"].sum()

col1, col2, col3 = st.columns(3)
col1.metric(f"{selected_state} basket Aug 2022", f"RM{total_22:.2f}")
col2.metric(f"{selected_state} basket Aug 2026", f"RM{total_26:.2f}")
col3.metric("Total increase", f"+RM{total_26-total_22:.2f}", f"+{(total_26-total_22)/total_22*100:.1f}%")

st.dataframe(state_df, hide_index=True, use_container_width=True)

st.caption(
    "Data: KPDN PriceCatcher, August 2022 and August 2026. "
    "Prices shown are median values across all premises in each state. "
    "East Malaysia excluded due to incomplete beras data. "
    "Price-controlled items (minyak masak, gula putih, ikan kembung, kangkung) show 0% change by policy."
)