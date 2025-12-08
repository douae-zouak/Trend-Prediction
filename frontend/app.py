import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import io
import base64
from datetime import datetime, timedelta
from PIL import Image

# ⚙️ Configuration de la page
st.set_page_config(
    page_title="Prédiction des Ventes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Application de prédiction développée par ZOUAK Douae et EL HRIOUI Chahd"
    }
)

API_URL = "http://localhost:8000"

# 🎨 Styles globaux modernisés
st.markdown("""
<style>
/* --------- GLOBAL APP --------- */
.stApp {
    background: radial-gradient(circle at top left, #0B0F19 0%, #121826 40%, #0B0F19 100%);
    color: #F0F2F6;
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
    max-width: 1200px;
}

footer {visibility: hidden;}
header {background: transparent;}

/* --------- HEADER --------- */
.main-header {
    font-size: 2.6rem;
    text-align: left;
    margin: 0 0 0.5rem 0;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 25%, #06B6D4 50%, #10B981 75%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-size: 200% auto;
    animation: gradientShift 8s ease infinite;
}

@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.main-subtitle {
    font-size: 1rem;
    color: #94A3B8;
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* --------- SIDEBAR --------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    border-right: 1px solid rgba(99, 102, 241, 0.15);
}

.sidebar-logo {
    text-align: center;
    padding: 1.5rem 0 0.8rem 0;
    font-weight: 700;
    font-size: 1.2rem;
    color: #E2E8F0;
    background: linear-gradient(135deg, #818CF8, #3B82F6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sidebar-badge {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #6366F1;
    text-align: center;
    margin-bottom: 2rem;
    padding: 0.4rem 1rem;
    background: rgba(99, 102, 241, 0.1);
    border-radius: 20px;
    display: inline-block;
    width: auto;
    margin-left: auto;
    margin-right: auto;
}

.sidebar-title {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #8B5CF6;
    margin-top: 1rem;
    margin-bottom: 1rem;
    padding-left: 1rem;
}

/* Navigation radio */
[data-testid="stSidebar"] .stRadio > label {
    font-size: 0.95rem;
    font-weight: 500;
    color: #CBD5E1;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    border-radius: 12px;
    padding: 0.6rem 1rem;
    margin-bottom: 0.35rem;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid transparent;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    background: rgba(99, 102, 241, 0.08);
    border-color: rgba(99, 102, 241, 0.2);
    transform: translateX(4px);
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.15));
    color: #FFFFFF;
    border: 1px solid rgba(99, 102, 241, 0.4);
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2);
}

/* --------- SECTION TITLES --------- */
.sub-header {
    font-size: 1.5rem;
    font-weight: 700;
    color: #F1F5F9;
    margin-bottom: 1rem;
    position: relative;
    padding-bottom: 0.5rem;
}

.sub-header::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, #8B5CF6, #3B82F6);
    border-radius: 2px;
}

.section-caption {
    font-size: 0.95rem;
    color: #94A3B8;
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* --------- METRIC CARDS --------- */



.metric-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #8B5CF6, #3B82F6, transparent);
}

.metric-card:hover {
    cursor: pointer;
    transform: translateY(-5px);
    border-color: rgba(99, 102, 241, 0.4);
    box-shadow: 
        0 20px 40px rgba(15, 23, 42, 0.6),
        0 0 30px rgba(99, 102, 241, 0.1);
}





/* --------- BOUTONS --------- */
.stButton>button {
    background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
    color: #FFFFFF;
    border: none;
    padding: 0.8rem 2rem;
    border-radius: 12px;
    font-weight: 600;
    letter-spacing: 0.03em;
    font-size: 0.95rem;
    box-shadow: 
        0 4px 20px rgba(99, 102, 241, 0.3),
        0 0 0 1px rgba(255, 255, 255, 0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.stButton>button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transition: left 0.6s;
}

.stButton>button:hover::before {
    left: 100%;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 
        0 8px 30px rgba(99, 102, 241, 0.4),
        0 0 0 1px rgba(255, 255, 255, 0.1);
    background: linear-gradient(135deg, #9F7AEA 0%, #4F8BF6 100%);
}

.stButton>button:active {
    transform: translateY(0);
    box-shadow: 
        0 2px 10px rgba(99, 102, 241, 0.3),
        0 0 0 1px rgba(255, 255, 255, 0.05);
}

/* --------- ALERTES --------- */
.stAlert {
    border-radius: 16px;
    border: 1px solid rgba(99, 102, 241, 0.2);
    background: rgba(30, 41, 59, 0.8);
}

/* --------- TABLES --------- */
.dataframe, .stDataFrame {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(99, 102, 241, 0.1);
}

/* --------- FOOTER --------- */
.custom-footer {
    text-align: center;
    color: #64748B;
    font-size: 0.85rem;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(99, 102, 241, 0.1);
}

.custom-footer a {
    color: #60A5FA;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.custom-footer a:hover {
    color: #38BDF8;
    text-decoration: underline;
}

/* Scrollbar personnalisée */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.5);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #8B5CF6, #3B82F6);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #9F7AEA, #4F8BF6);
}
</style>
""", unsafe_allow_html=True)


# 🧭 Sidebar
with st.sidebar:
    st.markdown("<div class='sidebar-logo'>Sales Forecast Studio</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-badge'>Prophet • Time Series</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-title'>Navigation</div>", unsafe_allow_html=True)
    page = st.radio(
        "",
        ["🏠 Accueil", "📊 Prédiction Automatique", "📁 Upload CSV", "⚙️ Paramètres Avancés"]
    )

    st.markdown("---")
    st.markdown("<div class='sidebar-title'>À propos</div>", unsafe_allow_html=True)
    st.info(
        "Application de prévision de ventes basée sur Prophet, avec visualisations interactives et métriques de performance."
    )

# 🔌 Fonctions utilitaires
def check_api_connection():
    try:
        response = requests.get(f"{API_URL}/health")
        return response.status_code == 200
    except:
        return False

def display_metrics(metrics_data):
    if metrics_data:
        cols = st.columns(3)
        with cols[0]:
            st.metric(
                label="MAE (Erreur Moyenne Absolue)",
                value=f"{metrics_data.get('MAE', 0):.2f}"
            )
        with cols[1]:
            st.metric(
                label="RMSE (Racine Carrée Erreur Moyenne)",
                value=f"{metrics_data.get('RMSE', 0):.2f}"
            )
        with cols[2]:
            st.metric(
                label="R² (Score de Détermination)",
                value=f"{metrics_data.get('R2', 0):.2f}"
            )

# 🏠 Page d'accueil
if page == "🏠 Accueil":
    st.markdown("<h1 class='main-header'>📊 Dashboard de Prédiction des Ventes</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='main-subtitle'>Anticipez vos ventes, sécurisez vos décisions et explorez vos scénarios en quelques clics.</div>",
        unsafe_allow_html=True
    )

    api_status = check_api_connection()
    if api_status:
        st.success("✅ Connecté au serveur de prédiction")
    else:
        st.error("❌ Impossible de se connecter au serveur. Veuillez démarrer le backend.")

    st.markdown("### Vue d’ensemble rapide")
    st.markdown("<div class='section-caption'>Aperçu des paramètres clés de votre moteur de prédiction.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('''
            <div id="metric-card" class="metric-card" style="
                position: relative;
                background: linear-gradient(145deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
                border-radius: 20px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                color: #F8FAFC;
                box-shadow: 
                    0 10px 30px rgba(15, 23, 42, 0.5),
                    inset 0 1px 0 rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(99, 102, 241, 0.2);
                backdrop-filter: blur(20px);
                overflow: hidden;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                text-align: center;
                min-height: 120px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                cursor: pointer;
            "
            onmouseover="this.style.transform='translateY(-5px)';this.style.borderColor='rgba(99, 102, 241, 0.4)';this.style.boxShadow='0 20px 40px rgba(15, 23, 42, 0.6), 0 0 30px rgba(99, 102, 241, 0.1)'"
            onmouseout="this.style.transform='translateY(0)';this.style.borderColor='rgba(99, 102, 241, 0.2)';this.style.boxShadow='0 10px 30px rgba(15, 23, 42, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.05)'"
            >
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 1px;
                    background: linear-gradient(90deg, transparent, #8B5CF6, #3B82F6, transparent);
                "></div>
                <div style="
                    font-size: 16px;
                    text-transform: uppercase;
                    letter-spacing: 0.15em;
                    color: #94A3B8;
                    margin-bottom: 10px;
                    font-weight: 500;
                ">
                    Horizon de prévision
                </div>
                <div style="
                    font-size: 28px;
                    font-weight: bold;
                    background: linear-gradient(135deg, #8B5CF6, #3B82F6);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin-bottom: 0.5rem;
                    line-height: 1.2;
                ">
                    3 mois
                </div>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown('''
        <div class="metric-card" style="
            position: relative;
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            color: #F8FAFC;
            box-shadow: 
                0 10px 30px rgba(15, 23, 42, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(99, 102, 241, 0.2);
            backdrop-filter: blur(20px);
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-align: center;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, #8B5CF6, #3B82F6, transparent);
            "></div>
            <div style="
                font-size: 16px;
                text-transform: uppercase;
                letter-spacing: 0.15em;
                color: #94A3B8;
                margin-bottom: 10px;
                font-weight: 500;
            ">
                Précision cible
            </div>
            <div style="
                font-size: 28px;
                font-weight: bold;
                background: linear-gradient(135deg, #8B5CF6, #3B82F6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
                line-height: 1.2;
            ">
                ≥ 85 %
            </div>
        </div>
    ''', unsafe_allow_html=True)

    with col3:
        st.markdown('''
        <div class="metric-card" style="
            position: relative;
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            color: #F8FAFC;
            box-shadow: 
                0 10px 30px rgba(15, 23, 42, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(99, 102, 241, 0.2);
            backdrop-filter: blur(20px);
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-align: center;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, #8B5CF6, #3B82F6, transparent);
            "></div>
            <div style="
                font-size: 16px;
                text-transform: uppercase;
                letter-spacing: 0.15em;
                color: #94A3B8;
                margin-bottom: 10px;
                font-weight: 500;
            ">
                Temps de réponse
            </div>
            <div style="
                font-size: 28px;
                font-weight: bold;
                background: linear-gradient(135deg, #8B5CF6, #3B82F6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
                line-height: 1.2;
            ">
                < 5 sec
            </div>
        </div>
    ''', unsafe_allow_html=True)
   
    st.markdown("### Comment démarrer")
    st.info(
        "1. **Prédiction Automatique** : générez instantanément les ventes des 3 prochains mois.\n"
        "2. **Upload CSV** : importez vos historiques pour des prévisions personnalisées.\n"
        "3. **Paramètres Avancés** : ajustez l’horizon de prévision et les dates de départ."
    )

    if st.button("🚀 Lancer une prédiction automatique"):
        st.session_state["page"] = "📊 Prédiction Automatique"
        st.experimental_rerun()

# 📊 Page de prédiction automatique
elif page == "📊 Prédiction Automatique":
    st.markdown("<h2 class='sub-header'>Prédiction Automatique des 3 Prochains Mois</h2>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-caption'>Lancez une prévision complète basée sur vos données historiques déjà configurées côté backend.</div>",
        unsafe_allow_html=True
    )

    if st.button("🔮 Générer la prédiction"):
        with st.spinner("Génération des prédictions..."):
            try:
                response = requests.post(f"{API_URL}/predict-next-months")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        predictions = data.get("monthly_predictions", [])
                        df_pred = pd.DataFrame(predictions)

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            total_pred = df_pred['predicted_sales'].sum()
                            st.metric("Total prédit (3 mois)", f"{total_pred:,.0f} €")
                        with col2:
                            avg_monthly = df_pred['predicted_sales'].mean()
                            st.metric("Moyenne mensuelle", f"{avg_monthly:,.0f} €")
                        with col3:
                            max_month = df_pred.loc[df_pred['predicted_sales'].idxmax(), 'month']
                            st.metric("Meilleur mois", max_month)

                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=df_pred['month'],
                            y=df_pred['predicted_sales'],
                            name='Ventes prédites',
                            marker_color='#6366F1',
                            text=df_pred['predicted_sales'].apply(lambda x: f"{x:,.0f}€"),
                            textposition='auto',
                        ))

                        if 'predicted_range' in df_pred.columns:
                            lower_vals = [r['lower'] for r in df_pred['predicted_range']]
                            upper_vals = [r['upper'] for r in df_pred['predicted_range']]

                            fig.add_trace(go.Scatter(
                                x=df_pred['month'],
                                y=upper_vals,
                                mode='lines',
                                line=dict(width=0),
                                showlegend=False,
                                hoverinfo='skip'
                            ))
                            fig.add_trace(go.Scatter(
                                x=df_pred['month'],
                                y=lower_vals,
                                mode='lines',
                                line=dict(width=0),
                                fillcolor='rgba(99,102,241,0.22)',
                                fill='tonexty',
                                showlegend=False,
                                hoverinfo='skip'
                            ))

                        fig.update_layout(
                            title='Prédiction des Ventes - 3 prochains mois',
                            xaxis_title='Mois',
                            yaxis_title='Ventes prédites (€)',
                            hovermode='x unified',
                            template='plotly_white',
                            height=500
                        )

                        st.plotly_chart(fig, use_container_width=True)

                        st.markdown("### 📋 Détails des prédictions")
                        display_df = df_pred.copy()
                        display_df['predicted_sales'] = display_df['predicted_sales'].apply(lambda x: f"{x:,.0f} €")
                        if 'predicted_range' in display_df.columns:
                            display_df['intervalle'] = display_df['predicted_range'].apply(
                                lambda x: f"{x['lower']:,.0f} - {x['upper']:,.0f} €"
                            )
                            display_df = display_df[['month', 'predicted_sales', 'intervalle']]

                        st.dataframe(display_df, use_container_width=True)

                        csv = df_pred.to_csv(index=False)
                        st.download_button(
                            label="📥 Télécharger les prédictions (CSV)",
                            data=csv,
                            file_name=f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.error(f"Erreur: {data.get('error', 'Erreur inconnue')}")
                else:
                    st.error(f"Erreur API: {response.status_code}")
            except Exception as e:
                st.error(f"Erreur: {str(e)}")

# 📁 Page upload CSV
elif page == "📁 Upload CSV":
    st.markdown("<h2 class='sub-header'>Prédiction à partir de fichier CSV</h2>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-caption'>Importez vos données historiques pour entraîner et évaluer le modèle sur votre propre base.</div>",
        unsafe_allow_html=True
    )

    st.info(
        "**Format CSV requis :**\n"
        "- Colonne de date : `Date Order was placed` ou `date`\n"
        "- Colonne de ventes : `Total Retail Price for This Order` ou `sales`\n"
        "- Format date : `YYYY-MM-DD`"
    )

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Fichier chargé : {uploaded_file.name}")
            st.markdown("### Aperçu des données")
            st.dataframe(df.head(), use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                predict_button = st.button("🚀 Lancer la prédiction", use_container_width=True)
            with col2:
                show_stats = st.checkbox("Afficher les statistiques", value=True)

            if predict_button:
                with st.spinner("Analyse en cours..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                        response = requests.post(f"{API_URL}/predict-csv", files=files)

                        if response.status_code == 200:
                            data = response.json()
                            if data.get("success"):
                                if data.get("plot"):
                                    plot_data = base64.b64decode(data["plot"])
                                    st.image(plot_data, caption="Prédictions vs Réelles")

                                if show_stats and data.get("metrics"):
                                    st.markdown("### 📊 Métriques de performance")
                                    display_metrics(data["metrics"])

                                st.markdown("### 🔮 Dernières prédictions")
                                predictions = data.get("predictions", [])
                                df_predictions = pd.DataFrame(predictions)
                                st.dataframe(df_predictions, use_container_width=True)

                                csv_data = df_predictions.to_csv(index=False)
                                st.download_button(
                                    label="📥 Exporter les prédictions",
                                    data=csv_data,
                                    file_name="predictions_export.csv",
                                    mime="text/csv"
                                )
                            else:
                                st.error(f"Erreur: {data.get('error')}")
                        else:
                            st.error(f"Erreur API: {response.status_code}")
                    except Exception as e:
                        st.error(f"Erreur lors de la prédiction: {str(e)}")
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier: {str(e)}")

# ⚙️ Page paramètres avancés
elif page == "⚙️ Paramètres Avancés":
    st.markdown("<h2 class='sub-header'>Paramètres avancés</h2>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-caption'>Affinez l’horizon temporel et testez la connexion à votre backend de prédiction.</div>",
        unsafe_allow_html=True
    )

    st.markdown("### 🔌 Test de connexion API")
    if st.button("Tester la connexion"):
        if check_api_connection():
            st.success("✅ Connecté avec succès au backend !")
        else:
            st.error("❌ Impossible de se connecter au backend")

    st.markdown("### 🎯 Paramètres de prédiction personnalisée")
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Date de début",
            value=datetime.now(),
            min_value=datetime.now() - timedelta(days=365),
            max_value=datetime.now() + timedelta(days=365)
        )

    with col2:
        periods = st.slider(
            "Période de prédiction (jours)",
            min_value=30,
            max_value=180,
            value=90,
            step=30
        )

    if st.button("🎯 Lancer une prédiction personnalisée"):
        with st.spinner("Calcul en cours..."):
            try:
                request_data = {
                    "start_date": start_date.strftime('%Y-%m-%d'),
                    "periods": periods
                }
                response = requests.post(f"{API_URL}/predict", json=request_data)

                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        if data.get("plot_data"):
                            plot_base64 = data["plot_data"]["plot"]
                            plot_data = base64.b64decode(plot_base64)
                            st.image(plot_data, caption=f"Prédiction pour {periods} jours")

                        predictions = data.get("predictions", [])
                        if predictions:
                            st.markdown("### 📋 Aperçu des prédictions")
                            df_preview = pd.DataFrame(predictions[:10])
                            st.dataframe(df_preview, use_container_width=True)
                    else:
                        st.error(f"Erreur: {data.get('error')}")
                else:
                    st.error(f"Erreur API: {response.status_code}")
            except Exception as e:
                st.error(f"Erreur: {str(e)}")

    st.markdown("### 🧩 Informations système")
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Statut API", "✅ En ligne" if health_data.get("model_loaded") else "⚠️ Partiel")
            with col2:
                st.metric("Modèle", "✅ Chargé" if health_data.get("model_loaded") else "❌ Absent")
            with col3:
                last_update = health_data.get("timestamp", "").split("T")[0]
                st.metric("Dernière vérification", last_update)
    except:
        st.warning("Impossible de récupérer les informations système")

# 🦶 Pied de page
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='custom-footer'>
        Dashboard de Prédiction des Ventes • Propulsé par Prophet • 
        <a href='#'>Documentation</a> • 
        <a href='#'>Support</a>
    </div>
    """,
    unsafe_allow_html=True
)
