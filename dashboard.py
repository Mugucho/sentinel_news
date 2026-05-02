import os
import streamlit as st
import logging

# --- 1. INYECTAR LA LLAVE ANTES DE IMPORTAR CUALQUIER OTRA COSA ---
if "HF_TOKEN" in st.secrets:
    os.environ["HF_TOKEN"] = st.secrets["HF_TOKEN"]

# --- 2. AHORA SÍ, IMPORTAR LOS MÓDULOS QUE USAN LA IA ---
from views.tab_news_viz import render_news_viz_tab

# from views.tab_watchlist import render_watchlist_tab (Si tienes esta pestaña)

# --- 3. CONFIGURACIÓN DE PÁGINA ---
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
