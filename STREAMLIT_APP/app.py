import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bitcoin Dashboard", page_icon="📊", layout="wide")

# ---------------------------------------------
# TITRE
# ---------------------------------------------
st.title("📈 Dashboard Bitcoin (2012–2025)")
st.markdown("""
Analyse interactive du marché du Bitcoin : prix, volatilité, volume,
records extrêmes et cycles de marché.
""")

# ---------------------------------------------
# LOAD DATA
# ---------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/DATASET_BTC.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
    df = df.sort_values("Timestamp")
    df['Year'] = df['Timestamp'].dt.year
    df['Month'] = df['Timestamp'].dt.month
    df['Day'] = df['Timestamp'].dt.day
    df['Hour'] = df['Timestamp'].dt.hour
    df['Weekday'] = df['Timestamp'].dt.weekday
    df['Return'] = df['Close'].pct_change()
    df['Volatility'] = df['High'] - df['Low']
    return df

df = load_data()

# Résampling daily
df_daily = df.resample('D', on='Timestamp').agg({
    'Open':'first', 'High':'max', 'Low':'min', 'Close':'last',
    'Volume':'sum', 'Return':'mean', 'Volatility':'mean'
})

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Choisir une page :", [
    "🏠 Accueil",
    "📊 Évolution du prix",
    "📉 Volatilité & Volume",
    "⚡ Records extrêmes",
    "🌡️ Heatmap Activité",
    "📉 Drawdown",
])

# ---------------------------------------------
#  PAGE 1 : ACCUEIL
# ---------------------------------------------
if page == "🏠 Accueil":
    st.subheader("Bienvenue dans le Dashboard Bitcoin 🔥")
    st.write("""
Ce dashboard permet de visualiser les tendances majeures du Bitcoin entre 2012 et 2025 :
- évolution du prix  
- analyse du volume  
- volatilité journalière  
- records historiques  
- cycles hebdomadaires et horaires  
- drawdown et risques extrêmes  
    """)
    st.write("Sélectionnez une section dans la barre latérale.")

# ---------------------------------------------
# PAGE 2 : EVOLUTION DU PRIX
# ---------------------------------------------
elif page == "📊 Évolution du prix":
    st.subheader("🎯 Évolution du prix du Bitcoin")

    fig, ax = plt.subplots(figsize=(14,5))
    ax.plot(df_daily.index, df_daily['Close'], color='blue')
    ax.set_title("Évolution du prix du Bitcoin (daily)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Prix ($)")
    ax.grid(True)

    st.pyplot(fig)

# ---------------------------------------------
# PAGE 3 : VOLATILITE & VOLUME
# ---------------------------------------------
elif page == "📉 Volatilité & Volume":
    st.subheader("📉 Volatilité journalière (High - Low)")
    fig1, ax1 = plt.subplots(figsize=(14,5))
    ax1.plot(df_daily['Volatility'], color='orange')
    ax1.set_title("Volatilité daily")
    st.pyplot(fig1)

    st.subheader("📊 Volume journalier")
    fig2, ax2 = plt.subplots(figsize=(14,5))
    ax2.plot(df_daily['Volume'], color='purple')
    ax2.set_title("Volume daily")
    st.pyplot(fig2)

# ---------------------------------------------
# PAGE 4 : RECORDS EXTREMES
# ---------------------------------------------
elif page == "⚡ Records extrêmes":

    st.subheader("🚀 Top 10 hausses (%)")
    top_gains = df_daily['Return'].nlargest(10).round(4)*100
    st.dataframe(top_gains)

    st.subheader("💥 Top 10 chutes (%)")
    top_losses = df_daily['Return'].nsmallest(10).round(4)*100
    st.dataframe(top_losses)

    st.subheader("⚡ Top volatilité (High - Low)")
    top_vol = df_daily['Volatility'].nlargest(10).round(2)
    st.dataframe(top_vol)

    st.subheader("📊 Top volume")
    top_volume = df_daily['Volume'].nlargest(10).round(2)
    st.dataframe(top_volume)

# ---------------------------------------------
# PAGE 5 : HEATMAP ACTIVITE
# ---------------------------------------------
elif page == "🌡️ Heatmap Activité":
    st.subheader("🔥 Heatmap des volumes par heure et jour")

    heatmap_data = df.groupby(['Weekday','Hour'])['Volume'].mean().unstack()

    fig, ax = plt.subplots(figsize=(12,6))
    sns.heatmap(heatmap_data, cmap="YlOrRd", ax=ax)
    st.pyplot(fig)

# ---------------------------------------------
# PAGE 6 : DRAWDOWN
# ---------------------------------------------
elif page == "📉 Drawdown":
    st.subheader("📉 Drawdown du Bitcoin (%)")

    df_daily['Peak'] = df_daily['Close'].cummax()
    df_daily['Drawdown'] = (df_daily['Close'] - df_daily['Peak']) / df_daily['Peak'] * 100

    fig, ax = plt.subplots(figsize=(14,5))
    ax.plot(df_daily.index, df_daily['Drawdown'], color='red')
    ax.axhline(0, color='black')
    ax.grid(True)
    st.pyplot(fig)
