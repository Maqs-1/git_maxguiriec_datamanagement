import streamlit as st
import pandas as pd
import re
import nltk
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Text Mining Bitcoin", page_icon="🧠")

# ---------------------------------------------------------
# 🔧 Chargement des ressources NLTK
# ---------------------------------------------------------
@st.cache_resource
def load_stopwords():
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    from nltk.corpus import stopwords
    return set(stopwords.words('french'))

STOPWORDS_FR = load_stopwords()

# ---------------------------------------------------------
# 🟦 TITRE
# ---------------------------------------------------------
st.title("Analyse Textuelle (Text Mining) autour du Bitcoin")

st.markdown("""
Cette page permet d'analyser un **article en français** parlant du Bitcoin :
- nettoyage du texte,
- extraction des mots les plus fréquents,
- génération d'un **WordCloud**,
- interprétation rapide du vocabulaire dominant.
""")

# ---------------------------------------------------------
# 📝 Zone de texte pour l'article
# ---------------------------------------------------------
st.subheader("Texte à analyser")

default_text = """
Bitcoin : Pour Tom Lee, le BTC retournera à 100 000 $ en 2025, mais plus question des 250 000 $.

Tom Lee, le président de BitMine, a légèrement revu à la baisse sa prédiction audacieuse de voir Bitcoin atteindre
250 000 $ d’ici la fin de l’année. Bien qu’il ait précédemment maintenu cette prévision, Lee parle maintenant
d’un « peut-être » concernant un nouveau sommet pour Bitcoin avant 2026.

Dans une interview récente, il a déclaré qu’il est « très probable » que Bitcoin dépasse les 100 000 $ avant la fin
de l’année, tout en restant plus prudent sur tout nouveau record. Cette déclaration marque une révision de son
optimisme initial.

Lee souligne que la cryptomonnaie réalise souvent ses plus forts gains sur une poignée de jours chaque année.
Il évoque des périodes de volatilité élevée, des ajustements de marché et une incertitude accrue, mais reste
convaincu du potentiel de long terme de Bitcoin.

Malgré une tendance baissière récente et un marché chahuté, Lee estime que Bitcoin a encore des « bons jours »
devant lui. Il note que même après des mouvements imprévus, la cryptomonnaie a montré qu’elle pouvait se relever,
ce qui le rend confiant quant à un rebond possible avant la fin de 2025.

Selon lui, les conditions actuelles pourraient offrir une opportunité d’achat, avec un retour du marché vers un
cycle haussier si les bons signaux s’alignent. Toutefois, il avertit que le marché reste exposé aux risques de
volatilité, à la macroéconomie et aux incertitudes.

Cette position, moins extrême qu’en début d’année, reflète une approche plus nuancée du marché, tout en conservant
une vision haussière sur le moyen terme.
"""

user_text = st.text_area(
    "Collez ici un article ou un texte en français sur le Bitcoin :",
    value=default_text,
    height=300
)

if not user_text.strip():
    st.warning("⚠️ Merci de coller un texte pour lancer l'analyse.")
    st.stop()

# ---------------------------------------------------------
# 🧼 Nettoyage du texte
# ---------------------------------------------------------
st.subheader("🧼 Nettoyage du texte")

def clean_text(text: str):
    # minuscule
    text = text.lower()
    # retirer chiffres, ponctuation, symboles
    text = re.sub(r"[^a-zàâäéèêëîïôöùûüçñ\s]", " ", text)
    # découpage
    words = text.split()
    # suppression stopwords + mots trop courts
    words = [w for w in words if w not in STOPWORDS_FR and len(w) > 2]
    return words

words = clean_text(user_text)
cleaned_text = " ".join(words)

st.write(f"Nombre de mots après nettoyage : **{len(words)}**")

# ---------------------------------------------------------
# Mots les plus fréquents
# ---------------------------------------------------------
st.subheader("🔝 Mots les plus fréquents")

n_top = st.slider("Nombre de mots à afficher :", 5, 30, 10)
counter = Counter(words)
most_common = counter.most_common(n_top)

freq_df = pd.DataFrame(most_common, columns=["Mot", "Fréquence"])
st.dataframe(freq_df)

# ---------------------------------------------------------
# ☁️ WordCloud
# ---------------------------------------------------------
st.subheader("☁️ WordCloud du vocabulaire dominant")

wc = WordCloud(
    width=800,
    height=400,
    background_color="white",
    colormap="Oranges"
).generate(cleaned_text)

fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# ---------------------------------------------------------
# Interprétation simple
# ---------------------------------------------------------
st.subheader("Interprétation automatique (rapide)")

main_words = [w for w, _ in most_common[:7]]
st.markdown(f"""
Les mots les plus présents dans ce texte sont : **{", ".join(main_words)}**.

Cela suggère que le texte insiste sur :
- le rôle du **Bitcoin** comme actif central,
- la notion de **marché**, de **volatilité** et d'**incertitude**,
- une vision plutôt **haussière à moyen terme** malgré des phases de baisse.

Ce type d'analyse textuelle permet de :
- résumer rapidement le **ton général** d'un article,
- repérer les thèmes dominants (risque, opportunité, prévisions),
- comparer plusieurs articles entre eux sur la même période.
""")


