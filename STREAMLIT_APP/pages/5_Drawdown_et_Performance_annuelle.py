import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Performance & Drawdown",
    page_icon="📉",
    layout="wide"
)

# ---------------------------------------------------------
# 🔧 Chargement des données
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/DATASET_BTC.csv")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")
    df = df.sort_values("Timestamp")

    # Variables dérivées
    df["Return"] = df["Close"].pct_change()
    df["Volatility"] = df["High"] - df["Low"]
    df["Year"] = df["Timestamp"].dt.year

    # Daily
    df_daily = df.resample("D", on="Timestamp").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

    df_daily["Return"] = df_daily["Close"].pct_change()
    df_daily["Volatility"] = df_daily["High"] - df_daily["Low"]
    df_daily["Year"] = df_daily.index.year

    # Peak & Drawdown
    df_daily["Peak"] = df_daily["Close"].cummax()
    df_daily["Drawdown_pct"] = (df_daily["Close"] - df_daily["Peak"]) / df_daily["Peak"] * 100

    return df, df_daily

df_raw, df_daily = load_data()

# ---------------------------------------------------------
# 🟦 TITRE
# ---------------------------------------------------------
st.title("Performance annuelle & Drawdown du Bitcoin")

st.markdown("""
Cette page met en avant le **comportement long terme** du Bitcoin :
- performance annuelle en pourcentage,
- volatilité moyenne par année,
- drawdown (baisse maximale depuis le dernier plus haut).
""")

# ---------------------------------------------------------
# 🎛️ Filtres
# ---------------------------------------------------------
years = sorted(df_daily["Year"].unique())
selected_years = st.sidebar.multiselect(
    "📅 Années à inclure :", years, default=years
)

df_d = df_daily[df_daily["Year"].isin(selected_years)].copy()

# ---------------------------------------------------------
# 📊 Performance annuelle
# ---------------------------------------------------------
st.subheader("Performance annuelle (%)")

# Rendement annuel basé sur Close (1er jan -> 31 déc)
yearly_close = df_d.groupby("Year")["Close"].agg(["first", "last"])
yearly_return = (yearly_close["last"] / yearly_close["first"] - 1) * 100
yearly_return = yearly_return.reset_index().rename(columns={0: "Return_pct", "index": "Year"})
yearly_return = yearly_return.rename(columns={0: "Return_pct"})

yearly_return_df = yearly_return.rename(columns={"Close": "Return_pct"})
yearly_return_df["Return_pct"] = yearly_return[0] if 0 in yearly_return.columns else yearly_return.iloc[:, -1]

# petite correction plus simple :
yearly_perf = (yearly_close["last"] / yearly_close["first"] - 1) * 100
perf_df = yearly_perf.reset_index().rename(columns={0: "Return_pct", "last": "last"})
perf_df = perf_df.rename(columns={perf_df.columns[1]: "Return_pct"})

fig_perf = px.bar(
    perf_df,
    x="Year",
    y="Return_pct",
    labels={"Return_pct": "Performance (%)", "Year": "Année"},
    title="Performance annuelle du Bitcoin (%)",
    color="Return_pct",
    color_continuous_scale="RdYlGn"
)
st.plotly_chart(fig_perf, use_container_width=True)

st.markdown("""
💡 **Interprétation rapide :**  
- barres vertes : années en forte hausse (bull market),  
- barres rouges : années en baisse (bear market).
""")

# ---------------------------------------------------------
# ⚡ Volatilité annuelle
# ---------------------------------------------------------
st.subheader("Volatilité journalière moyenne par année")

yearly_vol = df_d.groupby("Year")["Volatility"].mean()
vol_df = yearly_vol.reset_index().rename(columns={"Volatility": "Volatilité_moyenne"})

fig_vol = px.bar(
    vol_df,
    x="Year",
    y="Volatilité_moyenne",
    labels={"Volatilité_moyenne": "Volatilité (moyenne daily en $)", "Year": "Année"},
    title="Volatilité moyenne du Bitcoin par année"
)
st.plotly_chart(fig_vol, use_container_width=True)

st.markdown("""
💡 **Volatilité annuelle :**  
Plus la barre est haute, plus le Bitcoin a bougé fortement au cours de l'année 
(amplitude High-Low journalière en moyenne).
""")

# ---------------------------------------------------------
# 📉 Courbe de Drawdown
# ---------------------------------------------------------
st.subheader("Drawdown du Bitcoin (%)")

fig_dd = px.area(
    df_d.reset_index(),
    x="Timestamp",
    y="Drawdown_pct",
    labels={"Drawdown_pct": "Drawdown (%)", "Timestamp": "Date"},
    title="Drawdown du Bitcoin (baisse par rapport au dernier plus haut)"
)
fig_dd.update_traces(line_color="red")
st.plotly_chart(fig_dd, use_container_width=True)

st.markdown("""
💡 **Drawdown :**  
- 0% = nouveau plus haut historique.  
- −50%, −70%, −80% = baisses très profondes par rapport au sommet précédent.  
Le Bitcoin passe une grande partie du temps **en dessous de ses plus hauts**, avec des baisses 
de **−70 à −80 %** lors des grands bear markets.
""")

# ---------------------------------------------------------

