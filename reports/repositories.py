# reports/repositories.py

"""
Obsahuje ORM operace pro modely Report, Section, Paragraph, Chart, Table.
"""

# obsahuje následující funkce
"""
get_report_by_id(report_id)
list_reports(filter_criteria)
get_reports_by_author(user)
create_report(title, topic, year, author)
update_report(report, **fields)
delete_report(report)
get_section_by_id(section_id)
get_sections_by_report(report)
create_section(report, title, order=None)
update_section(section, **fields)
delete_section(section)
get_paragraph_by_id(paragraph_id)
create_paragraph(section, text, order=None)
update_paragraph(paragraph, **fields)
delete_paragraph(paragraph)
get_chart_by_id(chart_id)
create_chart(section, title, dataset_file=None, data_source=None, order=None)
update_chart(chart, **fields)
delete_chart(chart)
get_table_by_id(table_id)
create_table(section, title, data=None, order=None)
update_table(table, **fields)
delete_table(table)
"""

from .models import Report, Section, Paragraph, Chart, Table
from django.db import models


# -------------------- Report Repository Functions --------------------

def get_report_by_id(report_id: int) -> Report:
    """
    Načte a vrátí Report objekt podle ID.

    Args:
        report_id: Primární klíč Report objektu.

    Returns:
        Report: Instance Report modelu.

    Raises:
        Report.DoesNotExist: Pokud Report s daným ID neexistuje.
    """
    return Report.objects.get(pk=report_id)


def list_reports(filter_criteria: dict = None) -> models.QuerySet[Report]: ###
    """
    Vrátí QuerySet reportů s možností filtrování.

    Args:
        filter_criteria: Slovník s filtry pro QuerySet (např. {'status': 'PUBLISHED'}).
                       Pokud None, vrací všechny reporty.

    Returns:
        models.QuerySet[Report]: QuerySet Report objektů.
    """
    queryset = Report.objects.all()
    if filter_criteria:
        # Přidáme validaci pro povolené stavy
        valid_statuses = [choice[0] for choice in Report.ReportStatus.choices]
        for key, value in filter_criteria.items():
            if key == 'status' and value not in valid_statuses:
                raise ValueError(f"Invalid report status: {value}. Must be one of: {valid_statuses}")
        queryset = queryset.filter(**filter_criteria)
    return queryset


def get_reports_by_author(author_user: 'User') -> models.QuerySet[Report]:
    """
    Vrátí QuerySet reportů vytvořených daným uživatelem.

    Args:
        author_user: Instance User modelu autora.

    Returns:
        models.QuerySet[Report]: QuerySet Report objektů.
    """
    return Report.objects.filter(author=author_user)


def create_report(title: str, topic: str, year: int, author: 'User') -> Report:
    """
    Vytvoří nový Report objekt a uloží ho do databáze.

    Args:
        title: Titul reportu.
        topic: Téma reportu.
        year: Rok reportu.
        author: Instance User modelu autora.

    Returns:
        Report: Nově vytvořený a uložený Report objekt.
    """
    report = Report.objects.create(title=title, topic=topic, year=year, author=author)
    return report


def update_report(report: Report, **fields: dict) -> Report:
    """
    Aktualizuje pole existujícího Report objektu.

    Args:
        report: Instance Report modelu k aktualizaci.
        fields: Slovník s poli a jejich novými hodnotami (např. {'title': 'Nový titulek'}).

    Returns:
        Report: Aktualizovaný Report objekt.
    """
    for key, value in fields.items():
        setattr(report, key, value)
    report.save()
    return report


def delete_report(report: Report) -> None:
    """
    Smaže Report objekt z databáze.

    Args:
        report: Instance Report modelu k smazání.
    """
    report.delete()


# -------------------- Section Repository Functions --------------------

def get_section_by_id(section_id: int) -> Section:
    """
    Načte a vrátí Section objekt podle ID.
    """
    return Section.objects.get(pk=section_id)


def get_sections_by_report(report: Report) -> models.QuerySet[Section]:
    """
    Vrátí QuerySet sekcí patřících k danému Reportu.
    """
    return Section.objects.filter(report=report).order_by('order')


def create_section(report: Report, title: str, order: int = None) -> Section:
    """
    Vytvoří novou Section pro daný Report.
    """
    if order is None:
        # Automatické určení pořadí, pokud není zadáno
        last_section = Section.objects.filter(report=report).order_by('-order').first()
        order = (last_section.order + 1) if last_section else 1
    section = Section.objects.create(report=report, title=title, order=order)
    return section


def update_section(section: Section, **fields: dict) -> Section:
    """
    Aktualizuje pole existujícího Section objektu.
    """
    for key, value in fields.items():
        setattr(section, key, value)
    section.save()
    return section


def delete_section(section: Section) -> None:
    """
    Smaže Section objekt z databáze.
    """
    section.delete()


# -------------------- Paragraph Repository Functions --------------------

def get_paragraph_by_id(paragraph_id: int) -> Paragraph: ###
    """
    Načte a vrátí Paragraph objekt podle ID.
    """
    try:
        return Paragraph.objects.get(pk=paragraph_id)
    except Paragraph.DoesNotExist:
        raise Paragraph.DoesNotExist(f"Paragraph with id {paragraph_id} not found.")


def create_paragraph(section: Section, text: str, order: int = None) -> Paragraph: ###
    """
    Vytvoří nový Paragraph v dané sekci.
    """
    if order is None:
        # Automatické určení pořadí
        last_paragraph = Paragraph.objects.filter(section=section).order_by('-order').first()
        order = (last_paragraph.order + 1) if last_paragraph else 1
    paragraph = Paragraph.objects.create(section=section, text=text, order=order, status=Paragraph.ContentElementStatus.DRAFT)
    return paragraph


def update_paragraph(paragraph: Paragraph, **fields: dict) -> Paragraph:
    """
    Aktualizuje pole existujícího Paragraph objektu.
    """
    for key, value in fields.items():
        setattr(paragraph, key, value)
    paragraph.save()
    return paragraph


def delete_paragraph(paragraph: Paragraph) -> None:
    """
    Smaže Paragraph objekt z databáze.
    """
    paragraph.delete()


# -------------------- Chart Repository Functions --------------------

def get_chart_by_id(chart_id: int) -> Chart: ###
    """
    Načte a vrátí Chart objekt podle ID.
    """
    try:
        return Chart.objects.get(pk=chart_id)
    except Chart.DoesNotExist:
        raise Chart.DoesNotExist(f"Chart with id {chart_id} not found.")


def create_chart(section: Section, title: str, dataset=None, data_source=None, order: int = None) -> Chart: ###
    """
    Vytvoří nový Chart v dané sekci.
    """
    if order is None:
        # Automatické určení pořadí
        last_chart = Chart.objects.filter(section=section).order_by('-order').first()
        order = (last_chart.order + 1) if last_chart else 1
    chart = Chart.objects.create(
        section=section, title=title, dataset=dataset, data_source=data_source, order=order, status=Chart.ContentElementStatus.DRAFT
    )
    return chart


def update_chart(chart: Chart, **fields: dict) -> Chart:
    """
    Aktualizuje pole existujícího Chart objektu.
    """
    for key, value in fields.items():
        setattr(chart, key, value)
    chart.save()
    return chart


def delete_chart(chart: Chart) -> None:
    """
    Smaže Chart objekt z databáze.
    """
    chart.delete()


# -------------------- Table Repository Functions --------------------

def get_table_by_id(table_id: int) -> Table: ###
    """
    Načte a vrátí Table objekt podle ID.
    """
    try:
        return Table.objects.get(pk=table_id)
    except Table.DoesNotExist:
        raise Table.DoesNotExist(f"Table with id {table_id} not found.")


def create_table(section: Section, title: str, data=None, data_source=None, order: int = None) -> Table: ###
    """
    Vytvoří nový Table v dané sekci.
    """
    if order is None:
        # Automatické určení pořadí
        last_table = Table.objects.filter(section=section).order_by('-order').first()
        order = (last_table.order + 1) if last_table else 1
    table = Table.objects.create(section=section, title=title, data=data, data_source=data_source, order=order, status=Table.ContentElementStatus.DRAFT)
    return table


def update_table(table: Table, **fields: dict) -> Table:
    """
    Aktualizuje pole existujícího Table objektu.
    """
    for key, value in fields.items():
        setattr(table, key, value)
    table.save()
    return table


def delete_table(table: Table) -> None:
    """
    Smaže Table objekt z databáze.
    """
    table.delete()
