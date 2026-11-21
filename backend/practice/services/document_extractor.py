from pathlib import Path

from pypdf import PdfReader
from docx import Document
from pptx import Presentation


def extract_pdf_text(file_obj):
    """Extract text from a PDF file."""

    reader = PdfReader(file_obj)

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            extracted_pages.append(
                f"[Page {page_number}]\n{text.strip()}"
            )

    return "\n\n".join(extracted_pages)


def extract_word_text(file_obj):
    """Extract text from a Word document."""

    document = Document(file_obj)

    extracted_content = []

    # Extract paragraphs.
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            extracted_content.append(text)

    # Extract text from tables.
    for table in document.tables:
        for row in table.rows:
            cells = [
                cell.text.strip()
                for cell in row.cells
                if cell.text.strip()
            ]

            if cells:
                extracted_content.append(" | ".join(cells))

    return "\n\n".join(extracted_content)


def extract_powerpoint_text(file_obj):
    """Extract text from PowerPoint slides."""

    presentation = Presentation(file_obj)

    extracted_slides = []

    for slide_number, slide in enumerate(
        presentation.slides,
        start=1
    ):
        slide_content = []

        for shape in slide.shapes:

            if shape.has_text_frame:
                text = shape.text.strip()

                if text:
                    slide_content.append(text)

            if shape.has_table:
                for row in shape.table.rows:
                    cells = [
                        cell.text.strip()
                        for cell in row.cells
                        if cell.text.strip()
                    ]

                    if cells:
                        slide_content.append(" | ".join(cells))

        if slide_content:
            extracted_slides.append(
                f"[Slide {slide_number}]\n"
                + "\n".join(slide_content)
            )

    return "\n\n".join(extracted_slides)


def extract_text_from_file(file_obj):
    """Identify the file type and extract its text."""

    extension = Path(file_obj.name).suffix.lower()

    file_obj.seek(0)

    if extension == ".pdf":
        extracted_text = extract_pdf_text(file_obj)

    elif extension == ".docx":
        extracted_text = extract_word_text(file_obj)

    elif extension == ".pptx":
        extracted_text = extract_powerpoint_text(file_obj)

    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    if not extracted_text.strip():
        raise ValueError(
            f"No readable text was found in {file_obj.name}."
        )

    return extracted_text.strip()


def extract_text_from_materials(materials):
    """Extract and combine text from all uploaded lecture notes."""

    combined_content = []

    for material in materials:

        file_obj = material.file

        try:
            extracted_text = extract_text_from_file(file_obj)

            combined_content.append(
                f"\n\n========== "
                f"{Path(file_obj.name).name} "
                f"==========\n\n"
                f"{extracted_text}"
            )

        except Exception as error:
            raise ValueError(
                f"Could not read {Path(file_obj.name).name}: {error}"
            ) from error

    if not combined_content:
        raise ValueError(
            "No lecture notes were available for extraction."
        )

    return "\n".join(combined_content)