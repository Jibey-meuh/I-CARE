import streamlit as st
from groq import Groq

# Configuration de la page
st.set_page_config(
    page_title="Projet I-CARE - Assistant Voyage",
    page_icon="🌍",
    layout="wide"
)

# Initialisation du client Groq en utilisant les Secrets de Streamlit
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Clé API Groq manquante. Veuillez la configurer dans les Secrets de Streamlit Cloud.")
    st.stop()

# Style CSS personnalisé pour l'interface
st.markdown("""
    <style>
    .main-title { font-size: 42px; font-weight: bold; color: #FF4B4B; text-align: center; margin-bottom: 10px; }
    .subtitle { font-size: 18px; text-align: center; color: #555555; margin-bottom: 30px; }
    .section-box { padding: 20px; border-radius: 10px; background-color: #f9f9f9; border-left: 5px solid #FF4B4B; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("<div class='main-title'>🌍 Projet I-CARE</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Votre hub de sécurité et de logistique internationale géré par IA</div>", unsafe_allow_html=True)

# Barre latérale : Entrée utilisateur et filtres
st.sidebar.header("📍 Configuration de la recherche")
ville = st.sidebar.text_input("Entrez une ville ou un point géographique :", placeholder="Ex: Tokyo, Lima, Nairobi...")

st.sidebar.subheader("🔍 Informations à inclure :")
opt_urgences = st.sidebar.checkbox("🚨 Urgences locales & Numéros utiles", value=True)
opt_ambassade = st.sidebar.checkbox("🇨🇳 Ambassade / Consulat français le plus proche", value=True)
opt_hopitaux = st.sidebar.checkbox("🏥 Hôpitaux & Notes estimées", value=True)
opt_urg_heb = st.sidebar.checkbox("⛺ Hébergements d'urgence", value=False)
opt_woofing = st.sidebar.checkbox("🌱 Sites de WWOOFing disponibles", value=False)
opt_habitant = st.sidebar.checkbox("🏠 Logements chez l'habitant les mieux notés", value=False)
opt_supermarches = st.sidebar.checkbox("🛒 Supermarchés les mieux notés", value=False)

# Déclenchement de la recherche
if st.sidebar.button("Générer la feuille de route I-CARE 🚀"):
    if not ville.strip():
        st.warning("Veuillez entrer une destination valide avant de lancer la recherche.")
    else:
        with st.spinner(f"Analyse des infrastructures pour {ville} en cours..."):
            
            # Construction dynamique du prompt selon les options cochées
            sections_requises = []
            if opt_urgences:
                sections_requises.append("- Les numéros d'urgence locaux (Police, Ambulance, Pompiers) et consignes immédiates.")
            if opt_ambassade:
                sections_requises.append("- L'adresse et les coordonnées de l'Ambassade ou du Consulat français le plus proche.")
            if opt_hopitaux:
                sections_requises.append("- Les hôpitaux majeurs recommandés avec une estimation de leur notation/réputation globale.")
            if opt_urg_heb:
                sections_requises.append("- Les structures ou zones d'hébergements d'urgence accessibles.")
            if opt_woofing:
                sections_requises.append("- Les opportunités ou plateformes de WWOOFing actives dans cette région.")
            if opt_habitant:
                sections_requises.append("- Les meilleures adresses/zones de logement chez l'habitant classées par retour d'expérience.")
            if opt_supermarches:
                sections_requises.append("- Les supermarchés ou marchés d'alimentation générale les mieux notés de la zone.")

            prompt_instructions = "\n".join(sections_requises)

            # Prompt système et utilisateur pour Groq
            system_prompt = (
                "Tu es l'intelligence centrale du Projet I-CARE (International Care & Assistance Resource Engine). "
                "Ton rôle est de fournir un rapport de logistique et de sécurité factuel, précis et structuré pour les voyageurs français. "
                "Sois direct, utilise des listes à puces et mets en évidence les adresses et numéros de téléphone."
            )
            
            user_prompt = f"""
            Génère un rapport complet pour la destination suivante : **{ville}**.
            Tu dois exclusivement traiter les sections suivantes qui ont été sélectionnées par l'utilisateur :
            {prompt_instructions}
            
            Présente les données de manière claire, lisible et compartimentée avec des titres pertinents.
            """

            try:
                # Appel à l'architecture ultra-rapide de Groq (Llama 3.1 8B)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model="llama-3.1-8b-instant",
                    temperature=0.2,  # Basse température pour maximiser la rigueur factuelle
                )
                
                # Affichage du résultat
                reponse = chat_completion.choices[0].message.content
                st.success(f"Rapport I-CARE généré avec succès pour {ville} ! ✨")
                st.markdown(f"<div class='section-box'>{reponse}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Une erreur technique est survenue lors de la génération : {e}")

else:
    # Message d'accueil par défaut si aucune recherche n'est lancée
    st.info("💡 Saisissez une destination dans le panneau latéral gauche et cochez les services dont vous avez besoin pour voir la magie opérer.")
