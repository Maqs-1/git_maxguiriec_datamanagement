import streamlit as st

st.set_page_config(page_title="Synthèse finale", page_icon="📊")

# ---------------------------------------------------------
# TITRE
# ---------------------------------------------------------
st.title("Synthèse finale du projet Bitcoin (2012–2025)")
st.markdown("""
Cette page présente une synthèse globale des analyses réalisées dans l’application :  
structure du dataset, comportement du Bitcoin, cycles de marché, volatilité, volumes,  
événements extrêmes et analyse textuelle.
""")

st.markdown("---")

# ---------------------------------------------------------
# SECTION 1 — STRUCTURE & QUALITÉ DU DATASET
# ---------------------------------------------------------
st.header("1. Structure et qualité du dataset")

st.markdown("""
- Le dataset contient **plus de 7,3 millions d’observations** minute par minute.
- Les variables OHLCV (Open, High, Low, Close, Volume) permettent une analyse financière complète.
- Aucune valeur manquante critique ni doublon n’a été détecté.
- Plusieurs variables dérivées ont été créées afin d’enrichir l’analyse :
  - **Volatility** : amplitude des mouvements de prix,
  - **Volume en BTC et en dollars (USD)**,
  - **Variables temporelles** (année, mois, jour, heure, jour de la semaine),
  permettant l’étude des cycles de marché.
""")

st.markdown("---")

# ---------------------------------------------------------
# SECTION 2 — COMPORTEMENT GÉNÉRAL DU BITCOIN
# ---------------------------------------------------------
st.header("2. Comportement général du Bitcoin")

st.markdown("""
L’analyse met en évidence que le Bitcoin est un actif :

- **hautement volatil**,
- **fortement cyclique**,
- structuré autour d’une alternance claire entre **bull markets** et **bear markets**.

### Observations principales :
- Les **bull markets** se traduisent par des **bullruns rapides et explosifs** (2013, 2017, 2021).
- Ces phases haussières sont suivies de **bear markets profonds**, avec des drawdowns fréquents de **−70 % à −80 %**.
- La volatilité augmente mécaniquement avec le niveau de prix : plus le Bitcoin est cher, plus ses mouvements en valeur absolue sont importants.
- Les volumes explosent aussi bien lors des phases d’euphorie que lors des phases de **capitulation**.
""")

st.markdown("---")

# ---------------------------------------------------------
# SECTION 3 — CYCLES TEMPORELS
# ---------------------------------------------------------
st.header("3. Cycles temporels du Bitcoin")

st.markdown("""
### Cycle journalier
- Pic d’activité entre **16h et 20h UTC**, correspondant à l’ouverture des marchés américains.
- Activité plus faible pendant la nuit (01h–06h UTC).

### Cycle hebdomadaire
- Volumes et volatilité plus faibles le **week-end**.
- Activité plus soutenue en semaine, en particulier en début et milieu de semaine.

### Cycle mensuel et saisonnier
- Certains mois, comme **janvier** ou **novembre**, présentent historiquement davantage de volatilité.
- Les heatmaps (année × mois) révèlent des **régimes de marché persistants**, associés à des phases de bull market ou de bear market prolongées.
""")

st.markdown("---")

# ---------------------------------------------------------
# SECTION 4 — ANALYSE TEXTUELLE
# ---------------------------------------------------------
st.header("4. Analyse textuelle (presse crypto)")

st.markdown("""
L’analyse textuelle d’articles spécialisés montre que le discours médiatique est dominé par :

- les notions de **volatilité**, **incertitude**, **cycle**, **marché**,
- une prudence marquée à court terme,
- mais une vision généralement **haussière à moyen et long terme**.

Les WordClouds permettent d’identifier rapidement les thèmes centraux et la tonalité globale des articles.
""")

st.markdown("---")

# ---------------------------------------------------------
# SECTION 5 — LIMITES DE L’ANALYSE
# ---------------------------------------------------------
st.header("5. Limites du projet")

st.markdown("""
Malgré la robustesse de l’analyse, certaines limites doivent être soulignées :

- Les données minute sont très bruitées et nécessitent une agrégation.
- Le volume ne permet pas de distinguer acheteurs et vendeurs.
- L’absence de données exogènes :
  - macroéconomie,
  - marchés traditionnels,
  - indicateurs on-chain.

Ces limites ouvrent la voie à des extensions futures plus avancées.
""")

st.markdown("---")

# ---------------------------------------------------------
# CONCLUSION
# ---------------------------------------------------------
st.header("Conclusion générale")

st.markdown("""
Ce projet met en évidence que le Bitcoin est un actif :

- dominé par des **bull markets violents** et des **bear markets profonds**,
- caractérisé par une **volatilité structurellement élevée**,
- rythmé par des phases d’euphorie, de correction et de capitulation.

L’application Streamlit permet une exploration claire et interactive :
- des cycles de marché,
- des volumes et de la volatilité,
- des périodes extrêmes,
- et du discours médiatique autour du Bitcoin.

Elle offre ainsi une **compréhension globale et structurée du marché Bitcoin**, sans chercher à produire de prédiction.
""")
