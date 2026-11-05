import os
import re
import json
from pathlib import Path
from urllib.parse import urlparse, parse_qs, quote
from urllib.request import urlopen

import streamlit as st

from agent.transcript import TranscriptAgent
from agent.document import generate_word_document


# CARPETA DE SALIDA
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# IDENTIFICAR VIDEO
def extract_video_id(url):

    parsed = urlparse(url.strip())
    host = parsed.netloc.lower().split(":")[0]

    if host in ("youtube.com", "www.youtube.com", "m.youtube.com",
                "youtube-nocookie.com", "www.youtube-nocookie.com"):

        video_id = parse_qs(parsed.query).get("v", [None])[0]

        if not video_id:
            match = re.search(
                r"/(?:shorts|embed|live)/([A-Za-z0-9_-]{11})",
                parsed.path
            )
            video_id = match.group(1) if match else None

    elif host in ("youtu.be", "www.youtu.be"):

        video_id = parsed.path.strip("/").split("/")[0]

    else:
        video_id = None

    if not video_id or not re.fullmatch(
        r"[A-Za-z0-9_-]{11}", video_id
    ):
        raise ValueError("La URL de YouTube no es válida.")

    return video_id


# OBTENER TITULO AUTOMATICAMENTE
def get_video_title(video_id):

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    oembed_url = (
        "https://www.youtube.com/oembed?url="
        + quote(video_url, safe="")
        + "&format=json"
    )

    with urlopen(oembed_url, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["title"]


# CONFIGURACION DE LA INTERFAZ
st.set_page_config(
    page_title="YouTube Transcript Agent",
    page_icon="🎬",
    layout="centered"
)


# INTERFAZ
st.title("🎬 YouTube Transcript Agent")

st.write(
    "Pega el enlace de un video de YouTube "
    "para generar su transcripción en Word."
)

st.divider()

url = st.text_input(
    "URL del video de YouTube",
    placeholder="https://www.youtube.com/watch?v=..."
)


if st.button(
    "📄 Procesar video",
    type="primary",
    use_container_width=True
):

    if not url.strip():

        st.warning("Primero debes introducir una URL.")

    else:

        try:

            # 1. IDENTIFICAR VIDEO
            video_id = extract_video_id(url)

            st.info(f"Video identificado: {video_id}")

            # 2. OBTENER TITULO
            with st.spinner("Obteniendo título del video..."):

                title = get_video_title(video_id)

            st.write(f"**Título:** {title}")

            # 3. EXTRAER TRANSCRIPCION
            with st.spinner("Obteniendo transcripción de YouTube..."):

                agent = TranscriptAgent()
                result = agent.extract(video_id)

            # 4. GENERAR DOCUMENTO WORD
            with st.spinner("Generando documento Word..."):

                docx_path = generate_word_document(
                    title,
                    result,
                    OUTPUT_FOLDER
                )

            # 5. MOSTRAR RESULTADO
            st.success("¡Transcripción generada correctamente!")

            st.write(f"**Título:** {title}")
            st.write(f"**Idioma:** {result['language']}")
            st.write(f"**Fragmentos:** {result['fragments']}")
            st.write(f"**Caracteres:** {result['characters']}")

            # 6. BOTON DE DESCARGA
            with open(docx_path, "rb") as file:
                docx_bytes = file.read()

            st.download_button(
                label="⬇️ Descargar documento Word",
                data=docx_bytes,
                file_name=Path(docx_path).name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

        except Exception as error:

            st.error(
                f"Error al procesar el video: "
                f"{type(error).__name__}: {error}"
            )


# PIE DE PAGINA
st.divider()

st.caption(
    "YouTube Transcript Agent | "
    "Python + youtube-transcript-api + python-docx"
)

st.caption(
    "Genera y descarga tus transcripciones en formato Word."
)