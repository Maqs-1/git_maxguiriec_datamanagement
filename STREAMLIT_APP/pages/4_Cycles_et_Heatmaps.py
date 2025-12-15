import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cycles & Heatmaps", page_icon="🔥", layout="wide")

# =========================================================
# 🔧 Chargement des données
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/DATASET_BTC.csv")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")
    df = df.sort_values("Timestamp").set_index("Timestamp")

    # Volatilité ($)
    df["Volatility"] = df["High"] - df["Low"]

    # Volume en dollars
    df["Volume_USD"] = df["Volume"] * df["Close"]

    # Variables temporelles
    df["Year"] = df.index.year
    df["Month"] = df.index.month
    df["Hour"] = df.index.hour
    df["Weekday"] = df.index.weekday

    return df

df = load_data()

# =========================================================
# 🎛️ FILTRES
# =========================================================
st.title("Cycles & Heatmaps du Bitcoin")

years = sorted(df["Year"].unique())
selected_years = st.sidebar.multiselect("📅 Années à analyser", years, default=years)

use_usd = st.sidebar.checkbox("💵 Exprimer le volume en dollars (USD)", value=False)

volume_col = "Volume_USD" if use_usd else "Volume"
volume_label = "Volume moyen ($)" if use_usd else "Volume moyen (BTC)"

df_filt = df[df["Year"].isin(selected_years)]

# =========================================================
# 🧩 ONGLET
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🕒 Cycle journalier",
    "📆 Cycle hebdomadaire",
    "📅 Cycle mensuel",
    "🌡️ Heatmaps saisonnières"
])

# =========================================================
# 🟦 TAB 1 — CYCLE JOURNALIER (VRAI volume horaire)
# =========================================================
with tab1:
    st.subheader("Cycle journalier – volume & volatilité par heure")

    hourly = df_filt.resample("H").agg({
        volume_col: "sum",
        "High": "max",
        "Low": "min"
    }).dropna()

    hourly["Volatility"] = hourly["High"] - hourly["Low"]
    hourly["Hour"] = hourly.index.hour

    hourly_avg = hourly.groupby("Hour").mean().reset_index()

    st.plotly_chart(
        px.line(
            hourly_avg,
            x="Hour",
            y=volume_col,
            labels={volume_col: volume_label, "Hour": "Heure (UTC)"},
            title="Volume moyen par heure"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(
            hourly_avg,
            x="Hour",
            y="Volatility",
            labels={"Volatility": "Volatilité moyenne ($)", "Hour": "Heure (UTC)"},
            title="Volatilité moyenne par heure"
        ),
        use_container_width=True
    )


# =========================================================
# 🟧 TAB 2 — CYCLE HEBDOMADAIRE (VRAI volume journalier)
# =========================================================
with tab2:
    st.subheader("Cycle hebdomadaire – volume & volatilité par jour")

    daily = df_filt.resample("D").agg({
        volume_col: "sum",
        "High": "max",
        "Low": "min"
    }).dropna()

    daily["Volatility"] = daily["High"] - daily["Low"]
    daily["Weekday"] = daily.index.weekday

    weekly_avg = daily.groupby("Weekday").mean().reset_index()

    weekday_map = {
        0: "Lundi", 1: "Mardi", 2: "Mercredi",
        3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"
    }
    weekly_avg["Jour"] = weekly_avg["Weekday"].map(weekday_map)

    st.plotly_chart(
        px.bar(
            weekly_avg,
            x="Jour",
            y=volume_col,
            labels={volume_col: volume_label},
            title="Volume moyen par jour"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.bar(
            weekly_avg,
            x="Jour",
            y="Volatility",
            labels={"Volatility": "Volatilité moyenne ($)"},
            title="Volatilité moyenne par jour"
        ),
        use_container_width=True
    )

# =========================================================
# 🟩 TAB 3 — CYCLE MENSUEL (VRAI volume mensuel)
# =========================================================
with tab3:
    st.subheader("Cycle mensuel – volume & volatilité par mois")

    monthly = df_filt.resample("M").agg({
        volume_col: "sum",
        "High": "max",
        "Low": "min"
    }).dropna()

    monthly["Volatility"] = monthly["High"] - monthly["Low"]
    monthly["Month"] = monthly.index.month

    monthly_avg = monthly.groupby("Month").mean().reset_index()

    st.plotly_chart(
        px.line(
            monthly_avg,
            x="Month",
            y=volume_col,
            labels={volume_col: volume_label, "Month": "Mois"},
            title="Volume moyen par mois"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.line(
            monthly_avg,
            x="Month",
            y="Volatility",
            labels={"Volatility": "Volatilité moyenne ($)", "Month": "Mois"},
            title="Volatilité moyenne par mois"
        ),
        use_container_width=True
    )

# =========================================================
# 🟥 TAB 4 — HEATMAPS SAISONNIÈRES
# =========================================================
with tab4:
    st.subheader("Heatmaps saisonnières (Année × Mois)")

    heat = df_filt.resample("M").agg({
        volume_col: "sum",
        "High": "max",
        "Low": "min"
    }).dropna()

    heat["Volatility"] = heat["High"] - heat["Low"]
    heat["Year"] = heat.index.year
    heat["Month"] = heat.index.month

    metric = st.selectbox("Choisir une métrique", ["Volume", "Volatilité"])

    if metric == "Volume":
        pivot = heat.pivot(index="Year", columns="Month", values=volume_col)
        label = volume_label
    else:
        pivot = heat.pivot(index="Year", columns="Month", values="Volatility")
        label = "Volatilité moyenne ($)"

    st.plotly_chart(
        px.imshow(
            pivot,
            aspect="auto",
            color_continuous_scale="YlOrRd",
            labels={"color": label}
        ),
        use_container_width=True
    )


