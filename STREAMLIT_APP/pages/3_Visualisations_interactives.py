import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Visualisations avancées",
    page_icon="📈",
    layout="wide"
)

# ========================================================
# 🔧 Chargement & préparation des données
# ========================================================
@st.cache_data
def load_data():

    df = pd.read_csv("data/DATASET_BTC.csv")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")
    df = df.sort_values("Timestamp")

    # ================= DAILY =================
    df_daily = df.resample("D", on="Timestamp").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

    df_daily["Return"] = df_daily["Close"].pct_change() * 100
    df_daily["Volatility"] = df_daily["High"] - df_daily["Low"]
    df_daily["Volume_USD"] = df_daily["Volume"] * df_daily["Close"]

    df_daily["Year"] = df_daily.index.year
    df_daily["Month"] = df_daily.index.month
    df_daily["Timestamp"] = df_daily.index

    # ================= WEEKLY =================
    df_weekly = df.resample("W", on="Timestamp").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

    df_weekly["Return"] = df_weekly["Close"].pct_change() * 100
    df_weekly["Volatility"] = df_weekly["High"] - df_weekly["Low"]
    df_weekly["Volume_USD"] = df_weekly["Volume"] * df_weekly["Close"]

    df_weekly["Year"] = df_weekly.index.year
    df_weekly["Month"] = df_weekly.index.month
    df_weekly["Timestamp"] = df_weekly.index

    # ================= MONTHLY =================
    df_monthly = df.resample("M", on="Timestamp").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

    df_monthly["Return"] = df_monthly["Close"].pct_change() * 100
    df_monthly["Volatility"] = df_monthly["High"] - df_monthly["Low"]
    df_monthly["Volume_USD"] = df_monthly["Volume"] * df_monthly["Close"]

    df_monthly["Year"] = df_monthly.index.year
    df_monthly["Month"] = df_monthly.index.month
    df_monthly["Timestamp"] = df_monthly.index

    return df_daily, df_weekly, df_monthly


df_daily, df_weekly, df_monthly = load_data()

# ========================================================
# 🟦 TITRE
# ========================================================
st.title("📈 Visualisations avancées du Bitcoin (2012–2025)")

st.markdown("""
Cette page permet d’explorer le Bitcoin à différentes **échelles temporelles** :
- évolution du **prix**,
- **volume en BTC** et **volume en dollars**,
- **cycles d’activité**,
- **relations rendement / risque**,
- **distributions par période**.
""")

# ========================================================
# 🎛️ FILTRES GLOBAUX
# ========================================================
st.sidebar.header("⚙️ Filtres")

time_scale = st.sidebar.radio(
    "🕒 Échelle temporelle",
    ["Jour", "Semaine", "Mois"],
    index=0
)

if time_scale == "Jour":
    df_curve = df_daily.copy()
    period_label = "journalier"
elif time_scale == "Semaine":
    df_curve = df_weekly.copy()
    period_label = "hebdomadaire"
else:
    df_curve = df_monthly.copy()
    period_label = "mensuel"

years = sorted(df_curve["Year"].unique())
selected_years = st.sidebar.multiselect(
    "📅 Années",
    years,
    default=years
)

df_curve = df_curve[df_curve["Year"].isin(selected_years)]

# ========================================================
# 🧩 ONGLET
# ========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📉 Prix & Volume",
    "🔥 Cycles & Heatmap",
    "🔗 Relations",
    "📦 Distributions"
])

# ========================================================
# TAB 1 — PRIX & VOLUME
# ========================================================
with tab1:

    st.subheader(f"📉 Prix du Bitcoin ({period_label})")

    fig_price = px.line(
        df_curve,
        x="Timestamp",
        y="Close",
        labels={"Close": "Prix ($)", "Timestamp": "Date"}
    )
    st.plotly_chart(fig_price, use_container_width=True)

    st.subheader("📊 Volume échangé (BTC)")

    fig_vol_btc = px.line(
        df_curve,
        x="Timestamp",
        y="Volume",
        labels={"Volume": "Volume (BTC)", "Timestamp": "Date"}
    )
    st.plotly_chart(fig_vol_btc, use_container_width=True)

    st.subheader("💵 Volume échangé (USD)")

    fig_vol_usd = px.line(
        df_curve,
        x="Timestamp",
        y="Volume_USD",
        labels={"Volume_USD": "Volume ($)", "Timestamp": "Date"}
    )
    st.plotly_chart(fig_vol_usd, use_container_width=True)

# ========================================================
# TAB 2 — CYCLES & HEATMAP (HOURLY FIXE)
# ========================================================
with tab2:

    st.subheader("🔥 Cycle d’activité du marché (UTC)")

    df_hourly = pd.read_csv("data/DATASET_BTC.csv")
    df_hourly["Timestamp"] = pd.to_datetime(df_hourly["Timestamp"], unit="s")

    df_hourly["Hour"] = df_hourly["Timestamp"].dt.hour
    df_hourly["Weekday"] = df_hourly["Timestamp"].dt.weekday
    df_hourly["Year"] = df_hourly["Timestamp"].dt.year

    df_hourly = df_hourly[df_hourly["Year"].isin(selected_years)]

    heatmap = df_hourly.pivot_table(
        values="Volume",
        index="Weekday",
        columns="Hour",
        aggfunc="mean"
    )

    heatmap.index = ["Lundi", "Mardi", "Mercredi",
                     "Jeudi", "Vendredi", "Samedi", "Dimanche"]

    fig_hm = px.imshow(
        heatmap,
        aspect="auto",
        color_continuous_scale="YlOrRd",
        labels=dict(x="Heure (UTC)", y="Jour", color="Volume moyen (BTC)")
    )

    st.plotly_chart(fig_hm, use_container_width=True)

# ========================================================
# TAB 3 — RELATIONS
# ========================================================
with tab3:

    st.subheader("🔗 Relations rendement / risque")

    relation = st.selectbox(
        "Analyse",
        [
            "Prix vs Volatilité",
            "Volume USD vs Volatilité",
            "Return vs Volatilité"
        ]
    )

    if relation == "Prix vs Volatilité":
        x, y = "Close", "Volatility"
        x_label, y_label = "Prix ($)", "Volatilité ($)"

    elif relation == "Volume USD vs Volatilité":
        x, y = "Volume_USD", "Volatility"
        x_label, y_label = "Volume ($)", "Volatilité ($)"

    else:
        x, y = "Return", "Volatility"
        x_label, y_label = "Return (%)", "Volatilité ($)"

    fig_scatter = px.scatter(
        df_curve,
        x=x,
        y=y,
        opacity=0.5,
        labels={x: x_label, y: y_label}
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

# ========================================================
# TAB 4 — DISTRIBUTIONS
# ========================================================
with tab4:

    st.subheader("📦 Distributions")

    var = st.selectbox(
        "Variable",
        ["Return", "Volatility", "Volume_USD"]
    )

    label_map = {
        "Return": "Return (%)",
        "Volatility": "Volatilité ($)",
        "Volume_USD": "Volume ($)"
    }

    fig_box = px.box(
        df_curve,
        y=var,
        labels={var: label_map[var]}
    )

    st.plotly_chart(fig_box, use_container_width=True)

st.success("✅ Échelles temporelles cohérentes — données prêtes pour l’oral.")
