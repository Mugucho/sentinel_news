import streamlit as st
import pandas as pd
from datetime import datetime


@st.cache_data(ttl=3600)  # Se actualiza cada hora
def get_daily_macro_agenda():
    """
    Genera la agenda macroeconómica y geopolítica del día.
    En la Nivel 3 de la plataforma, aquí se conectaría el endpoint de Finnhub o AlphaVantage.
    """
    hoy = datetime.now().strftime("%d %b %Y")

    # Estructura del Radar de Eventos Críticos
    agenda = [
        {
            "hora": "08:30 AM",
            "evento": "Peticiones de Subsidio por Desempleo",
            "impacto": "Alto",
            "icono": "📉",
            "color": "#f39c12",
        },
        {
            "hora": "10:30 AM",
            "evento": "Inventarios de Petróleo Crudo",
            "impacto": "Alto",
            "icono": "🛢️",
            "color": "#f39c12",
        },
        {
            "hora": "02:00 PM",
            "evento": "Decisión de Tasas de Interés (FED)",
            "impacto": "Extremo",
            "icono": "🏦",
            "color": "#e74c3c",
        },
        {
            "hora": "02:30 PM",
            "evento": "Rueda de Prensa de J. Powell",
            "impacto": "Extremo",
            "icono": "🎙️",
            "color": "#e74c3c",
        },
        {
            "hora": "04:00 PM",
            "evento": "Resultados Earnings (GOOGL, AMZN, META)",
            "impacto": "Alto",
            "icono": "📊",
            "color": "#3498db",
        },
    ]

    return hoy, agenda


def render_macro_timeline():
    """
    Renderiza una línea de tiempo visual y elegante para la barra lateral.
    """
    hoy, agenda = get_daily_macro_agenda()

    st.markdown(
        f"<p style='color:#b0c4de; font-size: 14px; margin-bottom: 5px;'>📅 Agenda para hoy: {hoy}</p>",
        unsafe_allow_html=True,
    )

    for item in agenda:
        st.markdown(
            f"""
        <div style="border-left: 3px solid {item['color']}; padding-left: 10px; margin-bottom: 12px;">
            <p style="margin: 0; font-size: 12px; color: #bdc3c7;"><b>{item['hora']}</b> | Riesgo: {item['impacto']}</p>
            <p style="margin: 0; font-size: 14px;">{item['icono']} {item['evento']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
