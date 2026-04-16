import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.graph_objects as go
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Storagedata BI - Portal Maestro", page_icon="📊", layout="wide")

# CARGAR MODELOS (Banca y Telcos)
def cargar_modelos():
    modelos = {"banca": None, "telco": None}
    try:
        if os.path.exists('modelo_banca.pkl'):
            with open('modelo_banca.pkl', 'rb') as f:
                modelos["banca"] = pickle.load(f)
        if os.path.exists('modelo_telco.pkl'):
            with open('modelo_telco.pkl', 'rb') as f:
                modelos["telco"] = pickle.load(f)
    except Exception as e:
        st.error(f"Error al cargar modelos: {e}")
    return modelos

modelos = cargar_modelos()

# 2. ESTILO DE ALTO IMPACTO (DEGRADADO AZUL PROFUNDO)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
    }
    h1 { 
        font-size: 3rem !important; font-weight: 800 !important; color: #ffffff !important; 
        text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .stMarkdown p, label, .stNumberInput label, .stSlider label { 
        font-size: 1.1rem !important; color: #ffffff !important; font-weight: 600 !important;
    }
    .result-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px); text-align: center; margin-top: 10px;
    }
    .stButton>button {
        background-color: #ef4444 !important; color: white !important; border-radius: 8px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CONTROL DE ACCESO
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "proyecto_activo" not in st.session_state:
    st.session_state["proyecto_activo"] = None

# --- LOGIN ---
if not st.session_state["autenticado"]:
    st.markdown("<h1>STORAGEDATA BI</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        with st.form("login"):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.form_submit_button("INGRESAR AL SISTEMA"):
                if u == "admin" and p == "123":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")

# --- PORTAL PRINCIPAL ---
else:
    st.markdown("<h1>CENTRAL DE INTELIGENCIA</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📖 NOSOTROS", "📊 PROYECTOS BI", "📞 CONTACTO"])

    with tab2:
        st.markdown("### 📁 Catálogo de Proyectos Estratégicos")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🏦 RIESGO BANCA"): st.session_state["proyecto_activo"] = "banca"
        with c2:
            if st.button("📱 FUGA TELCOS (CHURN)"): st.session_state["proyecto_activo"] = "telco"
        with c3:
            if st.button("📦 INVENTARIO"): st.session_state["proyecto_activo"] = "inventario"
        
        st.markdown("---")

        # --- LÓGICA PROYECTO BANCA ---
        if st.session_state["proyecto_activo"] == "banca":
            st.subheader("🏦 Análisis de Riesgo Crediticio (Machine Learning)")
            if modelos["banca"]:
                col_in1, col_in2 = st.columns(2)
                with col_in1:
                    ing = st.number_input("Ingresos Mensuales", 1000, 20000, 5000)
                    puntos = st.slider("Score Crediticio (Data de Buró)", 300, 850, 650)
                with col_in2:
                    deudas = st.number_input("Número de Deudas Activas", 0, 15, 2)
                    anti = st.number_input("Antigüedad Laboral (Años)", 0, 50, 5)
                
                if st.button("🔍 ANALIZAR CRÉDITO"):
                    # Ajuste de datos para asegurar que el modelo filtre (incluyendo Edad=35)
                    input_data = np.array([[ing, 35, puntos, deudas, anti]])
                    prob = modelos["banca"].predict_proba(input_data)[0][1]
                    
                    r1, r2 = st.columns(2)
                    with r1:
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number", value = prob * 100,
                            title = {'text': "Riesgo de Impago %", 'font': {'color': 'white'}},
                            gauge = {'axis': {'tickcolor': "white"}, 'bar': {'color': "white"},
                                     'steps': [{'range': [0, 30], 'color': "#22c55e"},
                                               {'range': [30, 70], 'color': "#f59e0b"},
                                               {'range': [70, 100], 'color': "#ef4444"}]}))
                        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
                        st.plotly_chart(fig, use_container_width=True)
                    with r2:
                        color_res = "#22c55e" if prob < 0.5 else "#ef4444"
                        st.markdown(f"""<div class="result-card">
                            <h3>Veredicto Final</h3>
                            <h2 style="color:{color_res} !important;">{'APROBADO' if prob < 0.5 else 'RECHAZADO'}</h2>
                            <p>Análisis procesado con tecnología <b>Arbutus</b> para auditoría de datos.</p>
                        </div>""", unsafe_allow_html=True)
            else:
                st.error("Archivo 'modelo_banca.pkl' no detectado.")

        # --- LÓGICA PROYECTO TELCO ---
        elif st.session_state["proyecto_activo"] == "telco":
            st.subheader("📱 Predicción de Fuga de Clientes (Churn)")
            if modelos["telco"]:
                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    meses = st.slider("Meses de Permanencia", 1, 72, 24)
                    factura = st.number_input("Monto de Factura Mensual", 10, 500, 60)
                with col_t2:
                    reclamos = st.number_input("Reclamos Técnicos (Últ. Mes)", 0, 10, 1)
                
                if st.button("🔍 PREDECIR ABANDONO"):
                    prob_fuga = modelos["telco"].predict_proba([[meses, factura, reclamos]])[0][1]
                    st.markdown(f"""<div class="result-card">
                        <h3>Probabilidad de que el cliente se vaya:</h3>
                        <h1 style="color:#f59e0b !important;">{prob_fuga:.2%}</h1>
                        <p>Datos integrados desde <b>Teradata Vantage</b>.</p>
                    </div>""", unsafe_allow_html=True)
            else:
                st.error("Archivo 'modelo_telco.pkl' no detectado. Por favor entrénalo.")

        # --- LÓGICA PROYECTO INVENTARIO ---
        elif st.session_state["proyecto_activo"] == "inventario":
            st.info("Cargando Visualización de Tableau...")
            url = "https://public.tableau.com/views/proyecto_inventario_stda/Dashboard1"
            st.components.v1.html(f'<iframe src="{url}?:showVizHome=no&:embed=true" width="100%" height="600" style="border-radius:15px;"></iframe>', height=600)