# reports/utils.py

"""
Obsahuje pomocné utility funkce pro aplikaci reports.
Zahrnuje validace dat, manipulaci s obsahem, generování souborů apod.
"""

"""
Seznam funkcí v `reports/utils.py`:

Validace dat
1. `validate_report_data(data: dict) -> None`
2. `validate_section_data(data: dict) -> None`
3. `validate_paragraph_data(data: dict) -> None`
4. `validate_chart_data(data: dict) -> None`
5. `validate_table_data(data: dict) -> None`

Přečíslování obsahu
6. `reorder_section_content(section: Section) -> None`

Generování souborů
7. `generate_pdf(report: Report) -> bytes`
8. `generate_chart_preview(chart: Chart) -> str`
"""

from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Report, Section, ContentElement, Paragraph, Chart, Table


# -------------------- Validation Functions --------------------

def validate_report_data(data: dict) -> None:
    """
    Validuje data pro vytvoření nebo aktualizaci Report objektu.

    Args:
        data: Slovník s daty reportu (title, topic, year).

    Raises:
        ValidationError: Pokud validace selže.
    """
    if not data.get('title'):
        raise ValidationError("Title is required for a report.")
    if not data.get('topic'):
        raise ValidationError("Topic is required for a report.")
    if not isinstance(data.get('year'), int):
        raise ValidationError("Year must be an integer.")
    if data.get('year') < 1900 or data.get('year') > 2100:  # Rozumný rozsah letopočtu
        raise ValidationError("Year must be within a reasonable range (1900-2100).")


def validate_section_data(data: dict) -> None:
    """
    Validuje data pro vytvoření nebo aktualizaci Section objektu.

    Args:
        data: Slovník s daty sekce (title).

    Raises:
        ValidationError: Pokud validace selže.
    """
    if not data.get('title'):
        raise ValidationError("Title is required for a section.")


def validate_paragraph_data(data: dict) -> None:
    """
    Validuje data pro vytvoření nebo aktualizaci Paragraph objektu.

    Args:
        data: Slovník s daty odstavce (text).

    Raises:
        ValidationError: Pokud validace selže.
    """
    if not data.get('text'):
        raise ValidationError("Text is required for a paragraph.")


def validate_chart_data(data: dict) -> None:
    """
    Validuje data pro vytvoření nebo aktualizaci Chart objektu.

    Args:
        data: Slovník s daty grafu (title).

    Raises:
        ValidationError: Pokud validace selže.
    """
    if not data.get('title'):
        raise ValidationError("Title is required for a chart.")
    # Zde by se mohly přidat validace pro dataset_file nebo data_source, pokud je to potřeba

def validate_table_data(data: dict) -> None:
    """
    Validuje data pro vytvoření nebo aktualizaci Table objektu.

    Args:
        data: Slovník s daty tabulky (title).

    Raises:
        ValidationError: Pokud validace selže.
    """
    if not data.get('title'):
        raise ValidationError("Title is required for a table.")
    # Zde by se mohly přidat validace pro data (JSONField), pokud je to potřeba

# -------------------- Content Reordering Functions --------------------

# ________________ Původní verze def reorder_section_content() - aktualizace každého prvku zvlášť

# from django.db import transaction

# def reorder_section_content(section: Section) -> None:
#     """
#     Přečísluje pořadí (order) všech prvků obsahu v dané sekci.
#     """
#     content_elements = list(ContentElement.objects.filter(section=section).order_by("order"))

#     with transaction.atomic():  # Zabráníme částečným zápisům
#         for index, element in enumerate(content_elements, start=1):
#             if element.order != index:
#                 print(f"🔄 Updating ID={element.id} from {element.order} to {index}")  # Debug
#                 ContentElement.objects.filter(id=element.id).update(order=index)  # Přímý SQL UPDATE

from django.db import transaction

def reorder_section_content(section: Section) -> None:
    """
    Přečísluje pořadí (order) všech prvků obsahu v dané sekci efektivně pomocí `bulk_update()`.
    """
    content_elements = list(ContentElement.objects.filter(section=section).order_by("order"))

    if not content_elements:
        return  # Pokud není nic k přeuspořádání, skončíme

    with transaction.atomic():  # Zajistí, že všechny změny proběhnou najednou
        for index, element in enumerate(content_elements, start=1):
            if element.order != index:
                print(f"🔄 Updating ID={element.id} from {element.order} to {index}")  # Debug
                element.order = index  # Změníme hodnotu v paměti

        ContentElement.objects.bulk_update(content_elements, ["order"])  # Hromadná aktualizace


# -------------------- File Generation Functions --------------------

def generate_pdf(report: Report) -> bytes:
    from io import BytesIO
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    """
        Generuje PDF dokument z Report objektu.

    Args:
        report: Report objekt k exportu do PDF.

    Returns:
        bytes: Binární obsah PDF souboru.

    Raises:
        Exception: Pokud generování PDF selže (např. chyba knihovny ReportLab).
    """

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(inch, 10.5 * inch, report.title)

    p.setFont("Helvetica", 12)
    y_position = 10 * inch
    p.drawString(inch, y_position, f"Author: {report.author}")
    y_position -= 0.3 * inch
    p.drawString(inch, y_position, f"Topic: {report.topic}")
    y_position -= 0.3 * inch
    p.drawString(inch, y_position, f"Year: {report.year}")
    y_position -= 0.5 * inch

    p.setFont("Helvetica-Bold", 14)
    for section in report.sections.order_by("order"):
        p.drawString(inch, y_position, section.title)
        y_position -= 0.3 * inch
        p.setFont("Helvetica", 12)

        for element in section.content_elements.order_by("order"):
            if isinstance(element, Paragraph):
                text_lines = element.text.split("\n")
                for line in text_lines:
                    p.drawString(inch + 0.2 * inch, y_position, line)
                    y_position -= 0.3 * inch  # Posun dolů
            
            elif isinstance(element, Chart):
                p.drawString(inch + 0.2 * inch, y_position, f"Chart: {element.title} (Chart visualization not implemented in PDF)")
                y_position -= 0.3 * inch

            elif isinstance(element, Table):
                p.drawString(inch + 0.2 * inch, y_position, f"Table: {element.title} (Table data not implemented in PDF)")
                y_position -= 0.3 * inch

        y_position -= 0.5 * inch
        if y_position < inch:
            p.showPage()
            y_position = 10.5 * inch

    p.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data

def generate_chart_preview(chart: Chart) -> str: # Returns path to preview image file - Not fully implemented
    """
    Generuje náhled grafu (obrázek) pro Chart objekt. - Placeholder, needs charting library integration

    Args:
        chart: Chart objekt, pro který se má vygenerovat náhled.

    Returns:
        str: Cesta k vygenerovanému obrázku náhledu (např. PNG soubor).

    Raises:
        NotImplementedError: Pokud generování náhledu grafu není implementováno.
    """
    raise NotImplementedError("Chart preview generation not implemented yet. Needs charting library integration (e.g., matplotlib, seaborn).")
    # Implementace generování náhledu grafu (např. pomocí matplotlib nebo seaborn)
    # Uložení obrázku do souboru a vrácení cesty k souboru