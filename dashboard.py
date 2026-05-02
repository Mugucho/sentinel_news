import os
import streamlit as st
from views.tab_news_viz import render_news_viz_tab
import logging

# Suprime las advertencias de "acceso a __path__" de la librería transformers
# Coloca esto al principio de tu script principal (ej. dashboard.py)
logging.getLogger("transformers").setLevel(logging.ERROR)


# Configuración global de la página
st.set_page_config(
    page_title="Sentinel News - Financial Alchemist", page_icon="👁️", layout="wide"
)

# Inyectar el token de Hugging Face en el sistema para descargas más rápidas
if "HF_TOKEN" in st.secrets:
    os.environ["HF_TOKEN"] = st.secrets["HF_TOKEN"]

st.title("👁️ Sentinel News")
st.markdown("### Plataforma de Análisis Cuantitativo y Sentimiento")

# Sistema de Pestañas (Iniciando con tu Ventana Uno)
tabs = st.tabs(["🕸️ Visualizador Red (Pre-Market)"])

with tabs[0]:
    render_news_viz_tab()
