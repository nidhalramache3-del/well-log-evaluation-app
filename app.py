"""
تطبيق ويب لتقييم سجلات الآبار وحساب الاحتياطيات الهيدروكربونية
Well Log Evaluation & Hydrocarbon Reserves Calculation Web Application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import lasio
from io import StringIO

# ==================== قواميس الترجمة ====================
TRANSLATIONS = {
    'English': {
        'app_title': 'Well Log Evaluation & Reserves Calculator',
        'app_subtitle': 'Enterprise Petrophysical Analysis Platform',
        'language': 'Language',
        'parameters': 'Petrophysical Parameters',
        'a_param': 'Archie Factor (a)',
        'm_param': 'Cementation Exponent (m)',
        'n_param': 'Saturation Exponent (n)',
        'rw_param': 'Formation Water Resistivity (Rw)',
        'dt_ma_param': 'Matrix Transit Time (Δtma)',
        'rhob_ma_param': 'Matrix Density (ρma)',
        'nphi_ma_param': 'Matrix Neutron Porosity (NPHIma)',
        'tab1': '📤 Data Import',
        'tab2': '🔬 Petrophysics',
        'tab3': '📊 2D Dashboard',
        'tab4': '🔄 3D Model',
        'tab5': '💰 Volumetrics',
        'upload_data': 'Upload Well Log Data',
        'file_types': 'Supported formats: LAS, CSV',
        'data_preview': 'Data Preview',
        'stat_summary': 'Statistical Summary',
        'missing_values': 'Missing Values Treatment',
        'fill_method': 'Select filling method',
        'apply_filling': 'Apply Filling',
        'curves_available': 'Available Curves',
        'vshale_calc': 'Vshale Calculation',
        'spectral_gr': 'Spectral GR Analysis',
        'porosity_calc': 'Porosity Analysis',
        'saturation_calc': 'Saturation Analysis',
        'uranium': 'Uranium (ppm)',
        'thorium': 'Thorium (ppm)',
        'potassium': 'Potassium (%)',
        'vshale': 'Vshale (fraction)',
        'phi_sonic': 'Sonic Porosity',
        'phi_density': 'Density Porosity',
        'sw': 'Water Saturation (Sw)',
        'so': 'Oil Saturation (So)',
        'rxo': 'Flushed Zone Resistivity',
        'rt': 'True Resistivity',
        'track1': 'GR, SP & Caliper',
        'track2': 'Resistivity (Log Scale)',
        'track3': 'Porosity Overlay',
        'track4': 'Saturation Profile',
        'depth': 'Depth (m/ft)',
        '3d_model': '3D Wellbore Geological Model',
        'lithology': 'Lithology Distribution',
        'sand': 'Sandstone (Reservoir)',
        'shale': 'Shale (Seal)',
        'oil': 'Oil Zone',
        'water': 'Water Zone',
        'contour_data': 'Contour Map Data',
        'area': 'Area (acres)',
        'thickness': 'Net Pay Thickness (ft)',
        'calculate_ioip': 'Calculate IOIP',
        'bulk_volume': 'Bulk Volume (acre-ft)',
        'pore_volume': 'Pore Volume (acre-ft)',
        'hc_volume': 'Hydrocarbon Volume (acre-ft)',
        'ioip': 'Initial Oil In Place (STB)',
        'formation_volume': 'Formation Volume Factor (Bo)',
        'curve_mapping': 'Curve Mapping',
        'process_data': 'Process Petrophysics'
    },
    'Français': {
        'app_title': "Évaluation des Diagraphies & Réserves",
        'app_subtitle': "Plateforme d'Analyse Pétrophysique d'Entreprise",
        'language': 'Langue',
        'parameters': 'Paramètres Pétrophysiques',
        'a_param': "Facteur d'Archie (a)",
        'm_param': 'Exposant de Cimentation (m)',
        'n_param': "Exposant de Saturation (n)",
        'rw_param': 'Résistivité de l\'eau (Rw)',
        'dt_ma_param': 'Temps de Transit Matrice (Δtma)',
        'rhob_ma_param': 'Densité Matrice (ρma)',
        'nphi_ma_param': 'Porosité Neutron Matrice (NPHIma)',
        'tab1': '📤 Importation',
        'tab2': '🔬 Pétrophysique',
        'tab3': '📊 Tableau 2D',
        'tab4': '🔄 Modèle 3D',
        'tab5': '💰 Volumétrie',
        'upload_data': 'Télécharger les Données',
        'file_types': 'Formats supportés: LAS, CSV',
        'data_preview': 'Aperçu des Données',
        'stat_summary': 'Résumé Statistique',
        'missing_values': 'Traitement des Valeurs Manquantes',
        'fill_method': 'Choisir méthode de remplissage',
        'apply_filling': 'Appliquer le Remplissage',
        'curves_available': 'Courbes Disponibles',
        'vshale_calc': 'Calcul du Vshale',
        'spectral_gr': 'Analyse GR Spectrale',
        'porosity_calc': 'Analyse de Porosité',
        'saturation_calc': 'Analyse de Saturation',
        'uranium': 'Uranium (ppm)',
        'thorium': 'Thorium (ppm)',
        'potassium': 'Potassium (%)',
        'vshale': 'Vshale (fraction)',
        'phi_sonic': 'Porosité Sonique',
        'phi_density': 'Porosité Densité',
        'sw': 'Saturation en Eau (Sw)',
        'so': 'Saturation en Huile (So)',
        'rxo': 'Résistivité Zone Lavée',
        'rt': 'Résistivité Vraie',
        'track1': 'GR, SP & Caliper',
        'track2': 'Résistivité (Échelle Log)',
        'track3': 'Superposition Porosité',
        'track4': 'Profil de Saturation',
        'depth': 'Profondeur (m/ft)',
        '3d_model': 'Modèle Géologique 3D du Puits',
        'lithology': 'Distribution Lithologique',
        'sand': 'Grès (Réservoir)',
        'shale': 'Argile (Couverture)',
        'oil': 'Zone à Huile',
        'water': 'Zone à Eau',
        'contour_data': 'Données de Carte Contour',
        'area': 'Surface (acres)',
        'thickness': 'Épaisseur Nette (ft)',
        'calculate_ioip': 'Calculer IOIP',
        'bulk_volume': 'Volume Brut (acre-ft)',
        'pore_volume': 'Volume Poral (acre-ft)',
        'hc_volume': 'Volume Hydrocarbure (acre-ft)',
        'ioip': 'Huile en Place Initiale (STB)',
        'formation_volume': 'Facteur Volume de Formation (Bo)',
        'curve_mapping': 'Cartographie des Courbes',
        'process_data': 'Traiter la Pétrophysique'
    }
}

# ==================== دوال الحسابات البتروفيزيائية ====================

def calculate_vshale_consolidated(gr, gr_min, gr_max):
    igr = (gr - gr_min) / (gr_max - gr_min)
    vshale = 0.33 * (2**(2*igr) - 1)
    return np.clip(vshale, 0, 1)

def calculate_sonic_porosity(dt, dt_ma, dt_fl=189):
    phi_sonic = (dt - dt_ma) / (dt_fl - dt_ma)
    return np.clip(phi_sonic, 0, 0.4)

def calculate_density_porosity(rhob, rhob_ma, rhob_fl=1.0):
    phi_density = (rhob_ma - rhob) / (rhob_ma - rhob_fl)
    return np.clip(phi_density, 0, 0.4)

def calculate_water_saturation_archie(phi, rt, rw, a, m, n):
    sw = (a * rw / ((phi**m) * rt))**(1/n)
    return np.clip(sw, 0, 1)

# ==================== دوال إنشاء الرسوم البيانية ====================

def create_2d_dashboard(df, depth_col, curves_dict, lang):
    t = TRANSLATIONS[lang]
    fig = make_subplots(rows=1, cols=4, subplot_titles=(t['track1'], t['track2'], t['track3'], t['track4']), shared_yaxes=True, horizontal_spacing=0.05)
    depth = df[depth_col]
    
    # Track 1
    if curves_dict.get('GR') in df.columns:
        fig.add_trace(go.Scatter(x=df[curves_dict['GR']], y=depth, mode='lines', name='GR', line=dict(color='green')), row=1, col=1)
    if curves_dict.get('SP') in df.columns:
        fig.add_trace(go.Scatter(x=df[curves_dict['SP']], y=depth, mode='lines', name='SP', line=dict(color='blue')), row=1, col=1)
    
    # Track 2 (Resistivity)
    if curves_dict.get('RT') in df.columns:
        fig.add_trace(go.Scatter(x=np.log10(df[curves_dict['RT']].replace(0, 0.001)), y=depth, mode='lines', name='Rt', line=dict(color='red')), row=1, col=2)
    if curves_dict.get('RXO') in df.columns:
        fig.add_trace(go.Scatter(x=np.log10(df[curves_dict['RXO']].replace(0, 0.001)), y=depth, mode='lines', name='Rxo', line=dict(color='orange')), row=1, col=2)
        
    # Track 3 (Porosity)
    if curves_dict.get('NPHI') in df.columns:
        fig.add_trace(go.Scatter(x=df[curves_dict['NPHI']], y=depth, mode='lines', name='NPHI', line=dict(color='blue', dash='dash')), row=1, col=3)
    if curves_dict.get('RHOB') in df.columns:
        fig.add_trace(go.Scatter(x=(2.65 - df[curves_dict['RHOB']])/1.65, y=depth, mode='lines', name='RHOB(scaled)', line=dict(color='red')), row=1, col=3)
        
    # Track 4 (Saturation)
    if 'SW' in df.columns:
        fig.add_trace(go.Scatter(x=df['SW'], y=depth, mode='lines', name='Sw', line=dict(color='blue'), fill='tozerox'), row=1, col=4)
        fig.add_trace(go.Scatter(x=df['SO'], y=depth, mode='lines', name='So', line=dict(color='green'), fill='tonextx'), row=1, col=4)

    fig.update_layout(height=800, showlegend=True, title_text="")
    fig.update_xaxes(title_text="", row=1, col=1)
    fig.update_xaxes(title_text="log10(Ohm.m)", row=1, col=2)
    fig.update_xaxes(title_text="Fraction", row=1, col=3, autorange="reversed")
    fig.update_xaxes(title_text="Fraction", row=1, col=4)
    fig.update_yaxes(title_text=t['depth'], row=1, col=1, autorange="reversed")
    return fig

def create_3d_wellbore_model(df, depth_col, lang):
    t = TRANSLATIONS[lang]
    depth = df[depth_col].values
    n_points = len(depth)
    theta = np.linspace(0, 2*np.pi, 20)
    
    fig = go.Figure()
    step = max(1, n_points // 100) # تقليل النقاط لتسريع الرسم 3D
    
    for i in range(0, n_points-step, step):
        z0, z1 = depth[i], depth[i+step]
        vshale = df['VSH'].iloc[i] if 'VSH' in df.columns else 0.5
        so = df['SO'].iloc[i] if 'SO' in df.columns else 0
        sw = df['SW'].iloc[i] if 'SW' in df.columns else 1
        
        if vshale > 0.5:
            color = 'gray'
            name = t['shale']
        elif so > 0.4:
            color = 'green'
            name = t['oil']
        elif sw > 0.6:
            color = 'blue'
            name = t['water']
        else:
            color = 'yellow'
            name = t['sand']
            
        fig.add_trace(go.Mesh3d(
            x=[np.cos(th) for th in theta], y=[np.sin(th) for th in theta], z=[z0] * len(theta),
            i=list(range(len(theta)-1)), j=list(range(1, len(theta))), k=[len(theta)-1] * (len(theta)-1),
            color=color, opacity=0.9, name=name, showlegend=False
        ))

    fig.update_layout(
        title=t['3d_model'],
        scene=dict(zaxis_title=t['depth'], zaxis=dict(autorange="reversed")),
        height=700
    )
    return fig

# ==================== التطبيق الرئيسي ====================

def main():
    st.set_page_config(page_title="Petrophysics App", layout="wide")
    
    # القائمة الجانبية (Sidebar)
    with st.sidebar:
        lang = st.radio("Language / Langue", ['English', 'Français'])
        st.session_state['lang'] = lang
        t = TRANSLATIONS[lang]
        st.title(t['parameters'])
        a_param = st.number_input(t['a_param'], value=0.81, step=0.01) # 0.81 بناء على مشروع KSU
        m_param = st.number_input(t['m_param'], value=2.0, step=0.1)
        n_param = st.number_input(t['n_param'], value=2.0, step=0.1)
        rw_param = st.number_input(t['rw_param'], value=0.018, step=0.001, format="%.3f")
        dt_ma = st.number_input(t['dt_ma_param'], value=55.5, step=0.1)
        rhob_ma = st.number_input(t['rhob_ma_param'], value=2.65, step=0.01)

    st.title(f"🛢️ {t['app_title']}")
    tab1, tab2, tab3, tab4, tab5 = st.tabs([t['tab1'], t['tab2'], t['tab3'], t['tab4'], t['tab5']])
    
    # تهيئة البيانات
    if 'df_raw' not in st.session_state: st.session_state['df_raw'] = None
    if 'df_proc' not in st.session_state: st.session_state['df_proc'] = None
    if 'depth_col' not in st.session_state: st.session_state['depth_col'] = 'DEPT'

    # ========== TAB 1: استيراد البيانات ==========
    with tab1:
        st.header(t['upload_data'])
        uploaded_file = st.file_uploader("", type=['las', 'csv'])
        if uploaded_file:
            if uploaded_file.name.endswith('.las'):
                las = lasio.read(StringIO(uploaded_file.getvalue().decode('utf-8')))
                df = las.df().reset_index()
                st.session_state['depth_col'] = df.columns[0]
            else:
                df = pd.read_csv(uploaded_file)
                st.session_state['depth_col'] = df.columns[0]
                
            st.session_state['df_raw'] = df.fillna(method='ffill')
            st.success("Data loaded successfully!")
            st.dataframe(df.head())

    # ========== TAB 2: البتروفيزياء ==========
    with tab2:
        if st.session_state['df_raw'] is not None:
            st.header(t['curve_mapping'])
            df = st.session_state['df_raw'].copy()
            cols = ['None'] + list(df.columns)
            
            col1, col2, col3 = st.columns(3)
            gr_col = col1.selectbox("Gamma Ray (GR)", cols, index=cols.index('GR') if 'GR' in cols else 0)
            rt_col = col2.selectbox("Deep Resistivity (RT/LLD)", cols, index=cols.index('LLD') if 'LLD' in cols else 0)
            rxo_col = col3.selectbox("Shallow Resistivity (RXO/LLS)", cols, index=cols.index('LLS') if 'LLS' in cols else 0)
            
            dt_col = col1.selectbox("Sonic (DT)", cols, index=cols.index('DT') if 'DT' in cols else 0)
            nphi_col = col2.selectbox("Neutron (NPHI)", cols, index=cols.index('NPHI') if 'NPHI' in cols else 0)
            rhob_col = col3.selectbox("Density (RHOB)", cols, index=cols.index('RHOB') if 'RHOB' in cols else 0)

            if st.button(t['process_data']):
                # الحسابات
                if gr_col != 'None':
                    gr_min, gr_max = df[gr_col].min(), df[gr_col].max()
                    df['VSH'] = calculate_vshale_consolidated(df[gr_col], gr_min, gr_max)
                else:
                    df['VSH'] = 0.0
                    
                if dt_col != 'None':
                    df['PHI'] = calculate_sonic_porosity(df[dt_col], dt_ma)
                elif rhob_col != 'None':
                    df['PHI'] = calculate_density_porosity(df[rhob_col], rhob_ma)
                else:
                    df['PHI'] = 0.15 # قيمة افتراضية

                # معالجة المسامية لتجنب القسمة على صفر
                df['PHI'] = df['PHI'].replace(0, 0.001)

                if rt_col != 'None':
                    df['SW'] = calculate_water_saturation_archie(df['PHI'], df[rt_col], rw_param, a_param, m_param, n_param)
                    df['SO'] = 1 - df['SW']
                
                st.session_state['curves_dict'] = {'GR': gr_col, 'RT': rt_col, 'RXO': rxo_col, 'DT': dt_col, 'NPHI': nphi_col, 'RHOB': rhob_col}
                st.session_state['df_proc'] = df
                st.success("Petrophysical calculations completed!")
                st.dataframe(df[['VSH', 'PHI', 'SW', 'SO']].head())
        else:
            st.warning("Please upload data in Tab 1 first.")

    # ========== TAB 3: 2D Dashboard ==========
    with tab3:
        if st.session_state['df_proc'] is not None:
            fig_2d = create_2d_dashboard(st.session_state['df_proc'], st.session_state['depth_col'], st.session_state['curves_dict'], lang)
            st.plotly_chart(fig_2d, use_container_width=True)
        else:
            st.info("Process data in Tab 2 first.")

    # ========== TAB 4: 3D Model ==========
    with tab4:
        if st.session_state['df_proc'] is not None:
            fig_3d = create_3d_wellbore_model(st.session_state['df_proc'], st.session_state['depth_col'], lang)
            st.plotly_chart(fig_3d, use_container_width=True)
        else:
            st.info("Process data in Tab 2 first.")

    # ========== TAB 5: Volumetrics ==========
    with tab5:
        st.header(t['calculate_ioip'])
        colA, colB = st.columns(2)
        area_input = colA.number_input(t['area'], value=3000.0) # بالـ Acres
        h_input = colB.number_input(t['thickness'], value=100.0) # بالـ ft
        bo_input = colA.number_input(t['formation_volume'], value=1.19) # معامل KSU الافتراضي
        
        if st.session_state['df_proc'] is not None:
            avg_phi = st.session_state['df_proc']['PHI'].mean()
            avg_so = st.session_state['df_proc']['SO'].mean()
            
            st.write(f"Average Porosity: {avg_phi:.3f}")
            st.write(f"Average Oil Saturation: {avg_so:.3f}")
            
            if st.button("Calculate Volumes"):
                vol_acre_ft = area_input * h_input
                ioip = (7758 * vol_acre_ft * avg_phi * avg_so) / bo_input
                
                st.success(f"### {t['ioip']}: {ioip:,.0f} STB")
                st.info(f"**{t['bulk_volume']}**: {vol_acre_ft:,.0f} acre-ft")

if __name__ == "__main__":
    main()
