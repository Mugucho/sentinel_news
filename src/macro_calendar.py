import streamlit as st
import requests
from datetime import datetime


@st.cache_data(ttl=3600)  # Actualiza solo cada hora para ahorrar llamadas a la API
def get_daily_macro_agenda():
    """
    Busca la agenda macroeconómica y geopolítica del día usando la API de Finnhub.
    """
    hoy = datetime.now().strftime("%d %b %Y")
    agenda = []

    # Intentamos obtener la clave secreta de forma segura
    api_key = st.secrets.get("FINNHUB_API_KEY", None)

    if api_key and api_key != "pega_tu_clave_aqui":
        try:
            # Endpoint de Finnhub para el calendario económico
            url = f"https://finnhub.io/api/v1/calendar/economic?token={api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                events = data.get("economicCalendar", [])

                # Filtramos solo los eventos de hoy y de Estados Unidos (US)
                hoy_str = datetime.now().strftime("%Y-%m-%d")

                for e in events:
                    if (
                        e.get("time", "").startswith(hoy_str)
                        and e.get("country") == "US"
                    ):

                        impact = e.get("impact", "low").lower()

                        # Alquimia de colores e íconos basada en el impacto del evento
                        if impact == "high":
                            color = "#e74c3c"  # Rojo Neón
                            icono = "🚨"
                            impact_str = "Alto/Extremo"
                        elif impact == "medium":
                            color = "#f39c12"  # Naranja
                            icono = "⚠️"
                            impact_str = "Medio"
                        else:
                            continue  # Ignoramos eventos de bajo impacto para evitar ruido

                        # Extraemos la hora (formato HH:MM)
                        time_str = e.get("time", "").split(" ")[1][:5]

                        agenda.append(
                            {
                                "hora": time_str,
                                "evento": e.get("event", "Evento Económico"),
                                "impacto": impact_str,
                                "icono": icono,
                                "color": color,
                            }
                        )
        except Exception as e:
            st.sidebar.error(f"Error al conectar con Finnhub: {e}")

    # Fallback: Si no encuentra datos o falta la clave, muestra datos estructurales por defecto
    if not agenda:
        agenda = [
            {
                "hora": "00:00",
                "evento": "Configura la Clave API de Finnhub",
                "impacto": "Sistema",
                "icono": "🔧",
                "color": "#7f8c8d",
            },
            {
                "hora": "10:30 AM",
                "evento": "Inventarios de Petróleo (Ejemplo)",
                "impacto": "Alto",
                "icono": "🛢️",
                "color": "#f39c12",
            },
            {
                "hora": "02:00 PM",
                "evento": "Decisión de Tasas (FED) (Ejemplo)",
                "impacto": "Extremo",
                "icono": "🏦",
                "color": "#e74c3c",
            },
        ]

    # Ordenamos la agenda por hora
    agenda = sorted(agenda, key=lambda x: x["hora"])
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
