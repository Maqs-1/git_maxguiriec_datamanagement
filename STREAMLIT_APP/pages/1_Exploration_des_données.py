import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Exploration du dataset", page_icon="📂")

# -----------------------------------------------
# 🟦 TITRE DE LA PAGE
# -----------------------------------------------
st.title("📂 Exploration du jeu de données Bitcoin (2012–2025)")

st.markdown("""
Cette page permet d'explorer en détail la structure du dataset Bitcoin utilisé dans l'application.

Vous trouverez :
- la source des données  
- le nombre d’observations et de variables  
- les types et significations des colonnes  
- les valeurs manquantes  
- les doublons éventuels  
- un aperçu des données  
- des statistiques descriptives générales  
""")

# -----------------------------------------------
# 🟩 Chargement du dataset
# -----------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/DATASET_BTC.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
    return df

df = load_data()


# -----------------------------------------------
# 🟦 SECTION 1 : Source & Description du Dataset
# -----------------------------------------------
st.header("1. Source et description du dataset")

st.markdown("""
- **Source :** Kaggle — Historical Bitcoin Minute-by-minute Dataset  
- **Période couverte :** 2012 à 2025  
- **Fréquence :** données *minute*  
- **Variables OHLCV :**
  - `Open` : prix d’ouverture  
  - `High` : prix le plus haut  
  - `Low` : prix le plus bas  
  - `Close` : prix de clôture  
  - `Volume` : volume échangé  
  - `Timestamp` : horodatage UNIX  
""")


# -----------------------------------------------
# 🟦 SECTION 2 : Dimensions du dataset
# -----------------------------------------------
st.header("2. Dimensions du dataset")

rows, cols = df.shape
st.metric("Nombre d'observations", f"{rows:,}".replace(",", " "))
st.metric("Nombre de variables", cols)


# -----------------------------------------------
# 🟦 SECTION 3 : Aperçu des données
# -----------------------------------------------
st.header("3. Aperçu des données")

n = st.slider("Nombre de lignes à afficher :", 5, 50, 10)
st.dataframe(df.head(n))


# -----------------------------------------------
# 🟦 SECTION 4 : Types des variables
# -----------------------------------------------
st.header("4. Types des variables")

st.dataframe(df.dtypes.rename("Type"))


# -----------------------------------------------
# 🟦 SECTION 5 : Valeurs manquantes
# -----------------------------------------------
st.header("5. Valeurs manquantes")

missing = df.isna().sum()
missing_df = pd.DataFrame({
    "Colonnes": missing.index,
    "Valeurs manquantes": missing.values
})
st.dataframe(missing_df)


# -----------------------------------------------
# 🟦 SECTION 6 : Doublons
# -----------------------------------------------
st.header("6. Doublons dans le dataset")

duplicates = df.duplicated().sum()
st.write(f"🔁 Nombre de lignes dupliquées : **{duplicates}**")


# -----------------------------------------------
# 🟦 SECTION 7 : Statistiques descriptives globales
# -----------------------------------------------
st.header("7. Statistiques descriptives")

st.write("Statistiques pour les variables numériques (OHLCV) :")
st.dataframe(df.describe().T)



# ============================================================
# 🟦 SECTION 8 : Variables dérivées créées dans le projet
# ============================================================

st.header("8. Variables dérivées créées pour l'analyse")

st.markdown("""
Au cours du projet, plusieurs variables ont été créées afin d'enrichir l'analyse et de mieux 
comprendre le comportement du Bitcoin. Ces variables ne figurent pas dans le dataset original.
""")

# Création des variables dérivées (si pas encore créées ici)
df['Return'] = df['Close'].pct_change()
df['Volatility'] = df['High'] - df['Low']
df['RollingVol'] = df['Close'].rolling(window=60).std()

df['Year'] = df['Timestamp'].dt.year
df['Month'] = df['Timestamp'].dt.month
df['Day'] = df['Timestamp'].dt.day
df['Hour'] = df['Timestamp'].dt.hour
df['Weekday'] = df['Timestamp'].dt.weekday

# Tableau explicatif
variables_deriv = {
    "Return": "Variation relative du prix entre deux périodes",
    "Volatility": "Amplitude d'une période (High – Low)",
    "Year": "Année extraite du Timestamp",
    "Month": "Mois extrait du Timestamp",
    "Day": "Jour du mois",
    "Hour": "Heure (pour cycles intrajournaliers)",
    "Weekday": "Jour de la semaine (0=Lundi, 6=Dimanche)",
}

df_vars = pd.DataFrame.from_dict(variables_deriv, orient='index', columns=["Description"])
st.dataframe(df_vars)

# ============================================================
# 🟦 SECTION 9 : Téléchargement du dataset
# ============================================================

st.header("9. Téléchargement du dataset")

st.markdown("""
Vous pouvez télécharger le jeu de données utilisé dans ce projet afin de :
- reproduire les analyses,
- explorer les données hors de l’application,
- effectuer vos propres traitements.
""")

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

csv_data = convert_df_to_csv(df)

st.download_button(
    label="📥 Télécharger le dataset Bitcoin (CSV)",
    data=csv_data,
    file_name="DATASET_BTC.csv",
    mime="text/csv"
)
