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
st.title("Visualisations avancées du Bitcoin (2012–2025)")

st.markdown("""
Cette page permet d’explorer le Bitcoin à différentes **échelles temporelles** :

- évolution du **prix**,
- **volume échangé** (BTC et USD),
- **cycles d’activité** du marché,
- **distributions** des variables clés.
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
tab1, tab2, tab3 = st.tabs([
    "📉 Prix & Volume",
    "🔥 Cycles & Heatmap",
    "📦 Distributions"
])

# ========================================================
# TAB 1 — PRIX & VOLUME
# ========================================================
with tab1:

    st.subheader(f"Prix du Bitcoin ({period_label})")

    st.plotly_chart(
        px.line(
            df_curve,
            x="Timestamp",
            y="Close",
            labels={"Close": "Prix ($)", "Timestamp": "Date"}
        ),
        use_container_width=True
    )

    st.subheader("Volume échangé (BTC)")
    st.plotly_chart(
        px.line(
            df_curve,
            x="Timestamp",
            y="Volume",
            labels={"Volume": "Volume (BTC)", "Timestamp": "Date"}
        ),
        use_container_width=True
    )

    st.subheader("Volume échangé (USD)")
    st.plotly_chart(
        px.line(
            df_curve,
            x="Timestamp",
            y="Volume_USD",
            labels={"Volume_USD": "Volume ($)", "Timestamp": "Date"}
        ),
        use_container_width=True
    )
st.markdown("""
### Repères historiques majeurs du Bitcoin

L’évolution du prix du Bitcoin s’inscrit dans une succession de **bull markets**, **bear markets** et **phases de transition**, souvent déclenchés par des événements macroéconomiques ou propres à l’écosystème crypto.

- **2013 – Premier bull run majeur**  
  Explosion du prix liée à l’adoption initiale du Bitcoin.  
  Fin brutale avec le **bear market de 2014**, accentué par l’effondrement de **Mt. Gox**.

- **2017 – Bull run historique**  
  Forte spéculation grand public, apparition massive des ICOs.  
  Le pic de décembre 2017 est suivi d’un **bear market prolongé en 2018** (−80 %).

- **2020–2021 – Bull market institutionnel**  
  Contexte macro favorable (COVID, politiques monétaires accommodantes).  
  Entrée des institutions → **bull run jusqu’à ~67 000 $** en 2021.

- **2022 – Bear market structurel**  
  Hausse des taux, chute de l’écosystème crypto, faillites majeures  
  (**LUNA, Celsius, FTX**) → forte contraction du marché.

- **2023–2025 – Phase de reprise et nouveau cycle**  
  Retour progressif de la liquidité, anticipation du **halving**,  
  transition d’un bear market vers un **nouveau bull cycle**.
""")


# ========================================================
# TAB 2 — CYCLES & HEATMAP
# ========================================================
with tab2:

    st.subheader("Cycle d’activité du marché (UTC)")

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

    st.plotly_chart(
        px.imshow(
            heatmap,
            aspect="auto",
            color_continuous_scale="YlOrRd",
            labels=dict(x="Heure (UTC)", y="Jour", color="Volume moyen (BTC)")
        ),
        use_container_width=True
    )

# ========================================================
# TAB 3 — DISTRIBUTIONS
# ========================================================
with tab3:

    st.subheader("Distributions des variables")

    var = st.selectbox(
        "Variable",
        ["Volatility", "Volume_USD"]
    )

    label_map = {
        "Volatility": "Volatilité ($)",
        "Volume_USD": "Volume ($)"
    }

    st.plotly_chart(
        px.box(
            df_curve,
            y=var,
            labels={var: label_map[var]}
        ),
        use_container_width=True
    )
