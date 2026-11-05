
import os
import re

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH


def divide_paragraphs(text, sentences_per_paragraph=5):

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    return [
        " ".join(sentences[i:i + sentences_per_paragraph])
        for i in range(0, len(sentences), sentences_per_paragraph)
    ]


def generate_documents(title, result, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    name = re.sub(r'[^\w-]+', '_', title).strip('_')[:80]

    txt_path = os.path.join(output_folder, f"{name}.txt")
    docx_path = os.path.join(output_folder, f"{name}.docx")

    text = result["text"]

    # Generar TXT
    with open(txt_path, "w", encoding="utf-8") as file:
        file.write(text)

    # Generar Word
    doc = Document()

    heading = doc.add_heading(title, level=0)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle = doc.add_paragraph(
        "Transcripción completa — Idioma original"
    )
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    info = doc.add_paragraph(
        f"Video ID: {result['video_id']} | "
        f"Idioma: {result['language']}"
    )
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading("Transcripción", level=1)

    for paragraph_text in divide_paragraphs(text):

        paragraph = doc.add_paragraph(paragraph_text)

        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(8)

        for run in paragraph.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(11)

    footer = doc.add_paragraph()
    run = footer.add_run(
        f"Total: {result['characters']} caracteres"
    )
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(120, 120, 120)

    doc.save(docx_path)

    return txt_path, docx_path



def generate_word_document(title, result, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    name = re.sub(
        r'[^\w-]+',
        '_',
        title
    ).strip('_')[:80]

    docx_path = os.path.join(
        output_folder,
        f"{name}.docx"
    )

    text = result["text"]

    doc = Document()

    heading = doc.add_heading(title, level=0)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle = doc.add_paragraph(
        "Transcripción completa — Idioma original"
    )
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    info = doc.add_paragraph(
        f"Video ID: {result['video_id']} | "
        f"Idioma: {result['language']}"
    )
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading("Transcripción", level=1)

    for paragraph_text in divide_paragraphs(text):

        paragraph = doc.add_paragraph(paragraph_text)

        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.space_after = Pt(8)

        for run in paragraph.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(11)

    footer = doc.add_paragraph()

    run = footer.add_run(
        f"Total: {result['characters']} caracteres"
    )

    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(120, 120, 120)

    doc.save(docx_path)

    return docx_path

