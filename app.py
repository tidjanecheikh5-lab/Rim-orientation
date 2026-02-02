import streamlit as st
import pandas as pd
import random

# =========================
# CONFIGURATION PAGE
# =========================
st.set_page_config(
    page_title="Orientation scolaire",
    page_icon="🎓",
    layout="centered"
)

# =========================
# CSS (LISIBLE + PRO)
# =========================
st.markdown("""
<style>
body {
    background-color: #0E1117;
}
.big-title {
    font-size:40px;
    font-weight:bold;
    text-align:center;
    color:#FFFFFF;
}
.sub-title {
    font-size:20px;
    text-align:center;
    color:#A5F3FC;
}
.result-box {
    background-color: #FFFFFF;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 25px;
    border-left: 6px solid #2563EB;
    box-shadow: 0 6px 15px rgba(0,0,0,0.15);
}
.result-box h3 {
    color: #111827;
    font-size: 22px;
    margin-bottom: 10px;
}
.result-box p {
    color: #1F2937;
    font-size: 16px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# =========================
# CHARGEMENT DES DONNÉES
# =========================
df = pd.read_excel("Arise.xlsx", sheet_name="regles", engine="openpyxl")

# =========================
# BIBLIOTHÈQUE EXPLICATIONS
# =========================
explications = {
    "Mathématiques – Informatique": [
        "Ton goût pour la logique et les chiffres montre une capacité à raisonner de manière structurée. Cette filière te permettra de transformer cette rigueur en solutions technologiques concrètes.",
        "Tu as un esprit analytique et une affinité avec les mathématiques. Cette filière est idéale pour développer des compétences solides en informatique et en raisonnement abstrait."
    ],
    "Statistique": [
        "Tu aimes analyser et interpréter les données. La statistique te permettra de donner du sens aux chiffres et d’éclairer la prise de décision.",
        "Ton attrait pour la précision et les chiffres correspond parfaitement à la statistique."
    ],
    "Intelligence artificielle": [
        "Tu es attiré par l’innovation et les technologies avancées. L’intelligence artificielle te permettra de concevoir des systèmes capables d’apprendre et d’évoluer.",
        "Ton profil montre une curiosité pour les technologies intelligentes et les systèmes complexes."
    ],
    "Génie civil": [
        "Tu es attiré par le concret et la construction. Le génie civil te permettra de participer à la réalisation d’infrastructures utiles à la société.",
        "Ton goût pour l’organisation et les projets à long terme correspond bien au génie civil."
    ],
    "Finance et comptabilité": [
        "Tu as une affinité avec les chiffres et la gestion. Cette filière te permettra de comprendre et piloter les décisions financières.",
        "Ton profil montre une capacité à analyser, organiser et anticiper les enjeux économiques."
    ]
}

# =========================
# FONCTION GÉNÉRATION MESSAGE
# =========================
def generer_message(filiere, raisons):
    # Cas 1 : explication écrite à l'avance
    if filiere in explications:
        return random.choice(explications[filiere])

    # Cas 2 : génération à partir des raisons
    if raisons:
        raisons_uniques = list(set(raisons))
        texte = " ; ".join(raisons_uniques)
        return (
            f"Cette filière est recommandée car {texte}. "
            "Elle correspond à ton profil scolaire, à tes centres d’intérêt et à ta manière de travailler."
        )

    # Cas 3 : sécurité
    return (
        "Cette filière correspond globalement à ton profil et offre des perspectives intéressantes après le bac."
    )

# =========================
# SESSION STATE
# =========================
if "step" not in st.session_state:
    st.session_state.step = 0

# =========================
# ÉTAPE 0 – ACCUEIL
# =========================
if st.session_state.step == 0:
    st.markdown('<p class="big-title">🎓 Orientation scolaire</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Découvre les filières qui te correspondent vraiment</p>', unsafe_allow_html=True)

    if st.button("🚀 Commencer"):
        st.session_state.step = 1
        st.rerun()

# =========================
# ÉTAPE 1 – MATIÈRES
# =========================
elif st.session_state.step == 1:
    st.header("📘 Quelles sont tes matières préférées ?")
    st.session_state.matieres = st.multiselect(
        "Choisis une ou plusieurs matières",
        sorted(df["matiere"].dropna().unique())
    )

    if st.button("Continuer ➡️"):
        st.session_state.step = 2
        st.rerun()

# =========================
# ÉTAPE 2 – INTÉRÊTS
# =========================
elif st.session_state.step == 2:
    st.header("💡 Quels sont tes centres d’intérêt ?")
    st.session_state.interets = st.multiselect(
        "Sélectionne ce qui t’attire le plus",
        sorted(df["interet"].dropna().unique())
    )

    if st.button("Continuer ➡️"):
        st.session_state.step = 3
        st.rerun()

# =========================
# ÉTAPE 3 – STYLE
# =========================
elif st.session_state.step == 3:
    st.header("⚙️ Comment aimes-tu travailler ?")
    st.session_state.styles = st.multiselect(
        "Choisis ton style de travail",
        sorted(df["style"].dropna().unique())
    )

    if st.button("Voir mes résultats 🎯"):
        st.session_state.step = 4
        st.rerun()

# =========================
# ÉTAPE 4 – RÉSULTATS
# =========================
elif st.session_state.step == 4:
    st.header("🎯 Filières recommandées pour toi")

    scores = {}

    for _, row in df.iterrows():
        filiere = row["filiere"]
        score = 0
        raisons = []

        if row["matiere"] in st.session_state.matieres:
            score += 4
            raisons.append(f"tu apprécies la matière {row['matiere']}")

        if row["interet"] in st.session_state.interets:
            score += 3
            raisons.append(f"tu t’intéresses à {row['interet']}")

        if row["style"] in st.session_state.styles:
            score += 2
            raisons.append(f"ton style de travail est « {row['style']} »")

        if score > 0:
            if filiere not in scores:
                scores[filiere] = {"score": 0, "raisons": []}

            scores[filiere]["score"] += score
            scores[filiere]["raisons"].extend(raisons)

    if scores:
        top_filieres = sorted(
            scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )[:3]

        for filiere, data in top_filieres:
            message = generer_message(filiere, data["raisons"])

            st.markdown(f"""
            <div class="result-box">
                <h3>🎓 {filiere}</h3>
                <p><strong>Pourquoi cette filière ?</strong><br>{message}</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.warning("Aucune correspondance trouvée. Essaie d’autres choix.")

    if st.button("🔄 Recommencer"):
        st.session_state.clear()
        st.rerun()
