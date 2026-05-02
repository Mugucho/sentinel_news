import streamlit as st
from src.visualization import (
    render_news_network_graph,
    get_price_history,
    create_sidebar_sparkline,
)
from src.macro_calendar import render_macro_timeline  # <-- Nueva importación


def render_news_viz_tab():
    # --- NUEVO: RADAR DE HORARIOS MACRO EN LA BARRA LATERAL ---
    with st.sidebar:
        st.header("⏱️ Radar Macro")
        render_macro_timeline()
        st.divider()
    # ----------------------------------------------------------

    st.header("🕸️ Visualizador de Noticias en Red")
    st.markdown(
        "Identifica rápidamente el pulso del mercado (Clústers de Co-ocurrencia)."
    )

    # Modificamos las columnas para acomodar el Switch de IA
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        ticker = st.text_input("Ingresa el Ticker", value="TSLA").upper()
    with col2:
        num_news = st.slider("Número de noticias", 5, 30, 20)
    with col3:
        st.write("")  # Espaciado
        st.write("")  # Espaciado
        # MAGIA: El interruptor para cambiar de cerebro
        usar_ml = st.toggle("🧠 Activar Oráculo IA (FinBERT)", value=False)
        motor_actual = "ML" if usar_ml else "Normal"

    # Botón y Session State
    if st.button("Escanear y Generar Red de Noticias", type="primary"):
        st.session_state["run_news_scan"] = True
        st.session_state["current_ticker"] = ticker
        st.session_state["current_num_news"] = num_news
        st.session_state["current_engine"] = (
            motor_actual  # Guardamos qué motor elegiste
        )
        st.session_state["selected_node_id"] = None

    # Lógica de renderizado
    if st.session_state.get("run_news_scan", False):
        t = st.session_state["current_ticker"]
        n = st.session_state["current_num_news"]
        e = st.session_state.get("current_engine", "Normal")

        # Le pasamos el motor elegido a nuestra función render
        reporte_texto, news_list, selected_node_id = render_news_network_graph(t, n, e)

        # --- LÓGICA DEL PANEL LATERAL ---
        if selected_node_id:
            st.session_state["selected_node_id"] = selected_node_id

        current_selection = st.session_state.get("selected_node_id", None)

        if current_selection and current_selection != t:
            selected_news = next(
                (news for news in news_list if news["id"] == current_selection), None
            )

            if selected_news:
                with st.sidebar:
                    st.success("Noticia Seleccionada")

                    # --- NUEVO: GRÁFICO DE PRECIOS (Estilo Apple Stocks) ---
                    price_data = get_price_history(t)
                    if price_data is not None:
                        spark_fig, p_color, current_p, delta_p, pct_p = (
                            create_sidebar_sparkline(price_data)
                        )

                        if spark_fig:
                            st.write(f"**Rendimiento de {t} (Último Mes)**")

                            # Imprimimos el precio y el delta con el color correspondiente (Verde o Rojo)
                            st.markdown(
                                f"<h2 style='margin:0; padding:0;'>${current_p:,.2f}</h2>",
                                unsafe_allow_html=True,
                            )
                            st.markdown(
                                f"<p style='color:{p_color}; margin:0; padding:0; font-weight:bold;'>{delta_p:+.2f} ({pct_p:+.2f}%)</p>",
                                unsafe_allow_html=True,
                            )

                            # Inyectamos el gráfico Plotly
                            st.plotly_chart(
                                spark_fig,
                                use_container_width=True,
                                config={"displayModeBar": False},
                            )
                            st.divider()
                    # --- FIN DEL GRÁFICO ---

                    st.subheader(f"{selected_news['full_title']}")
                    st.divider()
                    st.write(f"**Resumen:**\n{selected_news['summary']}")
                    st.divider()

                    sent = (
                        "Positivo 🟢 (Cyan)"
                        if selected_news["sentiment_color"] == "#00d2ff"
                        else (
                            "Negativo 🔴 (Magenta)"
                            if selected_news["sentiment_color"] == "#ff007f"
                            else "Neutral 🟡 (Púrpura)"
                        )
                    )
                    st.caption(f"**Impacto Estimado:** {sent}")

                    # Mostramos la confianza del Oráculo si se usó el motor de ML
                    if e == "ML" and "sentiment_details" in selected_news:
                        scores = selected_news["sentiment_details"].get("scores")
                        if scores:
                            st.divider()
                            st.write("**Confianza del Oráculo:**")
                            st.progress(
                                scores["positive"],
                                text=f"🟢 Positivo ({scores['positive']:.1%})",
                            )
                            st.progress(
                                scores["negative"],
                                text=f"🔴 Negativo ({scores['negative']:.1%})",
                            )
                            st.progress(
                                scores["neutral"],
                                text=f"🟡 Neutral ({scores['neutral']:.1%})",
                            )
                            st.divider()

                    st.markdown(
                        f"**[🔗 LEER ARTÍCULO COMPLETO AQUÍ]({selected_news['url']})**"
                    )

        st.divider()
        st.download_button(
            label=f"📥 Descargar Reporte de {t} ({e} Engine) (.txt)",
            data=reporte_texto,
            file_name=f"Sentinel_Audit_{t}_{e}.txt",
            mime="text/plain",
            help="Descarga el texto en crudo para verificar qué datos extrajo Sentinel.",
        )
