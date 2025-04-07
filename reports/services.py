# reports/services.py

"""
Obsahuje business logiku pro práci s reporty, sekcemi a obsahem.
Využívá repository funkce z reports/repositories.py pro interakci s databází.
"""

"""
Seznam funkcí v `reports/services.py`:

Report Services
1. `create_report(data: dict, user: User) -> Report`
2. `submit_report_for_review(report: Report) -> Report`
3. `approve_report(report: Report, editor_user: User) -> Report`
4. `publish_report(report: Report, admin_user: User) -> Report`
5. `update_report_status(report: Report, new_status: str) -> Report`
6. `get_report_detail(report_id: int, user: User = None) -> Report`
7. `reorder_sections(report: Report) -> None`

Section Services
8. `add_section(report: Report, title: str) -> Section`
9. `remove_section(section: Section) -> None`
10. `move_section(section: Section, new_order: int) -> Section`

Content Element Services
11. `add_paragraph(section: Section, text: str) -> Paragraph`
12. `add_chart(section: Section, title: str, dataset_file=None, data_source=None) -> Chart`
13. `add_table(section: Section, title: str, data_source: 'DataSource') -> Table`
14. `edit_paragraph(paragraph: Paragraph, new_text: str) -> Paragraph`
15. `edit_chart(chart: Chart, new_title: str = None, new_dataset_file=None, new_data_source=None) -> Chart`
16. `edit_table(table: Table, new_title: str = None, refresh_data: bool = False) -> Table`
17. `reorder_content_elements(section: Section) -> None`
18. `remove_content_element(element: 'ContentElement') -> None`

"""

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from . import repositories
from . import utils
from .models import Report, Section, Paragraph, Chart, Table
from django.utils import timezone

# slovník s možnými změnami stavu reportu
# VALID_STATUS_TRANSITIONS = {
#     Report.ReportStatus.DRAFT: [Report.ReportStatus.STAGED],
#     Report.ReportStatus.STAGED: [Report.ReportStatus.APPROVED, Report.ReportStatus.DRAFT],
#     Report.ReportStatus.APPROVED: [Report.ReportStatus.PUBLISHED, Report.ReportStatus.STAGED],
#     Report.ReportStatus.PUBLISHED: [],  # Z publikovaného stavu už se obvykle nepřechází jinam
# }


# -------------------- Report Services --------------------

def create_report(data: dict, user: User) -> Report:
    """
    Vytvoří nový report.

    Args:
        data: Slovník s daty pro vytvoření reportu (title, topic, year).
        user: Uživatel, který report vytváří (autor).

    Returns:
        Report: Nově vytvořený report.

    Raises:
        ValidationError: Pokud validace dat selže.
    """
    utils.validate_report_data(data)  # Validace dat před uložením
    report = repositories.create_report(
        title=data['title'], topic=data['topic'], year=data['year'], author=user
    )
    return report

def publish_report(report: Report, admin_user: User) -> Report:  # Admin user for publishing
    """
    Publikuje schválený report (nastaví publication_date).

    Args:
        report: Report k publikování.
        admin_user: Uživatel, který publikuje report (admin).

    Returns:
        Report: Aktualizovaný report.

    Raises:
        ValidationError: Pokud report není ve stavu 'Approved' nebo uživatel nemá oprávnění.
    """
    # Kontrola, zda jsou všechny ContentElement ve stavu approved
    all_approved = True
    for section in report.sections.all():
        for element in section.content_elements.all():
            if element.status != element.ContentElementStatus.APPROVED:
                all_approved = False
                break
        if not all_approved:
            break

    if not all_approved:
        raise ValidationError("Nelze publikovat report, dokud nejsou všechny ContentElement schválené.")


    report = repositories.update_report(report, status=Report.ReportStatus.PUBLISHED)  # Nastavíme publication date
    # Zde by se mohly provést další kroky po publikaci (např. notifikace)
    return report

def update_report_status(report: Report, new_status: str) -> Report:
    """
    Obecná funkce pro změnu stavu reportu s validací přechodů.

    Args:
        report: Report, kterému se mění stav.
        new_status: Nový stav reportu (musí být z Report.ReportStatus).

    Returns:
        Report: Aktualizovaný report.

    Raises:
        ValidationError: Pokud přechod stavu není povolený.
    """
    valid_statuses = [choice[0] for choice in Report.ReportStatus.choices]
    if new_status not in valid_statuses:
        raise ValidationError(f"Invalid report status: {new_status}. Must be one of: {valid_statuses}")
    if report.status == Report.ReportStatus.PUBLISHED and new_status == Report.ReportStatus.OPEN:
        raise ValidationError("Z publikovaného reportu nelze udělat rozpracovaný.")


    report = repositories.update_report(report, status=new_status)
    return report

def get_report_detail(report_id: int, user: User = None) -> Report: # User is optional, for permission checks later
    """
    Načte detail reportu včetně sekcí a obsahu.

    Args:
        report_id: ID reportu k načtení.
        user: Aktuální uživatel (pro kontrolu oprávnění, pokud je potřeba).

    Returns:
        Report: Report objekt s prefetch_related pro sekce a content_elements.

    Raises:
        Report.DoesNotExist: Pokud report neexistuje.
        ValidationError: Pokud uživatel nemá oprávnění k zobrazení reportu.
    """
    report = repositories.get_report_by_id(report_id)
    report = Report.objects.prefetch_related('sections__content_elements').get(pk=report_id) # Re-fetch with prefetch
    return report

def reorder_sections(report: Report) -> None:
    """
    Přečísluje pořadí (order) všech sekcí v daném reportu.
    Zajišťuje sekvenční číslování od 1 bez mezer.

    Args:
        report: Report, jehož sekce se mají přečíslovat.
    """
    sections = repositories.get_sections_by_report(report) # Get sections ordered by 'order' already
    current_order = 1
    for section in sections:
        if section.order != current_order: # Only update if order is not already correct to avoid unnecessary saves
            repositories.update_section(section, order=current_order)
        current_order += 1


# -------------------- Section Services --------------------

def add_section(report: Report, title: str) -> Section:
    """
    Přidá novou sekci do reportu.

    Args:
        report: Report, do kterého se přidává sekce.
        title: Titul sekce.

    Returns:
        Section: Nově vytvořená sekce.

    Raises:
        ValidationError: Pokud validace dat sekce selže (např. duplicitní název).
    """
    # Zde by mohla být validace, např. kontrola duplicity názvu sekce v rámci reportu

    section = repositories.create_section(report=report, title=title)
    return section


def remove_section(section: Section) -> None:
    """
    Odstraní sekci z reportu.

    Args:
        section: Sekce k odstranění.

    Raises:
        ValidationError: Pokud operace není povolena (např. mazání publikované sekce).
    """
    try:
        report = section.report
    except Section.DoesNotExist:
        raise Section.DoesNotExist("Section with id does not exist")

    # Zde by mohla být kontrola oprávnění, např. editor může mazat jen draft sekce
    repositories.delete_section(section)
    reorder_sections(report)

def move_section(section: Section, new_order: int) -> Section:
    """
    Změní pořadí sekce v rámci reportu a provede přečíslování ostatních sekcí.
    """
    if not isinstance(new_order, int) or new_order <= 0:
        raise ValidationError("New order must be a positive integer.")

    report = section.report
    sections = list(repositories.get_sections_by_report(report)) # Get sections as list for manipulation
    if new_order > len(sections):
        raise ValidationError("New order is out of range for the number of sections.")


    old_order = section.order
    if old_order == new_order:
        return section # No change needed if orders are the same

    section = repositories.update_section(section, order=new_order) # Update the moved section's order

    if old_order < new_order: # Moving section down in order
        for s in sections:
            if s != section and old_order <= s.order <= new_order: # Shift sections between old and new order up by 1 if they are not the moved section
                repositories.update_section(s, order=s.order - 1)
    elif old_order > new_order: # Moving section up in order
        for s in sections:
            if s != section and new_order <= s.order <= old_order: # Shift sections between new and old order down by 1 if they are not the moved section
                 repositories.update_section(s, order=s.order + 1)

    reorder_sections(report) # Final reordering to ensure sequential order from 1 to N after move. Redundant but safer.
    return section

# -------------------- Content Element Services --------------------

def add_paragraph(section: Section, text: str, author: User) -> Paragraph:
    try:
        utils.validate_paragraph_data({'text': text})
    except ValidationError as e:
        raise e

    paragraph = repositories.create_paragraph(section=section, text=text, author=author)
    utils.reorder_section_content(section)
    return paragraph

def add_chart(section: Section, title: str, dataset_file=None, data_source=None, author=None) -> Chart:
    """
    Přidá nový graf do sekce.

    Args:
        section: Sekce, do které se přidává graf.
        title: Titul grafu.
        dataset_file: Soubor s daty pro graf (volitelné).
        data_source: Datový zdroj pro graf (volitelné, místo dataset_file).

    Returns:
        Chart: Nově vytvořený graf.
    """
    try:
        utils.validate_chart_data({'title': title}) # Validace
    except ValidationError as e:
        raise e
    chart = repositories.create_chart(
        section=section, title=title, dataset=dataset_file, data_source=data_source, author=author #oprava dataset_file -> dataset
    )
    utils.reorder_section_content(section) # Volání přímo utility funkce utils.reorder_section_content
    return chart

def add_table(section: Section, title: str, data_source: 'DataSource') -> Table:
    """
    Přidá novou tabulku do sekce.

    Args:
        section: Sekce, do které se přidává tabulka.
        title: Titul tabulky.
        data_source: Datový zdroj pro tabulku.

    Returns:
        Table: Nově vytvořená tabulka.
    """
    try:
        utils.validate_table_data({'title': title}) # Validace
    except ValidationError as e:
        raise e

    # Zde by se mohlo načíst data z data_source a uložit do Table.data (DataSourceService.fetch_data)
    table = repositories.create_table(section=section, title=title, data=None, data_source=data_source) # Data might be fetched and updated later
    utils.reorder_section_content(section) # Volání přímo utility funkce utils.reorder_section_content
    return table

def edit_paragraph(paragraph: Paragraph, new_text: str) -> Paragraph:
    """
    Upraví text odstavce.

    Args:
        paragraph: Odstavec k úpravě.
        new_text: Nový text odstavce.

    Returns:
        Paragraph: Aktualizovaný odstavec.

    Raises:
        ValidationError: Pokud operace není povolena (např. report není publikovaný, nebo uživatel je autor).
    """
    try:
        utils.validate_paragraph_data({'text': new_text}) # Validace dat
    except ValidationError as e:
        raise e

    paragraph = repositories.update_paragraph(paragraph, text=new_text)
    return paragraph


def edit_chart(chart: Chart, new_title: str = None, new_dataset_file=None, new_data_source=None) -> Chart:
    """
    Upraví vlastnosti grafu (titul, dataset, datový zdroj).

    Args:
        chart: Graf k úpravě.
        new_title: Nový titul grafu (volitelné).
        new_dataset_file: Nový datový soubor pro graf (volitelné).
        new_data_source: Nový datový zdroj pro graf (volitelné).

    Returns:
        Chart: Aktualizovaný graf.
    """
    fields_to_update = {}
    if new_title is not None:
        try:
            utils.validate_chart_data({'title': new_title})  # Validace titulku
        except ValidationError as e:
            raise e
        fields_to_update['title'] = new_title
    if new_dataset_file is not None:
        fields_to_update['dataset'] = new_dataset_file
    if new_data_source is not None:
        fields_to_update['data_source'] = new_data_source

    if fields_to_update:
        chart = repositories.update_chart(chart, **fields_to_update)
    return chart

def edit_table(table: Table, new_title: str = None, refresh_data: bool = False) -> Table:
    """
    Upraví vlastnosti tabulky (titul, případně obnoví data ze zdroje). - Data refresh not implemented yet

    Args:
        table: Tabulka k úpravě.
        new_title: Nový titul tabulky (volitelné).
        refresh_data: True, pokud se mají obnovit data ze zdroje (volitelné). - Not yet implemented

    Returns:
        Table: Aktualizovaná tabulka.
    """
    fields_to_update = {}
    if new_title is not None:
        try:
            utils.validate_table_data({'title': new_title})
        except ValidationError as e:
            raise e
        fields_to_update['title'] = new_title

    if fields_to_update:
        table = repositories.update_table(table, **fields_to_update)

    if refresh_data:
        raise NotImplementedError("Refresh data for table not implemented yet.") # Placeholder for data refresh logic

    return table

def remove_content_element(element: 'ContentElement') -> None: # Type Hinting for abstract model is tricky, using string literal
    """
    Odstraní prvek obsahu (odstavec, graf, tabulku) ze sekce.

    Args:
        element: Prvek obsahu k odstranění (instance Paragraph, Chart nebo Table).

    Raises:
        ValidationError: Pokud operace není povolena.
    """
    try:
        section = element.section # Get section BEFORE deleting element
    except Section.DoesNotExist as e:
        raise e

    if isinstance(element, Paragraph):
        repositories.delete_paragraph(element)
    elif isinstance(element, Chart):
        repositories.delete_chart(element)
    elif isinstance(element, Table):
        repositories.delete_table(element)
    else:
        raise ValueError("Unsupported content element type.")

    utils.reorder_section_content(section)