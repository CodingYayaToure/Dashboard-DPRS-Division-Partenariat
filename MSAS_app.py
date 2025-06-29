import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt


# --- FONCTION POUR LE TITRE DYNAMIQUE (VERSION ALLER-RETOUR) ---
def dynamic_typing_header(title, subtitle, title_color="#2F3C7E", cursor_color="#2F3C7E", 
                          typing_speed=70, delete_speed=40, pause_duration=1500):
    """
    Crée un composant HTML avec un effet de machine à écrire en boucle (aller-retour).
    
    Args:
        title (str): Le texte du titre principal.
        subtitle (str): Le texte du sous-titre.
        title_color (str): La couleur CSS pour le titre.
        cursor_color (str): La couleur CSS pour le curseur clignotant.
        typing_speed (int): Vitesse de frappe en millisecondes.
        delete_speed (int): Vitesse de suppression en millisecondes.
        pause_duration (int): Pause avant de supprimer le texte en millisecondes.
    """
    title_safe = title.replace("'", "\\'")
    subtitle_safe = subtitle.replace("'", "\\'")

    html_code = f"""
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        body {{ font-family: 'Roboto', sans-serif; background-color: transparent; }}
        
        .dynamic-title-container {{
            min-height: 120px; /* Espace total réservé pour éviter les sauts de page */
        }}
        .dynamic-title {{
            font-size: 2.2rem; font-weight: 700; color: {title_color};
            border-bottom: 3px solid {title_color};
            padding-bottom: 10px; margin-bottom: 0.5rem; min-height: 50px;
        }}
        .dynamic-subtitle {{
            font-size: 1.1rem; color: #333333; min-height: 30px;
        }}
        .typing-cursor {{
            display: inline-block; width: 10px; height: 1.7rem;
            background-color: {cursor_color}; animation: blink 1s step-end infinite;
            vertical-align: bottom;
        }}
        @keyframes blink {{
            from, to {{ background-color: transparent; }}
            50% {{ background-color: {cursor_color}; }}
        }}
    </style>
    </head>
    <body>
        <div class="dynamic-title-container">
            <div id="dynamic-title" class="dynamic-title"><span class="typing-cursor"></span></div>
            <div id="dynamic-subtitle" class="dynamic-subtitle"></div>
        </div>

        <script>
            const titleElement = document.getElementById('dynamic-title');
            const subtitleElement = document.getElementById('dynamic-subtitle');
            
            const titleText = '{title_safe}';
            const subtitleText = '{subtitle_safe}';
            const typingSpeed = {typing_speed};
            const deleteSpeed = {delete_speed};
            const pause = {pause_duration};

            // Fonction pour écrire le texte
            function typeWriter(element, text, index, callback) {{
                if (index < text.length) {{
                    element.innerHTML = text.substring(0, index + 1) + '<span class="typing-cursor"></span>';
                    setTimeout(() => typeWriter(element, text, index + 1, callback), typingSpeed);
                }} else {{
                    if (callback) setTimeout(callback, pause); // Pause avant d'exécuter la suite
                }}
            }}

            // Fonction pour effacer le texte
            function deleteWriter(element, callback) {{
                let text = element.innerHTML.replace('<span class="typing-cursor"></span>', '');
                let index = text.length;
                if (index > 0) {{
                    element.innerHTML = text.substring(0, index - 1) + '<span class="typing-cursor"></span>';
                    setTimeout(() => deleteWriter(element, callback), deleteSpeed);
                }} else {{
                    if (callback) callback();
                }}
            }}

            // La boucle infinie qui orchestre l'animation
            function startAnimationCycle() {{
                typeWriter(titleElement, titleText, 0, () => {{
                    deleteWriter(titleElement, () => {{
                        subtitleElement.innerHTML = '<span class="typing-cursor"></span>'; // Met le curseur sur la 2e ligne
                        typeWriter(subtitleElement, subtitleText, 0, () => {{
                            deleteWriter(subtitleElement, () => {{
                                startAnimationCycle(); // Recommence le cycle
                            }});
                        }});
                    }});
                }});
            }}

            document.addEventListener('DOMContentLoaded', startAnimationCycle);
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=180)

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Dashboard Avancé MSAS - CSU Sénégal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)



# --- INJECTION DU CSS PROFESSIONNEL ---
professional_styling = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
:root {
    --primary-color: #2F3C7E; --secondary-color: #1E2757; --accent-color: #FBEAEB;
    --background-color: #F0F2F6; --text-color: #333333; --light-text-color: #FFFFFF;
}
html, body, [class*="st-"] { font-family: 'Roboto', sans-serif; }
.main { background-color: var(--background-color); }
[data-testid="stSidebar"] { background: linear-gradient(200deg, var(--primary-color), var(--secondary-color)); }
[data-testid="stSidebar"] div, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p, 
[data-testid="stSidebar"] label, [data-testid="stSidebar"] li { color: var(--light-text-color) !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: var(--accent-color) !important; text-transform: uppercase; }
[data-testid="stSidebar"] hr { background-color: var(--accent-color); height: 2px; border: none; margin: 15px 0; }
[data-testid="stTabs"] { background-color: var(--background-color); padding-top: 10px; }
[data-testid="stTabs"] button { background-color: transparent; color: var(--text-color); border: none; border-bottom: 2px solid transparent; transition: all 0.3s ease; }
[data-testid="stTabs"] button:hover { background-color: #E0E0E0; border-bottom: 2px solid var(--primary-color); }
[data-testid="stTabs"] button[aria-selected="true"] { background-color: var(--primary-color); color: var(--light-text-color); font-weight: 700; border-bottom: 2px solid var(--primary-color); box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
[data-testid="stHeading"] h2 { border-left: 5px solid var(--primary-color); padding-left: 15px; color: var(--primary-color); }
[data-testid="stMetric"] { background-color: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 10px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); transition: all 0.2s ease-in-out; }
[data-testid="stMetric"]:hover { transform: scale(1.03); box-shadow: 0 6px 16px rgba(0,0,0,0.12); }
[data-testid="stExpander"] summary { background-color: var(--accent-color); color: var(--primary-color); border-radius: 5px; font-weight: 700; }
</style>
"""
st.markdown(professional_styling, unsafe_allow_html=True)


# --- FONCTIONS UTILITAIRES ---
def apply_professional_theme(fig):
    fig.update_layout(template="plotly_white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Roboto, sans-serif", size=12, color="#333333"), title_font_color="#2F3C7E", title_font_size=18, legend_font_size=12)
    return fig


# --- CHARGEMENT ET PRÉPARATION DES DONNÉES ---
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('Final_Full__type_colonnes_Cleaned.csv')
    except UnicodeDecodeError:
        data = pd.read_csv('Final_Full__type_colonnes_Cleaned.csv', encoding='latin1')

    data['Type'] = data['NOM DES STRUCTURES SANITAIRES CIBLES'].apply(
        lambda x: 'Hôpital' if 'hopital' in str(x).lower()
        else 'Centre de Santé' if 'centre de santé' in str(x).lower()
        else 'Poste de Santé' if 'poste de santé' in str(x).lower()
        else 'EPS' if 'eps' in str(x).lower()
        else 'Autre')
    
    #data['Région'] = data['Région'].str.strip().str.upper()
    # Création de colonnes dérivées pour l'analyse
    data['Type'] = data['NOM DES STRUCTURES SANITAIRES CIBLES'].apply(lambda x: 'Hôpital' if 'hopital' in str(x).lower() else 'Centre de Santé' if 'centre de santé' in str(x).lower() else 'Poste de Santé' if 'poste de santé' in str(x).lower() else 'EPS' if 'eps' in str(x).lower() else 'Autre')
    data['Région'] = data['Région'].str.strip().str.upper()
    data['Statut Convention'] = np.where(data['Nb Conventions Signées'] > 0, 'Signée', 'Non Signée')
    return data


# --- FONCTION POUR LE GRAPHIQUE ANIME ---
def create_animated_summary_chart(nb_signe, nb_non_signe):
    """
    Crée un graphique à barres animé qui montre la transition des décomptes
    des conventions signées vs non signées.
    """
    total = nb_signe + nb_non_signe
    if total == 0:
        # Affiche un message si aucune donnée n'est disponible
        fig = go.Figure()
        fig.update_layout(
            title="Aucune donnée à afficher pour les filtres actuels",
            xaxis = {"visible": False},
            yaxis = {"visible": False},
            annotations=[{
                "text": "Veuillez changer votre sélection de filtres.",
                "xref": "paper", "yref": "paper", "showarrow": False, "font": {"size": 16}
            }]
        )
        return fig

    # Créer les "frames" de l'animation, de 0% à 100%
    animation_steps = []
    for step in range(101):
        progress = step / 100.0
        animation_steps.append({'Statut': '✅ Signée', 'Nombre': nb_signe * progress, 'Étape': step})
        animation_steps.append({'Statut': '❌ Non Signée', 'Nombre': nb_non_signe * progress, 'Étape': step})
    anim_df = pd.DataFrame(animation_steps)

    # Créer le graphique à barres animé avec Plotly Express
    fig = px.bar(
        anim_df,
        x='Statut', y='Nombre', color='Statut',
        animation_frame='Étape',
        color_discrete_map={'✅ Signée': '#28a745', '❌ Non Signée': '#dc3545'},
        labels={'Nombre': 'Nombre de Structures', 'Statut': 'Statut de la Convention'},
        text='Nombre'
    )
    
    # Personnalisation de l'animation et du style
    fig.update_yaxes(range=[0, max(1, nb_signe, nb_non_signe) * 1.15])
    fig.update_traces(texttemplate='%{y:.0f}', textposition='outside')
    fig.update_layout(
        title_text="Répartition Animée des Conventions Signées vs Non Signées",
        showlegend=False,
        updatemenus=[{
            'type': 'buttons',
            'buttons': [
                {'label': '▶️ Rejouer', 'method': 'animate', 'args': [None, {'frame': {'duration': 20, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 5}}]},
            ],
            'direction': 'left', 'pad': {'r': 10, 't': 87}, 'showactive': False,
            'x': 0.1, 'xanchor': 'right', 'y': 0, 'yanchor': 'top'
        }]
    )
    return fig

# --- CORPS DE L'APPLICATION ---
df = load_data()

with st.sidebar:
    # ... (le code de la sidebar reste le même, avec la description en bas) ...
    #st.image("https://upload.wikimedia.org/wikipedia/commons/f/fd/Flag_of_Senegal.svg", width=100)
    st.image("https://www.africa-newsroom.com/files/large/3b2d908cc6dc36e/200/150", width=480)
    st.title("Dashboard DPRS / Division Partenariat")
    st.divider()
    st.header("Filtres de Navigation")
    all_regions = ["Toutes les régions"] + sorted(df['Région'].unique())
    selected_region = st.selectbox("Filtrer par Région:", all_regions)
    if selected_region == "Toutes les régions": filtered_df = df; districts = ["Tous les districts"] + sorted(df['District Sanitaire'].unique())
    else: filtered_df = df[df['Région'] == selected_region]; districts = ["Tous les districts"] + sorted(filtered_df['District Sanitaire'].unique())
    selected_district = st.selectbox("Filtrer par District:", districts)
    if selected_district != "Tous les districts": filtered_df = filtered_df[filtered_df['District Sanitaire'] == selected_district]
    st.divider()
    st.header("Description")
    st.markdown(""" Assurer la Couverture Sanitaire Universel (CSU) des Artisans sur l’étendue du territoire national enfin de leur faciliter l’accès aux soins médicales.

    **12 régions ont été ciblées :** Dakar, Thiès, Saint-Louis, Fatick, Diourbel, Matam, Louga, Kolda, Sédhiou, Ziguinchor, Kaolack et Kaffrine.

    L’objectif général après cette mission est d’évaluer les conventions spécifiques entre la MSNAS et les Structures Sanitaires Publiques du MSAS.""", unsafe_allow_html=True)


# --- TITRE PRINCIPAL ET KPIS (AVEC EFFET DYNAMIQUE ALLER-RETOUR) ---
dynamic_typing_header(
    title="🏥 Dashboard d'Analyse Approfondie de la CSU Sénégal (Protection Contre le risque Financier - MNSA du Sénegal)",
    subtitle="DIRECTION DE LA PLANIFICATION, DE LA RECHERCHE ET DES STATISTIQUES (DPRS) / DIVISION PARTENARIAT",
)
st.markdown("Visualisation détaillée des structures sanitaires conventionnées au Sénégal.")

# df = load_data()

# # --- SIDEBAR AVEC FILTRES ---
# st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/f/fd/Flag_of_Senegal.svg", width=100) 
# st.sidebar.title("Dashboard MSAS")
# st.sidebar.header("Filtres de Navigation")

# all_regions = ["Toutes les régions"] + sorted(df['Région'].unique())
# selected_region = st.sidebar.selectbox("Filtrer par Région:", all_regions)

# if selected_region == "Toutes les régions":
#     filtered_df = df
#     districts = ["Tous les districts"] + sorted(df['District Sanitaire'].unique())
# else:
#     filtered_df = df[df['Région'] == selected_region]
#     districts = ["Tous les districts"] + sorted(filtered_df['District Sanitaire'].unique())

# selected_district = st.sidebar.selectbox("Filtrer par District:", districts)

# if selected_district != "Tous les districts":
#     filtered_df = filtered_df[filtered_df['District Sanitaire'] == selected_district]

# --- TITRE PRINCIPAL ET KPIS ---
# st.title("🏥 Dashboard d'Analyse Approfondie de la CSU Sénégal (Protection Contre le risque Financier - MNSA du Sénegal)")
# st.markdown("Visualisation détaillée des structures sanitaires conventionnées au Sénégal.")

total_structures = len(filtered_df)
regions_couvertes = len(filtered_df['Région'].unique())
districts_sanitaires = len(filtered_df['District Sanitaire'].unique())
moy_structures_region = total_structures / regions_couvertes if regions_couvertes > 0 else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Structures Sanitaires", f"{total_structures}")
kpi2.metric("Régions Couvertes", f"{regions_couvertes}")
kpi3.metric("Districts Sanitaires", f"{districts_sanitaires}")
kpi4.metric("Moy. Structures/Région", f"{moy_structures_region:.1f}")

# Ajout de KPI supplémentaires
kpi5, kpi6, kpi7, kpi8 = st.columns(4)

# Calculs pour nouveaux KPI
type_counts = filtered_df['Type'].value_counts()
type_dominant = type_counts.index[0] if len(type_counts) > 0 else "N/A"
pourcentage_dominant = (type_counts.iloc[0] / total_structures * 100) if total_structures > 0 else 0

region_counts = filtered_df['Région'].value_counts()
region_max = region_counts.index[0] if len(region_counts) > 0 else "N/A"
structures_max = region_counts.iloc[0] if len(region_counts) > 0 else 0

moy_districts_region = districts_sanitaires / regions_couvertes if regions_couvertes > 0 else 0

kpi5.metric("Type Dominant", f"{type_dominant} ({pourcentage_dominant:.1f}%)")
kpi6.metric("Région avec le + de Structures", f"{region_max} ({structures_max})")
kpi7.metric("Moy. Districts/Région", f"{moy_districts_region:.1f}")
kpi8.metric("Taux de Couverture", f"{(regions_couvertes/14)*100:.1f}%" if regions_couvertes > 0 else "0%")

# --- NAVIGATION PRINCIPALE PAR ONGLETS ---
tab_overview, tab_conventions, tab_stats, tab_geo, tab_deepdive, tab_density, tab_comparative = st.tabs([
    "📊 Vue d'Ensemble", 

    "✍️ Suivi des Conventions",
    "📈 Analyses Statistiques Avancées",
    "🌍 Distribution Géographique", 

    "🔬 Analyse Approfondie & Données",
    "🗺️ Distribution & Densité", 
    "🔍 Analyse Comparative & Types",

    
])

# == ONGELET 1: VUE D'ENSEMBLE ===============================================
with tab_overview:
    st.header("Aperçu Global de la Répartition")
    col1, col2 = st.columns((2, 3))
    
    with col1:
        st.subheader("Répartition par Type de Structure")
        type_counts = filtered_df['Type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Nombre']
        fig_pie = px.pie(
            type_counts, names='Type', values='Nombre', hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title="Proportion des Types de Structures"
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Vue Hiérarchique : Région > District")
        fig_treemap = px.treemap(
            filtered_df, path=[px.Constant("Sénégal"), 'Région', 'District Sanitaire'],
            color='Région', color_discrete_sequence=px.colors.qualitative.Alphabet,
            title="Explorez la hiérarchie des structures"
        )
        fig_treemap.update_layout(margin = dict(t=50, l=25, r=25, b=25))
        st.plotly_chart(fig_treemap, use_container_width=True)

# == ONGELET 2: DISTRIBUTION & DENSITÉ ========================================
with tab_density:
    st.header("Analyse de la Distribution et de la Densité Géographique")

    st.subheader("Analyse de la Densité par Région")
    # Préparation des données pour le graphique à bulles
    region_agg = filtered_df.groupby('Région').agg(
        Nb_Structures=('NOM DES STRUCTURES SANITAIRES CIBLES', 'count'),
        Nb_Districts=('District Sanitaire', 'nunique')
    ).reset_index()
    region_agg['Structures_par_District'] = (region_agg['Nb_Structures'] / region_agg['Nb_Districts']).round(2)

    fig_bubble = px.scatter(
        region_agg,
        x="Nb_Districts",
        y="Nb_Structures",
        size="Structures_par_District",
        color="Région",
        hover_name="Région",
        size_max=60,
        title="Densité des Structures : Nb Structures vs. Nb Districts par Région"
    )
    fig_bubble.update_layout(
        xaxis_title="Nombre de Districts Sanitaires",
        yaxis_title="Nombre Total de Structures",
        legend_title="Régions"
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribution des Structures par District")
        district_analysis = filtered_df.groupby(['Région', 'District Sanitaire']).size().reset_index(name='Nb_Structures')
        fig_violin = px.violin(
            district_analysis, x='Région', y='Nb_Structures',
            title='Dispersion et Densité du Nb de Structures par District',
            color='Région', box=True, points="all"
        )
        fig_violin.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_violin, use_container_width=True)

    with col2:
        st.subheader("Classement des Districts")
        district_counts = filtered_df['District Sanitaire'].value_counts().reset_index()
        district_counts.columns = ['District', 'Nb_Structures']
        
        st.success("🏆 Top 5 des Districts les Mieux Dotés")
        st.dataframe(district_counts.head(5), use_container_width=True, hide_index=True)
        
        st.warning("📉 Top 5 des Districts les Moins Dotés")
        st.dataframe(district_counts.tail(5), use_container_width=True, hide_index=True)


# == ONGELET 3: ANALYSE COMPARATIVE & TYPES =================================
with tab_comparative:
    st.header("Analyse Comparative et Focus sur les Types de Structures")

    st.subheader("Composition des Structures par Région")
    region_type_counts = filtered_df.groupby(['Région', 'Type']).size().reset_index(name='Nombre')
    fig_stacked_bar = px.bar(
        region_type_counts,
        x='Région',
        y='Nombre',
        color='Type',
        title='Mix des Types de Structures par Région',
        labels={'Nombre': 'Nombre de Structures', 'Région': 'Région'},
        barmode='stack',
        text_auto=True
    )
    fig_stacked_bar.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_stacked_bar, use_container_width=True)
    
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Matrice Région vs. Type")
        pivot = pd.crosstab(filtered_df['Région'], filtered_df['Type'])
        fig_heatmap = px.imshow(
            pivot, labels=dict(x="Type de Structure", y="Région", color="Nombre"),
            aspect="auto", text_auto=True, color_continuous_scale='Cividis_r',
            title="Concentration par Type"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col2:
        st.subheader("Focus Hiérarchique sur les Types")
        fig_sunburst = px.sunburst(
            filtered_df,
            path=['Région', 'Type'],
            title='Explorez la Répartition Région -> Type',
            color='Région'
        )
        st.plotly_chart(fig_sunburst, use_container_width=True)

# == ONGELET 2: DISTRIBUTION GÉOGRAPHIQUE ========================================
with tab_geo:
    st.header("Analyse de la Distribution Géographique")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Structures par Région")
        region_counts = filtered_df['Région'].value_counts().reset_index()
        region_counts.columns = ['Région', 'Nombre']
        fig_bar_region = px.bar(
            region_counts.sort_values('Nombre'),
            x='Nombre', y='Région', orientation='h',
            labels={'Région': 'Région', 'Nombre': 'Nombre de Structures'},
            color='Nombre', color_continuous_scale='Viridis',
            height=500, text='Nombre'
        )
        st.plotly_chart(fig_bar_region, use_container_width=True)

    with col2:
        st.subheader("Distribution des Structures par District")
        district_analysis = filtered_df.groupby(['Région', 'District Sanitaire']).size().reset_index(name='Nb_Structures')
        fig_box = px.box(
            district_analysis, x='Région', y='Nb_Structures',
            title='Dispersion du Nombre de Structures par District',
            color='Région', points="all"
        )
        fig_box.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_box, use_container_width=True)

    st.subheader("Analyse des Écarts de Couverture")
    expander_gap = st.expander("Afficher l'analyse des régions sous et sur-représentées (basée sur toutes les données)")
    with expander_gap:
        gap_col1, gap_col2 = st.columns(2)
        region_counts_all = df['Région'].value_counts()
        with gap_col1:
            threshold_low = region_counts_all.quantile(0.25)
            sous_representees = region_counts_all[region_counts_all <= threshold_low].reset_index()
            sous_representees.columns = ['Région', 'Nb_Structures']
            st.warning(f"**Régions à renforcer (≤ {int(threshold_low)} structures)**")
            st.dataframe(sous_representees, use_container_width=True)
        with gap_col2:
            threshold_high = region_counts_all.quantile(0.75)
            performantes = region_counts_all[region_counts_all >= threshold_high].reset_index()
            performantes.columns = ['Région', 'Nb_Structures']
            st.success(f"**Régions les mieux dotées (≥ {int(threshold_high)} structures)**")
            st.dataframe(performantes, use_container_width=True)

# == ONGELET 3: ANALYSE APPROFONDIE & DONNÉES =================================
with tab_deepdive:
    st.header("Analyse Croisée et Exploration des Données")

    st.subheader("Matrice de Corrélation : Région vs. Type de Structure")
    pivot = pd.crosstab(filtered_df['Région'], filtered_df['Type'])
    fig_heatmap = px.imshow(
        pivot, labels=dict(x="Type", y="Région", color="Nombre"),
        aspect="auto", text_auto=True, color_continuous_scale='Blues',
        title="Concentration des Types de Structures par Région"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.subheader("Tableau de Bord Comparatif par Région")
    region_analysis = filtered_df.groupby('Région').agg(
        Nb_Districts=('District Sanitaire', 'nunique'),
        Type_Dominant=('Type', lambda x: x.mode()[0] if not x.mode().empty else 'N/A'),
        Total_Structures=('NOM DES STRUCTURES SANITAIRES CIBLES', 'count')
    ).reset_index()
    region_analysis['Structures_par_District'] = (region_analysis['Total_Structures'] / region_analysis['Nb_Districts']).round(2)
    
    st.markdown("Utilisez ce tableau pour comparer la performance et la composition de chaque région.")
    st.dataframe(
        region_analysis.style.background_gradient(subset=['Total_Structures', 'Structures_par_District'], cmap='Greens'),
        use_container_width=True, hide_index=True
    )

#ONGELET 2: SUIVI DES CONVENTIONS AVEC ANIMATION =======================
with tab_conventions:
    st.header("Suivi Détaillé du Statut des Conventions")
    
    # Calcul des nombres pour l'animation
    statut_counts = filtered_df['Statut Convention'].value_counts()
    nb_signe = statut_counts.get('Signée', 0)
    nb_non_signe = statut_counts.get('Non Signée', 0)

    # Affichage du graphique animé
    st.plotly_chart(create_animated_summary_chart(nb_signe, nb_non_signe), use_container_width=True)
    
    st.markdown("---")
    st.subheader("Explorateur Hiérarchique des Structures")
    regions_in_view = sorted(filtered_df['Région'].unique())
    if not regions_in_view:
        st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
    else:
        for region in regions_in_view:
            with st.expander(f"**Région : {region}**"):
                region_df = filtered_df[filtered_df['Région'] == region]
                districts_in_region = sorted(region_df['District Sanitaire'].unique())
                for district in districts_in_region:
                    st.markdown(f"#### District Sanitaire : {district}")
                    district_df = region_df[region_df['District Sanitaire'] == district]
                    col_signe, col_non_signe = st.columns(2)
                    with col_signe:
                        st.markdown("##### ✅ Structures avec Convention Signée")
                        structures_signees = district_df[district_df['Statut Convention'] == 'Signée']
                        if structures_signees.empty:
                            st.info("Aucune structure avec convention signée.")
                        else:
                            st.dataframe(structures_signees[['NOM DES STRUCTURES SANITAIRES CIBLES']], hide_index=True, use_container_width=True)
                    with col_non_signe:
                        st.markdown("##### ❌ Structures sans Convention Signée")
                        structures_non_signees = district_df[district_df['Statut Convention'] == 'Non Signée']
                        if structures_non_signees.empty:
                            st.success("Toutes les structures ciblées ont signé.")
                        else:
                             st.dataframe(structures_non_signees[['NOM DES STRUCTURES SANITAIRES CIBLES']], hide_index=True, use_container_width=True)
                    st.markdown("---")


# == ONGELET 6: ANALYSES STATISTIQUES AVANCÉES =============================
with tab_stats:
    st.header("📈 Analyses Statistiques Avancées et Indicateurs de Performance")
    st.markdown("Section dédiée aux analyses quantitatives approfondies des conventions et performances régionales.")
    
    # === SECTION 1: STATISTIQUES DESCRIPTIVES ===
    st.subheader("📊 Statistiques Descriptives Globales")
    
    # Préparation des données numériques
    numeric_cols = ['Valeurs', 'Nb Conventions Signées', 'Nb Conventions Non Signées', 
                   'Part Structures Ciblées', 'Part Conventions Signées', 'Part Conventions Non Signées']
    
    # Vérifier que les colonnes existent avant de les utiliser
    numeric_cols = [col for col in numeric_cols if col in filtered_df.columns]
    
    # Calculs seulement si des colonnes numériques sont trouvées
    if numeric_cols:
        stats_col1, stats_col2 = st.columns(2)
        
        with stats_col1:
            st.markdown("**📋 Résumé Statistique des Variables Clés**")
            stats_summary = filtered_df[numeric_cols].describe().round(2)
            st.dataframe(stats_summary, use_container_width=True)
            
            # Calculs d'indicateurs personnalisés
            total_conventions_signees = filtered_df['Nb Conventions Signées'].sum()
            total_conventions_non_signees = filtered_df['Nb Conventions Non Signées'].sum()
            total_conventions = total_conventions_signees + total_conventions_non_signees
            taux_signature_global = (total_conventions_signees / total_conventions * 100) if total_conventions > 0 else 0
            
            st.info(f"""
            **🎯 Indicateurs Clés:**
            - **Taux de signature global:** {taux_signature_global:.1f}%
            - **Total conventions signées:** {int(total_conventions_signees):,}
            - **Total conventions non signées:** {int(total_conventions_non_signees):,}
            - **Valeur totale:** {filtered_df['Valeurs'].sum():,.0f}
            """)
        
        with stats_col2:
            st.markdown("**📈 Distribution des Taux de Signature par Région**")
            region_perf = filtered_df.groupby('Région').agg({
                'Nb Conventions Signées': 'sum',
                'Nb Conventions Non Signées': 'sum'
            }).reset_index()
            region_perf['Taux_Signature'] = (region_perf['Nb Conventions Signées'] / 
                                            (region_perf['Nb Conventions Signées'] + region_perf['Nb Conventions Non Signées']) * 100).fillna(0)
            
            fig_taux = px.bar(
                region_perf.sort_values('Taux_Signature'),
                x='Taux_Signature', y='Région', orientation='h',
                title='Taux de Signature des Conventions par Région (%)',
                labels={'Taux_Signature': 'Taux de Signature (%)', 'Région': 'Région'},
                color='Taux_Signature',
                color_continuous_scale='RdYlGn',
                text='Taux_Signature'
            )
            fig_taux.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            fig_taux.update_layout(height=400)
            st.plotly_chart(fig_taux, use_container_width=True)
        
        st.markdown("---")
        
        # === SECTION 2: ANALYSES DE CORRÉLATION ===
        st.subheader("🔗 Matrice de Corrélation et Relations entre Variables")
        
        corr_col1, corr_col2 = st.columns([2, 1])
        
        with corr_col1:
            # Calcul de la matrice de corrélation
            correlation_matrix = filtered_df[numeric_cols].corr()
            
            fig_corr = px.imshow(
                correlation_matrix,
                labels=dict(color="Corrélation"),
                x=correlation_matrix.columns,
                y=correlation_matrix.columns,
                color_continuous_scale='RdBu_r',
                aspect="auto",
                title="Matrice de Corrélation entre Variables Quantitatives",
                text_auto='.2f'
            )
            fig_corr.update_layout(height=500)
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with corr_col2:
            st.markdown("**🔍 Interprétation des Corrélations:**")
            
            # Identification des corrélations les plus fortes
            corr_pairs = correlation_matrix.unstack().reset_index()
            corr_pairs.columns = ['Var1', 'Var2', 'Corrélation']
            corr_pairs = corr_pairs[corr_pairs['Var1'] != corr_pairs['Var2']]
            corr_pairs['abs_corr'] = corr_pairs['Corrélation'].abs()
            corr_df = corr_pairs.sort_values('abs_corr', ascending=False).drop_duplicates(subset=['abs_corr'])
            
            st.success("**💪 Corrélations Positives Fortes (>0.7):**")
            strong_pos = corr_df[corr_df['Corrélation'] > 0.7].head(3)
            for _, row in strong_pos.iterrows():
                st.write(f"• {row['Var1']} ↔ {row['Var2']}: {row['Corrélation']:.3f}")
            
            st.warning("**⚠️ Corrélations Négatives Fortes (<-0.7):**")
            strong_neg = corr_df[corr_df['Corrélation'] < -0.7].head(3)
            for _, row in strong_neg.iterrows():
                st.write(f"• {row['Var1']} ↔ {row['Var2']}: {row['Corrélation']:.3f}")
        
        st.markdown("---")
        
        # === SECTION 3: ANALYSES DE PERFORMANCE PAR RÉGION ===
        st.subheader("🏆 Tableau de Bord de Performance par Région")
        
        # Calcul des métriques de performance
        performance_df = filtered_df.groupby('Région').agg(
            Valeurs_sum=('Valeurs', 'sum'),
            Nb_Conventions_Signees_sum=('Nb Conventions Signées', 'sum'),
            Nb_Conventions_Non_Signees_sum=('Nb Conventions Non Signées', 'sum'),
            Part_Conventions_Signees_mean=('Part Conventions Signées', 'mean'),
            Nb_Structures_count=('NOM DES STRUCTURES SANITAIRES CIBLES', 'count')
        ).reset_index().round(2)
        
        # Ajout d'indicateurs calculés
        total_conv = performance_df['Nb_Conventions_Signees_sum'] + performance_df['Nb_Conventions_Non_Signees_sum']
        performance_df['Efficacite_Signature'] = (performance_df['Nb_Conventions_Signees_sum'] / total_conv * 100).fillna(0)
        performance_df['Valeur_Moyenne_Structure'] = (performance_df['Valeurs_sum'] / performance_df['Nb_Structures_count']).fillna(0)
        
        # Classement et scoring
        performance_df['Score_Global'] = (
            performance_df['Efficacite_Signature'].rank(pct=True) * 0.4 +
            performance_df['Valeur_Moyenne_Structure'].rank(pct=True) * 0.3 +
            performance_df['Part_Conventions_Signees_mean'].rank(pct=True) * 0.3
        ) * 100
        
        performance_df = performance_df.sort_values('Score_Global', ascending=False)
        
        # Affichage du tableau de performance
        st.markdown("**🎯 Classement des Régions par Score de Performance Global**")
        display_cols = ['Région', 'Efficacite_Signature', 'Valeur_Moyenne_Structure', 
                       'Part_Conventions_Signees_mean', 'Score_Global', 'Nb_Structures_count']
        display_df = performance_df[display_cols].copy()
        display_df.columns = ['Région', 'Efficacité Signature (%)', 'Valeur Moy./Structure', 
                             'Part Moy. Conv. Signées (%)', 'Score Global', 'Nb Structures']
        
        st.dataframe(
            display_df.style.background_gradient(subset=['Score Global'], cmap='RdYlGn')
                            .format({'Efficacité Signature (%)': '{:.1f}%', 
                                    'Valeur Moy./Structure': '{:,.0f}',
                                    'Part Moy. Conv. Signées (%)': '{:.1f}%',
                                    'Score Global': '{:.1f}'}),
            use_container_width=True, hide_index=True
        )
        
        st.markdown("---")
        
        # === SECTION 4: ANALYSES GRAPHIQUES AVANCÉES ===
        st.subheader("📊 Visualisations Statistiques Avancées")
        
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            st.markdown("**📈 Analyse de la Distribution des Valeurs**")
            fig_hist = px.histogram(
                filtered_df, x='Valeurs', nbins=30,
                title='Distribution des Valeurs des Conventions',
                labels={'Valeurs': 'Valeur des Conventions', 'count': 'Fréquence'},
                color_discrete_sequence=['#1f77b4']
            )
            fig_hist.add_vline(x=filtered_df['Valeurs'].mean(), line_dash="dash", 
                              line_color="red", annotation_text=f"Moyenne: {filtered_df['Valeurs'].mean():.0f}")
            fig_hist.add_vline(x=filtered_df['Valeurs'].median(), line_dash="dash", 
                              line_color="green", annotation_text=f"Médiane: {filtered_df['Valeurs'].median():.0f}")
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with viz_col2:
            st.markdown("**🎯 Scatter Plot: Efficacité vs Valeur Moyenne**")
            fig_scatter = px.scatter(
                performance_df, 
                x='Valeur_Moyenne_Structure', 
                y='Efficacite_Signature',
                size='Nb_Structures_count',
                color='Score_Global',
                hover_name='Région',
                title='Performance: Efficacité de Signature vs Valeur Moyenne par Structure',
                labels={'Valeur_Moyenne_Structure': 'Valeur Moyenne par Structure',
                       'Efficacite_Signature': 'Efficacité de Signature (%)'},
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # === SECTION 5: ANALYSES DE VARIANCE ===
        st.subheader("📏 Analyse de la Variance et de la Dispersion")
        
        variance_col1, variance_col2 = st.columns(2)
        
        with variance_col1:
            st.markdown("**📊 Box Plot: Distribution des Parts de Conventions Signées**")
            fig_box_region = px.box(
                filtered_df, x='Région', y='Part Conventions Signées',
                title='Dispersion des Parts de Conventions Signées par Région',
                color='Région'
            )
            fig_box_region.update_layout(showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig_box_region, use_container_width=True)
        
        with variance_col2:
            st.markdown("**📈 Analyse des Coefficients de Variation**")
            cv_analysis = filtered_df.groupby('Région')[numeric_cols].agg(['mean', 'std']).round(3)
            cv_data = []
            
            for region in cv_analysis.index:
                for col in numeric_cols:
                    mean_val = cv_analysis.loc[region, (col, 'mean')]
                    std_val = cv_analysis.loc[region, (col, 'std')]
                    if mean_val is not None and mean_val != 0:
                        cv = (std_val / abs(mean_val)) * 100
                        cv_data.append({'Région': region, 'Variable': col, 'CV (%)': cv})
            
            cv_df = pd.DataFrame(cv_data)
            
            key_vars = ['Part Conventions Signées', 'Valeurs', 'Nb Conventions Signées']
            cv_filtered = cv_df[cv_df['Variable'].isin(key_vars)]
            
            fig_cv = px.bar(
                cv_filtered, x='CV (%)', y='Région', color='Variable',
                title='Coefficients de Variation par Région (Stabilité)',
                orientation='h', barmode='group'
            )
            st.plotly_chart(fig_cv, use_container_width=True)
            
        st.markdown("---")
        st.markdown("**📋 Téléchargements et Rapports**")
        
        dl_col1, dl_col2, dl_col3 = st.columns(3)
        
        

# --- SYNTHÈSE & RECOMMANDATIONS ---
st.header("💡 Synthèse Analytique & Pistes d'Action")
st.markdown("Cette section résume les observations clés issues des données pour guider la stratégie.")

rec_col1, rec_col2, rec_col3 = st.columns(3)

with rec_col1:
    st.success("✅ Points Forts")
    # Logique pour trouver la région la mieux dotée
    region_max = region_agg.loc[region_agg['Nb_Structures'].idxmax()]
    st.markdown(f"""
    - **Bonne couverture globale** avec `{df['Région'].nunique()}` régions représentées.
    - La région de **{region_max['Région']}** se distingue par un grand nombre de structures (`{region_max['Nb_Structures']}`).
    - Forte prédominance des **Postes de Santé**, indiquant une bonne couverture de premier niveau.
    """)

with rec_col2:
    st.warning("⚠️ Points de Vigilance")
    # Logique pour trouver la région avec la plus faible densité
    region_min_density = region_agg.loc[region_agg['Structures_par_District'].idxmin()]
    st.markdown(f"""
    - **Disparités importantes** entre les régions en termes de densité de structures.
    - La région de **{region_min_density['Région']}** présente la plus faible densité de structures par district (`{region_min_density['Structures_par_District']}`).
    - Risque de **sous-représentation des Hôpitaux** et Centres de Santé dans certaines zones, impactant l'accès aux soins spécialisés.
    """)

with rec_col3:
    st.info("🎯 Pistes d'Action")
    st.markdown(f"""
    - **Analyser les besoins** des districts les moins dotés (voir classement) pour des investissements ciblés.
    - **Renforcer les régions à faible densité** comme **{region_min_density['Région']}** en visant un équilibre entre types de structures.
    - **Promouvoir des conventions** avec des Hôpitaux et Centres de Santé pour diversifier l'offre de soins.
    """)


# --- EXPLORATION DES DONNÉES BRUTES ---
with st.expander("📋 Explorer, rechercher et télécharger les données détaillées"):
    search_term = st.text_input("Rechercher dans les données...", key="search")

    if search_term:
        search_df = filtered_df[
            filtered_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)
        ]
    else:
        search_df = filtered_df

    st.dataframe(
        search_df[['Région', 'District Sanitaire', 'NOMBRE DE DISTRICTS SANITAIRES VISITES','NOM DES STRUCTURES SANITAIRES CIBLES', 'Valeurs',	'Nb Conventions Signées',
                   	'Nb Conventions Non Signées',	'Part Structures Ciblées',	'Part Conventions Signées',	'Part Conventions Non Signées', 'Type', 'Statut Convention']],
        height=400, hide_index=True, use_container_width=True
    )

    st.download_button(
        label="💾 Télécharger les données affichées",
        data=search_df.to_csv(index=False, sep=';').encode('utf-8'),
        file_name='donnees_filtrees.csv', mime='text/csv'
    )


# # --- STYLE CSS PERSONNALISÉ ---
# st.markdown("""
# <style>
#     h1 { color: #0a2a66; border-bottom: 3px solid #0a2a66; padding-bottom: 10px; }
#     h2, h3 { color: #1e3a8a; }
#     [data-testid="stMetric"] { background-color: #f0f9ff; border-left: 5px solid #2563eb; border-radius: 8px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
#     [data-baseweb="tab"] { background-color: #eef2ff !important; border-radius: 8px 8px 0 0 !important; }
#     [data-baseweb="tab"][aria-selected="true"] { background-color: #dbeafe !important; font-weight: bold; }
#     .st-expander { border: 1px solid #e2e8f0; border-radius: 8px; }
# </style>
# """, unsafe_allow_html=True)




# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'><p>Dashboard d'Analyse CSU Sénégal - MSAS</p><p><small>Version 4.4 - Propulsé par Streamlit avec style</small></p></div>", unsafe_allow_html=True)