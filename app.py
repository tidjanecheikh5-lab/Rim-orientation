import streamlit as st
import pandas as pd

# Charger ton Excel
df = pd.read_excel("Arise.xlsx", sheet_name="regles")

# Configuration de la page
st.set_page_config(page_title="Orientation scolaire", page_icon="🎓", layout="centered")

# CSS personnalisé
st.markdown("""
<style>
body {
    background-color: #F9F9F9;
}
.big-title {
    font-size:40px !important;
    color:#2C3E50;
    text-align:center;
    font-weight:bold;
}
.sub-title {
    font-size:20px !important;
    color:#16A085;
    text-align:center;
}
.result-box {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    border-left: 6px solid #2C3E50;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.result-box h3 {
    color: #2C3E50;
    font-size: 22px;
    margin-bottom: 10px;
}
.result-box p {
    color: #333333;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# Initialiser l'étape
if "step" not in st.session_state:
    st.session_state["step"] = 0

# Étape 0 : Accueil
if st.session_state["step"] == 0:
    st.markdown('<p class="big-title">🎓 Bienvenue sur ton conseiller d’orientation</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Clique sur "Commencer" pour découvrir la filière qui te correspond</p>', unsafe_allow_html=True)
    if st.button("🚀 Commencer"):
        st.session_state["step"] = 1
        st.rerun()

# Étape 1 : Choix des matières
elif st.session_state["step"] == 1:
    st.header("📘 Étape 1 : Choisis tes matières préférées")
    matieres = st.multiselect("Sélectionne :", df["matiere"].unique())
    if st.button("Continuer ➡️"):
        st.session_state["matieres"] = matieres
        st.session_state["step"] = 2
        st.rerun()

# Étape 2 : Choix des centres d’intérêt
elif st.session_state["step"] == 2:
    st.header("💡 Étape 2 : Choisis tes centres d’intérêt")
    interets = st.multiselect("Sélectionne :", df["interet"].unique())
    if st.button("Continuer ➡️"):
        st.session_state["interets"] = interets
        st.session_state["step"] = 3
        st.rerun()

# Étape 3 : Choix du style de travail
elif st.session_state["step"] == 3:
    st.header("⚙️ Étape 3 : Choisis ton style de travail")
    styles = st.multiselect("Sélectionne :", df["style"].unique())
    if st.button("Voir mes résultats 🎯"):
        st.session_state["styles"] = styles
        st.session_state["step"] = 4
        st.rerun()

# Étape 4 : Résultats
elif st.session_state["step"] == 4:
    st.header("🎯 Résultats : Tes filières conseillées")
    matieres = st.session_state.get("matieres", [])
    interets = st.session_state.get("interets", [])
    styles = st.session_state.get("styles", [])

    resultat = df[
        (df["matiere"].isin(matieres)) &
        (df["interet"].isin(interets)) &
        (df["style"].isin(styles))
    ]

    if not resultat.empty:
        filieres = resultat["filiere"].unique()[:3]
        for filiere in filieres:
            st.markdown(f"""
            <div class="result-box">
            <h3>➡️ {filiere}</h3>
            <p>Cette filière correspond à tes choix et ouvre des débouchés intéressants.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Aucune correspondance trouvée. Essaie une autre combinaison.")

    if st.button("🔄 Recommencer"):
        st.session_state.clear()
        st.session_state["step"] = 0
        st.rerun()