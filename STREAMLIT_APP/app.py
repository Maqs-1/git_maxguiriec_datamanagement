import streamlit as st

st.set_page_config(
    page_title="Dashboard Bitcoin",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# 🟦 TITRE
# ======================================================
st.title("Dashboard Bitcoin (2012–2025)")

st.markdown("""
Analyse interactive du marché du Bitcoin à partir de données historiques
minute par minute, couvrant la période 2012–2025.
""")

st.markdown("---")

# ======================================================
# 📌 PRÉSENTATION DU PROJET
# ======================================================
st.header("Présentation du projet")

st.markdown("""
Ce projet a été réalisé dans le cadre du **Projet de Data Management** du  
**Diplôme Universitaire Data Analyst – La Sorbonne**.

L’objectif est d’analyser le comportement historique du Bitcoin à travers :
- l’évolution du prix,
- le volume échangé,
- la volatilité,
- les cycles de marché (bull market / bear market),
- les drawdowns et périodes de stress extrême,
- l’analyse textuelle d’articles crypto.

L’application permet une **exploration interactive** du marché du Bitcoin,
à différentes échelles temporelles (horaire, journalière, mensuelle).
""")

st.markdown("---")

# ======================================================
# 📂 SOURCE DES DONNÉES
# ======================================================
st.header("Source du dataset")

st.markdown("""
- **Source :** Kaggle – *Historical Bitcoin Minute-by-Minute Dataset*  
- **Fréquence :** données minute  
- **Période couverte :** 2012 à 2025  
- **Variables principales :** Open, High, Low, Close, Volume  

Le dataset contient **plus de 7 millions d’observations**, ce qui permet
d’analyser finement la micro-structure du marché ainsi que les cycles long terme.
""")

st.markdown("---")

# ======================================================
# 👥 PARTICIPANTS
# ======================================================
st.header("Participants")

st.markdown("""
- **Max Guiriec**  
- **Said Mansour**
""")

st.markdown("---")

# ======================================================
# 🗓️ INFORMATIONS ACADÉMIQUES
# ======================================================
st.header("Cadre académique")

st.markdown("""
- **Formation :** Diplôme Universitaire Data Analyst  
- **Université :** La Sorbonne  
- **Date :** 16 décembre 2025  
""")

st.markdown("---")
