import streamlit as st
from views.tab_news_viz import render_news_viz_tab

# Configuración global de la página
st.set_page_config(
    page_title="Sentinel News - Financial Alchemist", page_icon="👁️", layout="wide"
)

st.title("👁️ Sentinel News")
st.markdown("### Plataforma de Análisis Cuantitativo y Sentimiento")

# Sistema de Pestañas (Iniciando con tu Ventana Uno)
tabs = st.tabs(["🕸️ Visualizador Red (Pre-Market)"])

with tabs[0]:
    render_news_viz_tab()
