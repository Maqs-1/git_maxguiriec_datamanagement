import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Statistiques Descriptives", page_icon="📊")

# --------------------------------------------------------
# 🔧 Chargement des données
# --------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/DATASET_BTC.csv")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")
    df = df.sort_values("Timestamp")

    # Variables minute
    df["Volatility"] = df["High"] - df["Low"]
    df["RollingVol"] = df["Close"].rolling(window=60).std()
    df["Year"] = df["Timestamp"].dt.year

    # ---------------- DAILY ----------------
    df_daily = df.resample("D", on="Timestamp").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

    df_daily["Return_daily_pct"] = df_daily["Close"].pct_change() * 100
    df_daily["Year"] = df_daily.index.year

    # ---------------- WEEKLY ----------------
    df_weekly = df.resample("W", on="Timestamp").agg({
        "Close": "last"
    }).dropna()

    df_weekly["Return_weekly_pct"] = df_weekly["Close"].pct_change() * 100
    df_weekly["Year"] = df_weekly.index.year

    # ---------------- MONTHLY ----------------
    df_monthly = df.resample("M", on="Timestamp").agg({
        "Close": "last"
    }).dropna()

    df_monthly["Return_monthly_pct"] = df_monthly["Close"].pct_change() * 100
    df_monthly["Year"] = df_monthly.index.year

    return df, df_daily, df_weekly, df_monthly


df, df_daily, df_weekly, df_monthly = load_data()

# --------------------------------------------------------
# 🟦 TITRE
# --------------------------------------------------------
st.title("📊 Statistiques Descriptives du Bitcoin")

st.markdown("""
Cette page présente les statistiques descriptives des principales variables du Bitcoin.  

📌 Les **returns sont exprimés en pourcentage (%)** et calculés à différentes
échelles temporelles (journalière, hebdomadaire, mensuelle) afin de garantir
des graphiques lisibles et interprétables.
""")

# --------------------------------------------------------
# 1️⃣ Choix du type de graphique
# --------------------------------------------------------
graph_type = st.sidebar.selectbox(
    "📌 Type de graphique",
    ["Histogramme", "Densité (KDE)", "Boxplot"]
)

# --------------------------------------------------------
# 2️⃣ Choix de la variable
# --------------------------------------------------------
variable = st.sidebar.selectbox(
    "🎯 Variable analysée",
    [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Volatility",
        "RollingVol",
        "Return_daily_pct",
        "Return_weekly_pct",
        "Return_monthly_pct"
    ]
)

# --------------------------------------------------------
# 3️⃣ Sélection du bon dataframe
# --------------------------------------------------------
if variable == "Return_daily_pct":
    data_df = df_daily
elif variable == "Return_weekly_pct":
    data_df = df_weekly
elif variable == "Return_monthly_pct":
    data_df = df_monthly
else:
    data_df = df

# --------------------------------------------------------
# 4️⃣ Filtre années
# --------------------------------------------------------
years = sorted(data_df["Year"].unique())
selected_years = st.sidebar.multiselect(
    "📅 Années à afficher :", years, default=years
)

filtered_series = (
    data_df[data_df["Year"].isin(selected_years)][variable]
    .dropna()
)

# --------------------------------------------------------
# 🧠 Préparation intelligente des données
# --------------------------------------------------------
def prepare_for_plot(series, variable_name):
    series = series.dropna()
    log_used = False

    # Winsorisation
    if variable_name in ["Volume", "Volatility", "RollingVol"]:
        p99 = series.quantile(0.99)
        series = series[series <= p99]

    # Log automatique pour le volume
    if variable_name == "Volume" and series.max() > 100:
        series = np.log1p(series)
        log_used = True

    return series, log_used

data, log_used = prepare_for_plot(filtered_series, variable)

# --------------------------------------------------------
# 📋 Statistiques descriptives
# --------------------------------------------------------
st.subheader(f"📋 Statistiques descriptives — {variable}")

stats = filtered_series.describe().round(4)
stats["skewness"] = filtered_series.skew().round(4)
stats["kurtosis"] = filtered_series.kurt().round(4)

st.dataframe(stats.to_frame(name="Valeur"))

# --------------------------------------------------------
# 📊 Graphiques
# --------------------------------------------------------

# -------- HISTOGRAMME --------
if graph_type == "Histogramme":
    st.subheader(f"📊 Histogramme — {variable}")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(data, bins=40, color="skyblue", edgecolor="black")

    # Ligne zéro pour les returns
    if "Return" in variable:
        ax.axvline(0, color="red", linestyle="--", linewidth=2)
        ax.set_xlabel("Return (%)")
        ax.set_ylabel("Nombre de périodes")
    else:
        ax.set_xlabel(variable)
        ax.set_ylabel("Fréquence")

    ax.set_title(f"Distribution de {variable}")
    st.pyplot(fig)

# -------- KDE --------
elif graph_type == "Densité (KDE)":
    st.subheader(f"🌡️ Densité — {variable}")

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.kdeplot(data, fill=True, color="purple", ax=ax)

    if "Return" in variable:
        ax.axvline(0, color="red", linestyle="--", linewidth=2)
        ax.set_xlabel("Return (%)")
    else:
        ax.set_xlabel(variable)

    ax.set_title(f"Densité de {variable}")
    st.pyplot(fig)

# -------- BOXPLOT --------
else:
    st.subheader(f"📦 Boxplot — {variable}")

    fig, ax = plt.subplots(figsize=(10, 3))
    sns.boxplot(x=data, color="orange", ax=ax)

    if "Return" in variable:
        ax.axvline(0, color="red", linestyle="--", linewidth=2)
        ax.set_xlabel("Return (%)")
    else:
        ax.set_xlabel(variable)

    ax.set_title(f"Boxplot de {variable}")
    st.pyplot(fig)

# --------------------------------------------------------
st.markdown("---")
st.success("✅ Graphiques générés avec unités cohérentes et interprétables.")
