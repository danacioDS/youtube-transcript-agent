
import json
import os
import re
import zipfile

from agent.transcript import TranscriptAgent
from agent.document import generate_documents



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = os.path.join(BASE_DIR, "config", "videos.json")
OUTPUT = "/mnt/c/Users/DANIEL/Documents/Video_transcripts"
LOGS = os.path.join(BASE_DIR, "logs")


def extract_video_id(url):

    match = re.search(
        r'(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})',
        url
    )

    if not match:
        raise ValueError(f"URL no válida: {url}")

    return match.group(1)


def run_agent():

    os.makedirs(OUTPUT, exist_ok=True)
    os.makedirs(LOGS, exist_ok=True)

    with open(CONFIG, "r", encoding="utf-8") as file:
        videos = json.load(file)

    agent = TranscriptAgent()

    successes = 0
    failures = []

    for index, video in enumerate(videos, 1):

        title = video["titulo"]
        filename = video["archivo"]

        print(f"\n[{index}/{len(videos)}] {title}")

        docx_path = os.path.join(OUTPUT, f"{filename}.docx")

        if os.path.exists(docx_path):
            print("   ⏭️ Ya procesado.")
            successes += 1
            continue

        try:

            video_id = extract_video_id(video["url"])

            result = agent.extract(video_id)

            result["video_id"] = video_id

            txt_path, docx_path = generate_documents(
                title,
                result,
                OUTPUT
            )

            print(f"   ✅ Word: {docx_path}")
            print(f"   ✅ TXT: {txt_path}")
            print(f"   📊 Caracteres: {result['characters']}")

            successes += 1

        except Exception as error:

            message = f"{title}: {type(error).__name__}: {error}"

            print(f"   ❌ {message}")
            failures.append(message)

    # Crear ZIP
    zip_path = os.path.join(BASE_DIR, "transcripciones.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:

        for filename in os.listdir(OUTPUT):

            filepath = os.path.join(OUTPUT, filename)

            if os.path.isfile(filepath):
                archive.write(filepath, arcname=filename)

    # Registrar errores
    with open(
        os.path.join(LOGS, "errores.txt"),
        "w",
        encoding="utf-8"
    ) as file:

        file.write("\n".join(failures))

    print("\n" + "=" * 55)
    print(f"Videos procesados: {successes}")
    print(f"Errores: {len(failures)}")
    print(f"ZIP generado: {zip_path}")
    print("=" * 55)


if __name__ == "__main__":
    run_agent()
