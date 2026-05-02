# 👁️ Sentinel v2

### Plataforma de Análisis Cuantitativo y Sentimiento

**Sentinel v2** es una aplicación web interactiva diseñada para el análisis financiero que transforma el flujo de noticias de un activo en una visualización de red intuitiva. Permite a los usuarios identificar rápidamente el "pulso del mercado", detectar clústeres de sentimiento y correlacionar las noticias con el rendimiento del precio del activo.

 <!-- Reemplaza con una captura de pantalla real de tu app -->

---

## 🚀 Características Principales

-   **Visualización de Red Interactiva**: Genera un grafo de noticias donde cada nodo es un artículo y se conecta a un nodo central (el ticker), utilizando un motor de físicas (`forceAtlas2Based`) para agrupar nodos de manera orgánica.

-   **Doble Motor de Análisis de Sentimiento**:
    -   **Motor Normal**: Un analizador rápido basado en palabras clave para una visión general inmediata.
    -   **Oráculo IA (FinBERT)**: Un motor avanzado que utiliza el modelo `ProsusAI/finbert` para un análisis de sentimiento financiero de alta precisión, especializado en el dominio de las finanzas.

-   **Confianza del Oráculo**: Cuando se utiliza el motor de IA, la aplicación muestra las puntuaciones de confianza (positiva, negativa, neutral) del modelo para cada noticia, ofreciendo una capa adicional de transparencia analítica.

-   **Contexto de Mercado en Tiempo Real**: Al seleccionar una noticia, se muestra un gráfico del rendimiento del precio del activo en el último mes, permitiendo una correlación visual instantánea entre la noticia y la acción del precio.

-   **Panel de Detalles Dinámico**: Un panel lateral muestra el título completo, el resumen, la fecha de publicación, el sentimiento y un enlace directo al artículo original.

-   **Exportación de Reportes**: Permite descargar un informe completo en formato `.txt` con todos los datos extraídos y analizados para una auditoría o registro personal.

---

## 🛠️ Construido Con

-   Streamlit - Para la creación de la interfaz web.
-   Streamlit-Agraph - Para la visualización de grafos interactivos.
-   Hugging Face Transformers - Para la ejecución del modelo FinBERT.
-   PyTorch - Como backend para el modelo de IA.
-   yfinance - Para la obtención de datos históricos de precios.

---

## 🏁 Cómo Empezar

Sigue estos pasos para ejecutar una instancia local de Sentinel v2.

### Prerrequisitos

-   Python 3.8+
-   pip

### Instalación

1.  Clona el repositorio en tu máquina local:
    ```sh
    git clone https://github.com/tu-usuario/sentinel-v2.git
    ```

2.  Navega al directorio del proyecto:
    ```sh
    cd sentinel-v2
    ```

3.  Instala las dependencias necesarias:
    ```sh
    pip install -r requirements.txt
    ```

### Ejecución

1.  Ejecuta la aplicación desde la terminal:
    ```sh
    streamlit run dashboard.py
    ```

2.  Abre tu navegador y ve a `http://localhost:8501`.

> **Nota:** La primera vez que actives el "Oráculo IA", la aplicación descargará los pesos del modelo FinBERT (aproximadamente 420MB). Este proceso solo ocurre una vez y puede tardar unos minutos dependiendo de tu conexión a internet.

---

## 📖 Uso

1.  **Ingresa un Ticker**: Escribe el símbolo de la acción que deseas analizar (ej. `TSLA`, `AAPL`, `GOOGL`).
2.  **Ajusta los Parámetros**: Selecciona el número de noticias que quieres procesar.
3.  **Elige tu Motor**: (Opcional) Activa el interruptor "🧠 Activar Oráculo IA" para un análisis más profundo.
4.  **Genera la Red**: Haz clic en el botón "Escanear y Generar Red de Noticias".
5.  **Explora**:
    -   Observa cómo se forman los clústeres de noticias por color (sentimiento).
    -   Haz clic en cualquier esfera de noticia para ver sus detalles en el panel lateral, junto con el gráfico de precios.
    -   Arrastra los nodos para explorar las conexiones.

---

## 📄 Licencia

Distribuido bajo la Licencia MIT. Consulta `LICENSE.txt` para más información.

---

## 📧 Contacto

Tu Nombre - @TuTwitter - tu-email@ejemplo.com

Enlace del Proyecto: https://github.com/tu-usuario/sentinel-v2
