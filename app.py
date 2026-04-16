import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Storagedata BI - Portal Maestro", page_icon="📦", layout="wide")

# 2. ESTILO DE ALTO IMPACTO (CSS PERSONALIZADO)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #330000 50%, #000000 100%);
        color: white;
    }
    h1 { font-size: 4rem !important; font-weight: 800 !important; color: #FF0000 !important; text-shadow: 3px 3px 10px #000; text-align: center; }
    h2 { font-size: 2.5rem !important; color: white !important; font-weight: 700; }
    p, li, span { font-size: 1.4rem !important; }

    /* Estilo de Pestañas */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px 12px 0px 0px;
        color: white !important;
        padding: 15px 30px;
        font-size: 1.2rem !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF0000 !important;
        font-weight: bold;
    }

    /* Diseño del Formulario de Login */
    [data-testid="stForm"] {
        background-color: rgba(0, 0, 0, 0.8);
        border: 3px solid #FF0000;
        border-radius: 25px;
        padding: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CONTROL DE ACCESO
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "usuario_nombre" not in st.session_state:
    st.session_state["usuario_nombre"] = ""
if "proyecto_activo" not in st.session_state:
    st.session_state["proyecto_activo"] = None # Controla qué dashboard se muestra

# --- ESCENARIO A: LOGIN ---
if not st.session_state["autenticado"]:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<h1>STORAGEDATA</h1>", unsafe_allow_html=True)
        with st.form("login_master"):
            u = st.text_input("👤 USUARIO")
            p = st.text_input("🔑 CONTRASEÑA", type="password")
            if st.form_submit_button("🚀 INICIAR SESIÓN"):
                if u == "admin" and p == "123":
                    st.session_state["autenticado"] = True
                    st.session_state["usuario_nombre"] = u
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")

# --- ESCENARIO B: PORTAL ---
else:
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>MENÚ</h2>", unsafe_allow_html=True)
        st.success(f"Conectado: {st.session_state['usuario_nombre'].upper()}")
        if st.button("❌ CERRAR SESIÓN", use_container_width=True):
            st.session_state["autenticado"] = False
            st.session_state["proyecto_activo"] = None
            st.rerun()

    st.markdown("<h1>CENTRAL DE INTELIGENCIA</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📖 NOSOTROS", "📊 PROYECTOS BI", "📞 CONTACTO"])

    with tab1:
        st.markdown("## Nuestra Identidad")
        st.write("Bienvenido al centro de mando de Storagedata.")

    with tab2:
        st.markdown("## 📁 Catálogo de Proyectos BI")
        st.write("Seleccione un proyecto para visualizar el análisis:")
        
        # FILA DE BOTONES (Menú de proyectos)
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("📦 INVENTARIO STDA", use_container_width=True):
                st.session_state["proyecto_activo"] = "inventario"
        
        with col_b:
            if st.button("📈 VENTAS (PRÓX.)", use_container_width=True, disabled=True):
                st.session_state["proyecto_activo"] = "ventas"
        
        with col_c:
            if st.button("🚚 LOGÍSTICA (PRÓX.)", use_container_width=True, disabled=True):
                st.session_state["proyecto_activo"] = "logistica"

        st.markdown("---")

        # LÓGICA PARA MOSTRAR EL PROYECTO SELECCIONADO
        if st.session_state["proyecto_activo"] == "inventario":
            url_inv = "https://public.tableau.com/views/proyecto_inventario_stda/Dashboard1"
            
            # Botón para ir directo a Tableau
            st.link_button("🔗 ABRIR EN TABLAEU PUBLIC (PANTALLA COMPLETA)", url_inv)
            
            # El Visor incrustado
            html_code = f"""
                <iframe src="{url_inv}?:showVizHome=no&:embed=true" 
                        width="100%" height="800" frameborder="0" 
                        style="border-radius: 20px; border: 3px solid #FF0000; background-color: white;">
                </iframe>
            """
            st.components.v1.html(html_code, height=850)
        
        elif st.session_state["proyecto_activo"] is None:
            st.info("👈 Por favor, haz clic en un botón superior para cargar un dashboard.")

    with tab3:
        st.markdown("## Soporte")
        st.write("📧 soporte@storagedata.com")