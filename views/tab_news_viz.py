import streamlit as st
from src.visualization import render_news_network_graph


def render_news_viz_tab():
    st.header("🕸️ Visualizador de Noticias en Red")
    st.markdown(
        "Identifica rápidamente el pulso del mercado (Clústers de Co-ocurrencia)."
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        ticker = st.text_input("Ingresa el Ticker", value="TSLA").upper()
    with col2:
        num_news = st.slider("Número de noticias", 5, 30, 20)

    # Botón y Session State
    if st.button("Escanear y Generar Red de Noticias", type="primary"):
        st.session_state["run_news_scan"] = True
        st.session_state["current_ticker"] = ticker
        st.session_state["current_num_news"] = num_news
        # MAGIA 1: Limpiamos la selección anterior si hacemos un nuevo escaneo
        st.session_state["selected_node_id"] = None

    # Lógica de renderizado
    if st.session_state.get("run_news_scan", False):
        t = st.session_state["current_ticker"]
        n = st.session_state["current_num_news"]

        # Recibimos el texto, la lista de noticias y el ID del nodo en el que hiciste clic
        reporte_texto, news_list, selected_node_id = render_news_network_graph(t, n)

        # --- MAGIA 2: PERSISTENCIA DEL CLIC EN MEMORIA ---
        # Si el usuario hace clic, lo guardamos firmemente en la memoria de la sesión
        if selected_node_id:
            st.session_state["selected_node_id"] = selected_node_id

        # Recuperamos el nodo de la memoria (esto sobrevive a la recarga de Streamlit)
        current_selection = st.session_state.get("selected_node_id", None)

        # --- LÓGICA DEL PANEL LATERAL ---
        if current_selection and current_selection != t:
            # Buscamos la noticia exacta usando el ID guardado en memoria
            selected_news = next(
                (news for news in news_list if news["id"] == current_selection), None
            )

            if selected_news:
                # Dibujamos el sidebar de forma forzada
                with st.sidebar:
                    st.success("Noticia Seleccionada")
                    st.subheader(f"{selected_news['full_title']}")
                    st.divider()
                    st.write(f"**Resumen:**\n{selected_news['summary']}")
                    st.divider()

                    # MAGIA 3: Corrección del mapeo a la nueva paleta Neón
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

                    st.markdown(
                        f"**[🔗 LEER ARTÍCULO COMPLETO AQUÍ]({selected_news['url']})**"
                    )

        st.divider()
        st.download_button(
            label=f"📥 Descargar Reporte de {t} (.txt)",
            data=reporte_texto,
            file_name=f"Sentinel_Audit_{t}.txt",
            mime="text/plain",
            help="Descarga el texto en crudo para verificar qué datos extrajo Sentinel.",
        )
