import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import urllib.request
import xml.etree.ElementTree as ET
import ssl
import random
import re
import torch
import yfinance as yf
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification


@st.cache_resource
def get_finbert_model():
    """Carga el modelo y tokenizador de FinBERT una sola vez."""
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    return tokenizer, model


def analyze_finbert_sentiment(text):
    """Analizador de sentimiento usando el modelo FinBERT."""
    tokenizer, model = get_finbert_model()
    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=512, padding=True
    )
    outputs = model(**inputs)
    prediction = torch.nn.functional.softmax(outputs.logits, dim=-1)

    positive_score = prediction[0][0].item()
    negative_score = prediction[0][1].item()
    neutral_score = prediction[0][2].item()

    scores = {
        "positive": positive_score,
        "negative": negative_score,
        "neutral": neutral_score,
    }

    if positive_score > negative_score and positive_score > neutral_score:
        return {
            "sentiment": "Positiva",
            "color": "#00d2ff",  # Cyan Neón
            "importance": 25 + (positive_score * 20),
            "scores": scores,
        }
    elif negative_score > positive_score and negative_score > neutral_score:
        return {
            "sentiment": "Negativa",
            "color": "#ff007f",  # Magenta Neón
            "importance": 25 + (negative_score * 20),
            "scores": scores,
        }
    else:
        return {
            "sentiment": "Neutral",
            "color": "#8a2be2",  # Púrpura
            "importance": 10 + (neutral_score * 15),
            "scores": scores,
        }


def analyze_basic_sentiment(text):
    """Analizador de sentimiento con paleta Neón (Estilo Neural Network)."""
    if not text:
        return {
            "sentiment": "Neutral",
            "color": "#8a2be2",  # Púrpura
            "importance": random.uniform(15, 30),
            "scores": None,
        }

    text = text.lower()
    bullish_words = [
        "surge",
        "jump",
        "rise",
        "beat",
        "growth",
        "upgrade",
        "profit",
        "high",
        "buy",
        "soar",
        "record",
        "gain",
    ]
    bearish_words = [
        "fall",
        "drop",
        "miss",
        "decline",
        "downgrade",
        "loss",
        "low",
        "sell",
        "lawsuit",
        "risk",
        "crash",
        "plunge",
        "cut",
    ]

    bull_score = sum(1 for word in bullish_words if word in text)
    bear_score = sum(1 for word in bearish_words if word in text)

    # Colores Neón Vibrantes para fondos oscuros
    if bull_score > bear_score:
        return {
            "sentiment": "Positiva",
            "color": "#00d2ff",  # Cyan Neón
            "importance": random.uniform(20, 45),
            "scores": None,
        }
    elif bear_score > bull_score:
        return {
            "sentiment": "Negativa",
            "color": "#ff007f",  # Magenta Neón
            "importance": random.uniform(20, 45),
            "scores": None,
        }
    else:
        return {
            "sentiment": "Neutral",
            "color": "#8a2be2",  # Púrpura
            "importance": random.uniform(10, 25),
            "scores": None,
        }


def clean_html(raw_html):
    """Limpia etiquetas HTML de los resúmenes RSS"""
    if not raw_html:
        return "Resumen no disponible. Haz clic en el enlace para leer más."
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


@st.cache_data(ttl=3600)  # Cache por una hora
def get_price_history(ticker, period="1mo"):
    """
    Obtiene los datos históricos de precios usando yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        if hist.empty:
            return None
        # Devolvemos solo el precio de cierre para el gráfico
        return hist[["Close"]]
    except Exception:
        return None


# IMPORTANTE: Usamos el caché de Streamlit para no volver a descargar
# las noticias cada vez que haces clic en una esfera.
@st.cache_data(ttl=600)
def fetch_rss_news(ticker, num_news, engine="Normal"):
    """Conexión directa al RSS Feed de Yahoo Finance con Caché."""
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    real_news = []

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req, context=ctx)
        xml_data = response.read()

        root = ET.fromstring(xml_data)
        items = root.findall("./channel/item")

        for i, item in enumerate(items[:num_news]):
            title_node = item.find("title")
            link_node = item.find("link")
            desc_node = item.find("description")
            pub_date_node = item.find("pubDate")

            title = title_node.text if title_node is not None else "Noticia Financiera"
            url_link = link_node.text if link_node is not None else "#"
            summary = (
                clean_html(desc_node.text)
                if desc_node is not None
                else "Haz clic en el enlace para leer el artículo."
            )
            pub_date = pub_date_node.text if pub_date_node is not None else ""

            text_to_analyze = title + " " + summary

            if engine == "ML":
                with st.spinner(f"El Oráculo IA está analizando la noticia {i+1}..."):
                    sentiment_data = analyze_finbert_sentiment(
                        text_to_analyze
                    )
            else:
                sentiment_data = analyze_basic_sentiment(text_to_analyze)

            # Títulos muy cortos para no ensuciar la red densa
            words = title.split()
            display_title = " ".join(words[:3]) + "..." if len(words) > 3 else title

            real_news.append(
                {
                    "id": f"news_{i}",
                    "display_title": display_title,
                    "full_title": title,
                    "summary": f"[{pub_date}] {summary}",
                    "url": url_link,
                    "sentiment_color": sentiment_data["color"],
                    "importance": sentiment_data["importance"],
                    "sentiment_details": sentiment_data,  # Guardamos todos los detalles
                }
            )

    except Exception as e:
        st.sidebar.error(f"Error extrayendo datos crudos: {e}")

    if not real_news:
        real_news.append(
            {
                "id": "news_error",
                "display_title": "Sin novedades",
                "full_title": f"No hay noticias de última hora para {ticker}",
                "summary": "El feed no tiene datos recientes.",
                "url": "#",
                "sentiment_color": "#8a2be2",
                "importance": 20,
                "sentiment_details": {"sentiment": "Neutral", "scores": None},
            }
        )

    return real_news


def render_news_network_graph(ticker, num_news=30, engine="Normal"):
    """
    Renderiza el gráfico con interconexión de red densa y motor ForceAtlas2.
    Usa la memoria de sesión para evitar que el gráfico se reinicie al hacer clic.
    """
    news_list = fetch_rss_news(ticker, num_news, engine)

    # Creamos un identificador único para saber si estamos buscando un ticker nuevo
    graph_id = f"{ticker}_{num_news}"

    # --- MAGIA ANTIRREINICIO: Solo calculamos el grafo si es una búsqueda nueva ---
    if st.session_state.get("current_graph_id") != graph_id:

        # 1. CREAR NODOS
        nodes = []
        nodes.append(
            Node(
                id=ticker,
                label=ticker,
                size=25,
                color="#ffffff",
                font={
                    "color": "white",
                    "size": 20,
                    "strokeWidth": 1,
                    "strokeColor": "#000",
                },
            )
        )

        for news in news_list:
            node_size = news["importance"] * 0.4
            nodes.append(
                Node(
                    id=news["id"],
                    label=news["display_title"],
                    size=node_size,
                    color=news["sentiment_color"],
                    font={"color": "#b0c4de", "size": 10},
                    title=f"<b>{news['full_title']}</b><br><br><i>Haz clic para detalles</i>",
                )
            )

        # 2. CREAR ARISTAS (LA TELARAÑA)
        edges = []
        for news in news_list:
            edges.append(
                Edge(source=news["id"], target=ticker, color="#2c3e50", width=0.5)
            )

        for i, news1 in enumerate(news_list):
            for j, news2 in enumerate(news_list):
                if i < j:
                    if news1["sentiment_color"] == news2["sentiment_color"]:
                        if random.random() > 0.6:
                            edges.append(
                                Edge(
                                    source=news1["id"],
                                    target=news2["id"],
                                    color=news1["sentiment_color"],
                                    width=1.2,
                                )
                            )

        # 3. CONFIGURAR FÍSICAS (Optimizado para iPad y Pantallas Responsivas)
        config = Config(
            width="100%",  # <-- MAGIA 1: Ancho fluido que se adapta a cualquier rotación del iPad
            height=650,  # <-- Altura reducida para permitir ver el botón de descarga sin tanto scroll
            directed=False,
            physics=True,
            solver="forceAtlas2Based",
            forceAtlas2Based={
                "gravitationalConstant": -40,  # MAGIA 2: Repulsión menor para que los clústers no se escapen de la pantalla
                "centralGravity": 0.008,  # Gravedad ligeramente mayor para mantenerlos en el centro de tu visión
                "springLength": 80,  # Conectores un poco más cortos para compactar la red
                "springConstant": 0.002,
                "damping": 0.01,
                "avoidOverlap": 0.8,
            },
            # Mantenemos la estabilización apagada para que siga flotando
            stabilization={"enabled": False},
            layout={"randomSeed": 42},
            interaction={
                "hover": True,
                "tooltipDelay": 100,
                "zoomView": True,
                "dragNodes": True,
            },
        )

        # Guardamos los objetos creados en la memoria para que sobrevivan a los clics
        st.session_state["graph_nodes"] = nodes
        st.session_state["graph_edges"] = edges
        st.session_state["graph_config"] = config
        st.session_state["current_graph_id"] = graph_id

    # --- RENDERIZADO ESTABLE ---
    # Le pasamos a agraph los objetos desde la memoria, no objetos nuevos.
    selected_node_id = agraph(
        nodes=st.session_state["graph_nodes"],
        edges=st.session_state["graph_edges"],
        config=st.session_state["graph_config"],
    )

    # 4. CONSTRUCCIÓN DEL REPORTE DE TEXTO
    log_text = f"=== SENTINEL V2: LOG DE NOTICIAS PARA {ticker} ===\n"
    log_text += f"Total de noticias procesadas: {len(news_list)}\n"
    log_text += f"Motor de Análisis: {engine}\n"
    log_text += "=" * 50 + "\n\n"

    for i, news in enumerate(news_list, 1):
        details = news["sentiment_details"]
        sentiment_label = details["sentiment"]

        if sentiment_label == "Positiva":
            sentimiento_txt = "Positivo (Alcista)"
        elif sentiment_label == "Negativa":
            sentimiento_txt = "Negativo (Bajista)"
        else:
            sentimiento_txt = "Neutral"

        log_text += f"NOTICIA #{i}\n"
        log_text += f"TÍTULO: {news['full_title']}\n"
        log_text += f"RESUMEN: {news['summary']}\n"
        log_text += (
            f"SENTIMIENTO: {sentimiento_txt} | IMPORTANCIA: {news['importance']:.2f}\n"
        )
        if engine == "ML" and details.get("scores"):
            scores = details["scores"]
            log_text += f"CONFIANZA IA: Positivo={scores['positive']:.2%}, Negativo={scores['negative']:.2%}, Neutral={scores['neutral']:.2%}\n"

        log_text += f"URL: {news['url']}\n"
        log_text += "-" * 50 + "\n\n"

    return log_text, news_list, selected_node_id
