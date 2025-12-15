#  Bitcoin Market Analysis (2012–2025)

Projet réalisé dans le cadre du **Diplôme Universitaire Data Analyst – La Sorbonne**.  
Ce projet propose une **analyse complète et interactive du marché du Bitcoin** à partir de données minute par minute, couvrant la période **2012–2025**.

---

## 👥 Membres du projet

- **Max Guiriec**
- **Said Mansour**

📅 Date : **16 décembre 2025**

---

##  Source des données

- **Dataset** : *Historical Bitcoin Minute-by-minute Dataset*  
- **Plateforme** : Kaggle  
- **Fréquence** : données minute (OHLCV)  
- **Période couverte** : 2012 → 2025  

> ⚠️ Le fichier CSV n’est pas inclus dans le dépôt GitHub en raison de sa taille (>100MB).

---

##  Objectifs du projet

- Comprendre le **comportement historique du Bitcoin**
- Identifier les **phases de bull market et bear market**
- Étudier :
  - l’évolution du prix
  - les volumes échangés (BTC et USD)
  - la volatilité
  - les drawdowns
  - les cycles temporels (heure, jour, mois)
- Mettre en évidence les **événements extrêmes**
- Explorer le **discours médiatique** autour du Bitcoin (text mining)

---

##  Contenu de l’application Streamlit

L’application est organisée en plusieurs pages :

- **Exploration des données**  
- **Statistiques descriptives**
- **Visualisations interactives**
- **Cycles & heatmaps**
- **Performance annuelle & drawdown**
- **Analyse textuelle (WordCloud, TF-IDF)**
- **Synthèse finale**

---

## 🛠️ Technologies utilisées

- Python 3
- Streamlit
- Pandas / NumPy
- Plotly / Matplotlib / Seaborn
- Scikit-learn
- WordCloud

---

## 📦 Installation et exécution

1. Cloner le dépôt :
```bash
git clone https://github.com/Maqs-1/git_maxguiriec_datamanagement.git
cd git_maxguiriec_datamanagement

---

## Installer les dépendances 

2. pip install -r requirements.txt

## Lancer l'appli 

3. streamlit run STREAMLIT_APP/app.py

## 🗂️ Structure du projet

PROJET_BITCOIN/
│
├── DATA/ # Données brutes (non versionnées)
├── NOTEBOOK/ # Notebooks d’exploration et d’analyse
├── STREAMLIT_APP/
│ ├── app.py # Application principale
│ ├── pages/ # Pages Streamlit (analyses)
│ ├── assets/ # Images / ressources
│ └── data/ # Dataset local (ignoré par Git)
│
├── requirements.txt # Dépendances Python
├── MEMBERS.txt # Membres du projet
├── README.md # Documentation
└── LICENSE


