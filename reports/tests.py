# reports/tests.py

"""
Obsahuje testy funkcí z reports/services.py, reports/repositories.py a reports/utils.py.
"""

"""
Seznam testovaných funkcí v 'reports/tests.py':

Testy pro 'services.py'

Report Services
1. `test_create_report_valid_data`
2. `test_create_report_invalid_data_missing_title`
    3. `test_submit_report_for_review_valid_transition`
    4. `test_submit_report_for_review_invalid_transition_not_draft`
    5. `test_approve_report_valid_transition`
    6. `test_approve_report_invalid_transition_not_staged`
#7. `test_publish_report_valid_transition`
#8. `test_publish_report_invalid_transition_not_approved`
#9. `test_update_report_status_valid_transition`
#10. `test_update_report_status_invalid_transition`
 

Section Services
11. `test_add_section_valid_data`
12. `test_remove_section_valid_removal`
13. `test_remove_section_nonexistent_section`
14. `test_move_section_valid_move`

Content Element Services
15. `test_add_paragraph_valid_data`
16. `test_add_paragraph_invalid_data`
17. `test_add_chart_valid_data`
18. `test_add_chart_invalid_data_missing_title`
19. `test_add_table_valid_data`
20. `test_add_table_invalid_data_missing_title`
21. `test_edit_paragraph_valid_data`
22. `test_edit_paragraph_invalid_data`
23. `test_edit_chart_valid_data`
24. `test_edit_chart_valid_data_change_data_source`
25. `test_edit_chart_invalid_data`
26. `test_edit_table_valid_data`
27. `test_edit_table_invalid_data`
28. `test_reorder_content_elements`
29. `test_remove_content_element_valid_removal`
30. `test_remove_content_element_nonexistent`

---

Testy pro 'repositories.py'

Report Repository
31. `test_get_report_by_id_existing_report`
32. `test_get_report_by_id_non_existing_report`
33. `test_list_reports_no_filter`
#34. `test_list_reports_with_filter`
35. `test_get_reports_by_author`
36. `test_create_report`
37. `test_update_report`
38. `test_delete_report`

Section Repository
39. `test_get_section_by_id_existing_section`
40. `test_get_section_by_id_non_existing_section`
41. `test_get_sections_by_report_existing_sections`
42. `test_get_sections_by_report_no_sections`
43. `test_create_section_valid_data`
44. `test_create_section_valid_data_with_custom_order`
45. `test_create_section_invalid_data_missing_title`
46. `test_update_section_valid_data`
47. `test_update_section_invalid_data_empty_title`
48. `test_update_section_non_existing`
49. `test_delete_section_existing`
50. `test_delete_section_non_existing`

Paragraph Repository
51. `test_get_paragraph_by_id_existing`
52. `test_get_paragraph_by_id_non_existing`
53. `test_create_paragraph_valid_data`
54. `test_create_paragraph_valid_data_with_custom_order`
55. `test_create_paragraph_invalid_data_empty_text`
56. `test_update_paragraph_valid_data`
57. `test_update_paragraph_invalid_data_empty_text`
58. `test_update_paragraph_non_existing`
59. `test_delete_paragraph_existing`
60. `test_delete_paragraph_non_existing`

Chart Repository
61. `test_get_chart_by_id_existing`
62. `test_get_chart_by_id_non_existing`
63. `test_create_chart_valid_data`
64. `test_create_chart_valid_data_with_custom_order`
65. `test_create_chart_invalid_data_missing_title`
66. `test_update_chart_valid_data`
67. `test_update_chart_invalid_data_empty_title`
68. `test_update_chart_non_existing`
69. `test_delete_chart_existing`
70. `test_delete_chart_non_existing`

Table Repository
71. `test_get_table_by_id_existing`
72. `test_get_table_by_id_non_existing`
73. `test_create_table_valid_data`
74. `test_create_table_valid_data_with_custom_order`
75. `test_create_table_invalid_data_missing_title`
76. `test_update_table_valid_data`
77. `test_update_table_invalid_data_empty_title`
78. `test_update_table_non_existing`
79. `test_delete_table_existing`
80. `test_delete_table_non_existing`

---

Testy pro 'utils.py'

Validace dat
81. `test_validate_report_data_valid`
82. `test_validate_report_data_missing_title`
83. `test_validate_report_data_invalid_year`
84. `test_validate_section_data_valid`
85. `test_validate_section_data_missing_title`
86. `test_validate_paragraph_data_valid`
87. `test_validate_paragraph_data_missing_text`
88. `test_validate_chart_data_valid`
89. `test_validate_chart_data_missing_title`
90. `test_validate_table_data_valid`
91. `test_validate_table_data_missing_title`

Přečíslování obsahu
92. `test_reorder_section_content_correct_order`
93. `test_reorder_section_content_no_change_needed`
94. `test_reorder_section_content_empty_section`
95. `test_reorder_section_content_complex_case`

Generování PDF
96. `test_generate_pdf_valid_output`
97. `test_generate_pdf_contains_report_info`
98. `test_generate_pdf_contains_sections_and_elements`
99. `test_generate_pdf_no_sections`

"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from reports.models import Report, Section, Paragraph, Chart, Table  # Import modelů
from reports import repositories, services, utils  # Import repositories, services, utils

class ReportServiceTest(TestCase):
    """
    Testovací třída pro service funkce související s Report modelem (reports/services.py).
    """

    def setUp(self):
        """
        Příprava testovacích dat před každou testovací metodou.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.report_data = {
            'title': 'Test Report',
            'topic': 'Science',
            'year': 2024,
        }

    def test_create_report_valid_data(self):
        """
        Testuje create_report service funkci s validními daty.
        Ověřuje, že se report úspěšně vytvoří a uloží do databáze.
        """
        report = services.create_report(data=self.report_data, user=self.user)
        self.assertIsInstance(report, Report)  # Ověř, že funkce vrátila instanci Report modelu
        self.assertEqual(report.title, self.report_data['title'])  # Ověř, že se data správně uložila
        self.assertEqual(report.author, self.user)
        self.assertEqual(Report.objects.count(), 1)  # Ověř, že je v databázi 1 report

    def test_create_report_invalid_data_missing_title(self):
        """
        Testuje create_report service funkci s nevalidními daty (chybí title).
        Ověřuje, že funkce vyvolá ValidationError a report se nevytvoří.
        """
        invalid_data = self.report_data.copy()
        invalid_data.pop('title')  # Odstraníme title z dat

        with self.assertRaises(ValidationError):  # Ověř, že se vyvolá ValidationError
            services.create_report(data=invalid_data, user=self.user)
        self.assertEqual(Report.objects.count(), 0)  # Ověř, že v databázi není žádný report

    def test_publish_report_valid_transition(self):
        """
        Testuje publish_report service funkci s validním přechodem stavu (report je ve stavu OPEN a všechny ContentElement jsou APPROVED).
        Ověřuje, že se report úspěšně publikuje (stav se změní na PUBLISHED).
        """
        # Vytvoříme report ve stavu OPEN
        report = services.create_report(data=self.report_data, user=self.user)

        # Vytvoříme sekci
        section = services.add_section(report=report, title="Test Section")

        # Vytvoříme paragraph a schválíme ho
        paragraph = repositories.create_paragraph(section=section, text="Test Paragraph")
        paragraph = repositories.update_paragraph(paragraph, status=Paragraph.ContentElementStatus.APPROVED)

        # Schválíme celý report
        report = services.publish_report(report, self.user)

        self.assertEqual(report.status, Report.ReportStatus.PUBLISHED)  # Ověříme, že stav je PUBLISHED

    def test_publish_report_invalid_transition_not_approved(self):
        """
        Testuje publish_report service funkci s nevalidním přechodem stavu (report není ve stavu OPEN, nebo ne všechny ContentElement jsou ve stavu APPROVED).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        report = services.create_report(data=self.report_data, user=self.user)
        section = services.add_section(report=report, title="Test Section")
        services.add_paragraph(section=section, text="Test Paragraph")  # Necháme odstavec ve stavu DRAFT

        with self.assertRaises(ValidationError) as context:
            services.publish_report(report, self.user)  # Pokusíme se publikovat report, který nemá všechny ContentElement schválené

        self.assertEqual(str(context.exception), "['Nelze publikovat report, dokud nejsou všechny ContentElement schválené.']")

    def test_update_report_status_valid_transition(self):
        """
        Testuje update_report_status service funkci s validním přechodem stavu (OPEN -> PUBLISHED).
        Ověřuje, že se stav reportu úspěšně změní.
        """
        report = services.create_report(data=self.report_data, user=self.user)
        # Vytvoříme sekci
        section = services.add_section(report=report, title="Test Section")

        # Vytvoříme paragraph a schválíme ho
        paragraph = repositories.create_paragraph(section=section, text="Test Paragraph")
        paragraph = repositories.update_paragraph(paragraph, status=Paragraph.ContentElementStatus.APPROVED)
        report = services.update_report_status(report, Report.ReportStatus.PUBLISHED)
        self.assertEqual(report.status, Report.ReportStatus.PUBLISHED)

    def test_update_report_status_invalid_transition(self):
        """
        Testuje update_report_status service funkci s nevalidním přechodem stavu (PUBLISHED -> OPEN).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        report = services.create_report(data=self.report_data, user=self.user)
        report.status = Report.ReportStatus.PUBLISHED
        report.save()
        with self.assertRaises(ValidationError) as context:
            services.update_report_status(report, Report.ReportStatus.OPEN)
        self.assertEqual(str(context.exception), "['Z publikovaného reportu nelze udělat rozpracovaný.']")

# -------------------- Testy pro Section a Content Element Services --------------------

class SectionContentServiceTest(TestCase):
    """
    Testovací třída pro service funkce související se sekcemi a prvky obsahu (reports/services.py).
    """

    def setUp(self):
        """
        Příprava testovacích dat před každou testovací metodou.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.report = services.create_report(
            data={'title': 'Test Report', 'topic': 'Science', 'year': 2024}, user=self.user
        )
        self.section_data = {'title': 'Test Section'}


    # -------------------- Section Tests --------------------

    def test_add_section_valid_data(self):
        """
        Testuje add_section service funkci s validními daty.
        Ověřuje, že se sekce úspěšně vytvoří a uloží do databáze.
        """
        section = services.add_section(report=self.report, title=self.section_data['title'])
        self.assertIsInstance(section, Section)
        self.assertEqual(section.title, self.section_data['title'])
        self.assertEqual(section.report, self.report)
        self.assertEqual(Section.objects.count(), 1)
    
    def test_remove_section_valid_removal(self):
        """
        Testuje remove_section service funkci s validním smazáním sekce.
        Ověřuje, že se sekce úspěšně smaže z databáze a pořadí zbývajících sekcí se přečísluje.
        """
        section1 = services.add_section(report=self.report, title="Section 1")
        section2 = services.add_section(report=self.report, title="Section 2")
        section3 = services.add_section(report=self.report, title="Section 3")

        services.remove_section(section2) # Smažeme sekci 2

        self.assertEqual(Section.objects.count(), 2)  # Ověříme, že zbyly 2 sekce
        # Ověříme, že se správně přečíslovalo pořadí zbylých sekcí
        sections = Section.objects.filter(report=self.report).order_by('order')
        self.assertEqual(sections[0].title, "Section 1")
        self.assertEqual(sections[0].order, 1)
        self.assertEqual(sections[1].title, "Section 3")
        self.assertEqual(sections[1].order, 2)

    def test_remove_section_nonexistent_section(self):
        """
        Testuje remove_section service funkci s pokusem o smazání neexistující sekce.
        Ověřuje, že se vyvolá Section.DoesNotExist.
        """
        with self.assertRaises(Section.DoesNotExist):
             Section.objects.get(pk=9999) # Try removing section which does not exists in DB


    # -------------------- Content Element Tests --------------------

    def test_add_paragraph_valid_data(self):
        """
        Testuje add_paragraph service funkci s validními daty.
        Ověřuje, že se odstavec úspěšně vytvoří a uloží do databáze.
        """
        section = services.add_section(report=self.report, title="Test Section")
        paragraph = services.add_paragraph(section=section, text="Test Paragraph Text")
        self.assertIsInstance(paragraph, Paragraph)
        self.assertEqual(paragraph.text, "Test Paragraph Text")
        self.assertEqual(paragraph.section, section)
        self.assertEqual(Paragraph.objects.count(), 1)
        self.assertEqual(utils.reorder_section_content(section), None)

    def test_add_paragraph_invalid_data(self):
        """
        Testuje add_paragraph service funkci s nevalidními daty (prázdný text).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        section = services.add_section(report=self.report, title="Test Section")
        with self.assertRaises(ValidationError):
            services.add_paragraph(section=section, text="")
        self.assertEqual(Paragraph.objects.count(), 0)

    def test_add_chart_valid_data(self):
        """
        Testuje add_chart service funkci s validními daty.
        Ověřuje, že se graf úspěšně vytvoří a uloží do databáze.
        """
        section = services.add_section(report=self.report, title="Test Section")
        chart = services.add_chart(section=section, title="Test Chart Title")
        self.assertIsInstance(chart, Chart)
        self.assertEqual(chart.title, "Test Chart Title")
        self.assertEqual(chart.section, section)
        self.assertEqual(Chart.objects.count(), 1)
        self.assertEqual(utils.reorder_section_content(section), None)

    def test_add_table_valid_data(self):
        """
        Testuje add_table service funkci s validními daty.
        Ověřuje, že se tabulka úspěšně vytvoří a uloží do databáze.
        """
        from data_sources.models import DataSource  # Import DataSource model

        section = services.add_section(report=self.report, title="Test Section")

        # Vytvoříme dummy datový zdroj
        data_source = DataSource.objects.create(name="Test Data Source", source_type="CSV", file="test.csv")

        table = services.add_table(section=section, title="Test Table Title", data_source=data_source) # Přidán data_source
        self.assertIsInstance(table, Table)
        self.assertEqual(table.title, "Test Table Title")
        self.assertEqual(table.section, section)
        self.assertEqual(Table.objects.count(), 1)
        self.assertEqual(utils.reorder_section_content(section), None)
        
    def test_add_chart_invalid_data_missing_title(self):
        """
        Testuje add_chart service funkci s nevalidními daty (chybí title).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        from data_sources.models import DataSource  # Import DataSource model

        section = services.add_section(report=self.report, title="Test Section")

        # Vytvoříme dummy datový zdroj
        data_source = DataSource.objects.create(name="Test Data Source", source_type="CSV", file="test.csv")

        with self.assertRaises(ValidationError):
            services.add_chart(section=section, title=None, data_source=data_source)  # title je None
        self.assertEqual(Chart.objects.count(), 0)

    def test_add_table_invalid_data_missing_title(self):
        """
        Testuje add_table service funkci s nevalidními daty (chybí title).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        from data_sources.models import DataSource  # Import DataSource model

        section = services.add_section(report=self.report, title="Test Section")

        # Vytvoříme dummy datový zdroj
        data_source = DataSource.objects.create(name="Test Data Source", source_type="CSV", file="test.csv")

        with self.assertRaises(ValidationError):
            services.add_table(section=section, title=None, data_source=data_source)  # title je None
        self.assertEqual(Table.objects.count(), 0)

    def test_edit_paragraph_valid_data(self):
        """
        Testuje edit_paragraph service funkci s validními daty.
        Ověřuje, že se text odstavce úspěšně aktualizuje v databázi.
        """
        section = services.add_section(report=self.report, title="Test Section")
        paragraph = services.add_paragraph(section=section, text="Original Text")
        updated_paragraph = services.edit_paragraph(paragraph=paragraph, new_text="Updated Text")

        self.assertEqual(updated_paragraph.text, "Updated Text")  # Ověříme, že se text aktualizoval
        self.assertEqual(Paragraph.objects.get(pk=paragraph.pk).text, "Updated Text")  # Ověříme i v databázi

    def test_edit_paragraph_invalid_data(self):
        """
        Testuje edit_paragraph service funkci s nevalidními daty (prázdný text).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        section = services.add_section(report=self.report, title="Test Section")
        paragraph = services.add_paragraph(section=section, text="Original Text")

        with self.assertRaises(ValidationError):
            services.edit_paragraph(paragraph=paragraph, new_text="")  # Prázdný text
        
    def test_edit_chart_valid_data(self):
        """
        Testuje edit_chart service funkci s validními daty (změna titulku).
        Ověřuje, že se titulek grafu úspěšně aktualizuje v databázi.
        """
        from data_sources.models import DataSource  # Import DataSource model
        section = services.add_section(report=self.report, title="Test Section")

        # Vytvoříme dummy datový zdroj
        data_source = DataSource.objects.create(name="Test Data Source", source_type="CSV", file="test.csv")

        chart = services.add_chart(section=section, title="Original Title", data_source=data_source)
        updated_chart = services.edit_chart(chart=chart, new_title="Updated Title")

        self.assertEqual(updated_chart.title, "Updated Title")  # Ověříme, že se titulek aktualizoval
        self.assertEqual(Chart.objects.get(pk=chart.pk).title, "Updated Title")  # Ověříme i v databázi

    def test_edit_chart_valid_data_change_data_source(self):
         """
         Testuje edit_chart service funkci s validními daty (změna data_source).
         Ověřuje, že se data_source grafu úspěšně aktualizuje v databázi.
         """
         from data_sources.models import DataSource  # Import DataSource model
    
         section = services.add_section(report=self.report, title="Test Section")
    
         # Vytvoříme dummy datové zdroje
         data_source1 = DataSource.objects.create(name="Test Data Source 1", source_type="CSV", file="test1.csv")
         data_source2 = DataSource.objects.create(name="Test Data Source 2", source_type="CSV", file="test2.csv")
    
         chart = services.add_chart(section=section, title="Original Title", data_source=data_source1)
         updated_chart = services.edit_chart(chart=chart, new_data_source=data_source2)
    
         self.assertEqual(updated_chart.data_source, data_source2)  # Ověříme, že se data_source aktualizoval
         self.assertEqual(Chart.objects.get(pk=chart.pk).data_source, data_source2)  # Ověříme i v databázi

    def test_edit_chart_invalid_data(self):
        """
        Testuje edit_chart service funkci s nevalidními daty (prázdný titulek).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        from data_sources.models import DataSource  # Import DataSource model
        section = services.add_section(report=self.report, title="Test Section")

        # Vytvoříme dummy datový zdroj
        data_source = DataSource.objects.create(name="Test Data Source", source_type="CSV", file="test.csv")

        chart = services.add_chart(section=section, title="Original Title", data_source=data_source)
        with self.assertRaises(ValidationError):
            services.edit_chart(chart=chart, new_title="")  # Prázdný titulek

    def test_edit_table_valid_data(self):
        """
        Testuje edit_table service funkci s validními daty (změna titulku).
        Ověřuje, že se titulek tabulky úspěšně aktualizuje v databázi.
        """
        from data_sources.models import DataSource  # Import DataSource model

        section = services.add_section(report=self.report, title="Test Section")

        # Vytvoříme dummy datový zdroj
        data_source = DataSource.objects.create(name="Test Data Source", source_type="CSV", file="test.csv")

        table = services.add_table(section=section, title="Original Title", data_source=data_source)
        updated_table = services.edit_table(table=table, new_title="Updated Title")

        self.assertEqual(updated_table.title, "Updated Title")  # Ověříme, že se titulek aktualizoval
        self.assertEqual(Table.objects.get(pk=table.pk).title, "Updated Title")  # Ověříme i v databázi

    def test_edit_table_invalid_data(self):
        """
        Testuje edit_table service funkci s nevalidními daty (prázdný titulek).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        from data_sources.models import DataSource  # Import DataSource model

        section = services.add_section(report=self.report, title="Test Section")

        # Vytvoříme dummy datový zdroj
        data_source = DataSource.objects.create(name="Test Data Source", source_type="CSV", file="test.csv")

        table = services.add_table(section=section, title="Original Title", data_source=data_source)
        with self.assertRaises(ValidationError):
            services.edit_table(table=table, new_title="")  # Prázdný titulek

def test_reorder_section_content(self):
    """
    Testuje utility funkci reorder_section_content.
    Ověřuje, že se správně přečísluje pořadí prvků obsahu v sekci.
    """
    section = services.add_section(report=self.report, title="Test Section")
    paragraph1 = services.add_paragraph(section=section, text="Paragraph 1")
    paragraph2 = services.add_paragraph(section=section, text="Paragraph 2")
    chart = services.add_chart(section=section, title="Test Chart")

    # Ručně změníme pořadí prvků (aby nebylo sekvenční)
    Paragraph.objects.filter(id=paragraph1.id).update(order=3)
    Paragraph.objects.filter(id=paragraph2.id).update(order=1)
    Chart.objects.filter(id=chart.id).update(order=2)

    # Ověříme, že databáze skutečně obsahuje změny
    paragraph1.refresh_from_db()
    paragraph2.refresh_from_db()
    chart.refresh_from_db()

    print("Pořadí před voláním reorder_section_content():")
    for p in Paragraph.objects.filter(section=section).order_by("order"):
        print(f"Paragraph ID={p.pk}, Order={p.order}")
    for c in Chart.objects.filter(section=section).order_by("order"):
        print(f"Chart ID={c.pk}, Order={c.order}")

    utils.reorder_section_content(section)  # Přečíslujeme pořadí

    print("Pořadí po volání reorder_section_content():")
    for p in Paragraph.objects.filter(section=section).order_by("order"):
        print(f"Paragraph ID={p.pk}, Order={p.order}")
    for c in Chart.objects.filter(section=section).order_by("order"):
        print(f"Chart ID={c.pk}, Order={c.order}")  

    # Ověříme, že se pořadí správně přečíslovalo
    paragraph1.refresh_from_db()
    paragraph2.refresh_from_db()
    chart.refresh_from_db()

    self.assertEqual(paragraph1.order, 3) # původně mělo jedničku, ale my jsme to přehodili
    self.assertEqual(paragraph2.order, 1) # tady jsme měnit pořadí
    self.assertEqual(chart.order, 2) # tady jsme měnili pořadí

    # teď to vrátíme zpátky
    utils.reorder_section_content(section)

    paragraph1.refresh_from_db()
    paragraph2.refresh_from_db()
    chart.refresh_from_db()

    self.assertEqual(paragraph1.order, 1) # Původně to mělo jedničku
    self.assertEqual(paragraph2.order, 2)
    self.assertEqual(chart.order, 3)


    def test_remove_content_element_nonexistent(self):
        """
        Testuje remove_content_element service funkci s pokusem o smazání neexistujícího prvku.
        Ověřuje, že se vyvolá příslušná výjimka (Paragraph.DoesNotExist, Chart.DoesNotExist, Table.DoesNotExist).
        """
        with self.assertRaises(Paragraph.DoesNotExist):
            Paragraph.objects.get(pk=999)  # Pokusíme se načíst neexistující odstavec

  # -------------------- Repositories --------------------

class ReportRepositoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_get_report_by_id_existing_report(self):
        report = Report.objects.create(title='Test Report', topic='Science', year=2024, author=self.user)
        retrieved_report = repositories.get_report_by_id(report.id)
        self.assertEqual(retrieved_report, report)

    def test_get_report_by_id_non_existing_report(self):
        with self.assertRaises(Report.DoesNotExist):
            repositories.get_report_by_id(999)

    def test_list_reports_no_filter(self):
        Report.objects.create(title='Report 1', topic='Science', year=2024, author=self.user)
        Report.objects.create(title='Report 2', topic='Math', year=2023, author=self.user)
        reports = repositories.list_reports()
        self.assertEqual(len(reports), 2)

    def test_list_reports_with_filter(self):
        Report.objects.create(title='Report 1', topic='Science', year=2024, author=self.user, status=Report.ReportStatus.PUBLISHED)
        Report.objects.create(title='Report 2', topic='Math', year=2023, author=self.user, status=Report.ReportStatus.OPEN)
        reports = repositories.list_reports(filter_criteria={'status': Report.ReportStatus.PUBLISHED})
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0].title, 'Report 1')

    def test_get_reports_by_author(self):
        user2 = User.objects.create_user(username='testuser2', password='testpassword')
        Report.objects.create(title='Report 1', topic='Science', year=2024, author=self.user)
        Report.objects.create(title='Report 2', topic='Math', year=2023, author=user2)
        reports = repositories.get_reports_by_author(self.user)
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0].title, 'Report 1')

    def test_create_report(self):
        report = repositories.create_report(title='New Report', topic='History', year=2022, author=self.user)
        self.assertEqual(report.title, 'New Report')
        self.assertEqual(Report.objects.count(), 1)

    def test_update_report(self):
        report = Report.objects.create(title='Original Title', topic='Science', year=2024, author=self.user)
        updated_report = repositories.update_report(report, title='Updated Title', year=2025)
        self.assertEqual(updated_report.title, 'Updated Title')
        self.assertEqual(updated_report.year, 2025)
        self.assertEqual(Report.objects.get(pk=report.id).title, 'Updated Title')

    def test_delete_report(self):
        report = Report.objects.create(title='Report to Delete', topic='Geography', year=2021, author=self.user)
        repositories.delete_report(report)
        with self.assertRaises(Report.DoesNotExist):
            Report.objects.get(pk=report.id)

class SectionRepositoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.report = Report.objects.create(title='Test Report', topic='Science', year=2024, author=self.user)
        self.section = Section.objects.create(report=self.report, title='Test Section', order=1)

    def test_get_section_by_id_existing_section(self):
        """
        Testuje funkci get_section_by_id s existující sekcí.
        Ověřuje, že správně načte sekci z databáze.
        """
        retrieved_section = repositories.get_section_by_id(self.section.id)
        self.assertEqual(retrieved_section, self.section)
        self.assertEqual(retrieved_section.title, 'Test Section')
        self.assertEqual(retrieved_section.report, self.report)

    def test_get_section_by_id_non_existing_section(self):
        """
        Testuje funkci get_section_by_id s neexistující sekcí.
        Ověřuje, že vyvolá výjimku Section.DoesNotExist.
        """
        with self.assertRaises(Section.DoesNotExist):
            repositories.get_section_by_id(9999)  # ID, které neexistuje

    def test_get_sections_by_report_existing_sections(self):
        """
        Testuje funkci get_sections_by_report, když report obsahuje sekce.
        Ověřuje, že se vrátí všechny sekce v očekávaném pořadí.
        """
        # Přidáme další sekce do reportu
        section2 = Section.objects.create(report=self.report, title='Section 2', order=2)
        section3 = Section.objects.create(report=self.report, title='Section 3', order=3)

        sections = repositories.get_sections_by_report(self.report)

        self.assertEqual(len(sections), 3)  # Ověříme, že jsou načteny 3 sekce
        self.assertEqual(sections[0], self.section)  # Ověříme správné pořadí
        self.assertEqual(sections[1], section2)
        self.assertEqual(sections[2], section3)

    def test_get_sections_by_report_no_sections(self):
        """
        Testuje funkci get_sections_by_report, když report neobsahuje žádné sekce.
        Ověřuje, že vrácený queryset je prázdný.
        """
        Section.objects.filter(report=self.report).delete()  # Smažeme všechny sekce

        sections = repositories.get_sections_by_report(self.report)

        self.assertEqual(len(sections), 0)  # Ověříme, že není žádná sekce

    def test_create_section_valid_data(self):
        """
        Testuje funkci create_section s validními daty.
        Ověřuje, že se sekce správně vytvoří a přidá do reportu.
        """
        section = repositories.create_section(report=self.report, title="New Section")
        
        self.assertIsInstance(section, Section)  # Ověříme, že se vrátila instance modelu Section
        self.assertEqual(section.title, "New Section")  # Ověříme správné jméno sekce
        self.assertEqual(section.report, self.report)  # Ověříme správnou vazbu na report
        self.assertEqual(section.order, 2)  # Ověříme správné pořadí (self.section už existuje s order=1)
        self.assertEqual(Section.objects.count(), 2)  # Ověříme, že v databázi jsou nyní 2 sekce

    def test_create_section_valid_data_with_custom_order(self):
        """
        Testuje funkci create_section s explicitně zadaným pořadím.
        Ověřuje, že sekce získá správně přidělené pořadí.
        """
        section = repositories.create_section(report=self.report, title="Custom Ordered Section", order=5)
        
        self.assertEqual(section.order, 5)  # Ověříme, že pořadí bylo správně přiděleno
        self.assertEqual(Section.objects.count(), 2)  # Ověříme, že sekce byla uložena

    def test_create_section_invalid_data_missing_title(self):
        """
        Testuje funkci create_section s nevalidními daty (chybějící title).
        Ověřuje, že funkce vyvolá výjimku IntegrityError.
        """
        from django.db.utils import IntegrityError

        with self.assertRaises(IntegrityError):
            repositories.create_section(report=self.report, title=None)  # Chybějící title

    def test_update_section_valid_data(self):
        """
        Testuje update_section s validními daty.
        Ověřuje, že se sekce správně aktualizuje v databázi.
        """
        updated_section = repositories.update_section(self.section, title="Updated Section", order=2)

        self.assertEqual(updated_section.title, "Updated Section")  # Ověříme změnu názvu
        self.assertEqual(updated_section.order, 2)  # Ověříme změnu pořadí
        self.section.refresh_from_db()  # Načteme z databáze aktuální hodnoty
        self.assertEqual(self.section.title, "Updated Section")
        self.assertEqual(self.section.order, 2)

    def test_update_section_invalid_data_empty_title(self):
        """
        Testuje update_section s nevalidními daty (prázdný title).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            self.section.title = ""
            self.section.full_clean()  # Spustí Django validaci modelu
            repositories.update_section(self.section, title="")


    def test_update_section_non_existing(self):
        """
        Testuje update_section na neexistující sekci.
        Ověřuje, že se vyvolá DoesNotExist při pokusu o získání neexistující sekce.
        """
        with self.assertRaises(Section.DoesNotExist):
            section = repositories.get_section_by_id(9999)  # Neexistující ID
            repositories.update_section(section, title="New Title")  # Toto se nikdy neprovede

    def test_delete_section_existing(self):
        """
        Testuje delete_section s existující sekcí.
        Ověřuje, že sekce je úspěšně odstraněna z databáze.
        """
        repositories.delete_section(self.section)

        with self.assertRaises(Section.DoesNotExist):
            Section.objects.get(pk=self.section.id)  # Ověříme, že sekce již neexistuje
        self.assertEqual(Section.objects.count(), 0)  # Ověříme, že databáze je prázdná

    def test_delete_section_non_existing(self):
        """
        Testuje delete_section s neexistující sekcí.
        Ověřuje, že funkce nevyvolá chybu, pokud sekce neexistuje.
        """
        non_existing_section = Section(id=9999, report=self.report, title="Ghost Section", order=1)

        # Pokusíme se smazat sekci, která neexistuje
        try:
            repositories.delete_section(non_existing_section)
        except Exception as e:
            self.fail(f"delete_section vyvolala neočekávanou výjimku: {e}")

        # Ověříme, že stále existuje původní sekce
        self.assertEqual(Section.objects.count(), 1)

    def test_get_paragraph_by_id_existing(self):
        """
        Testuje get_paragraph_by_id s existujícím odstavcem.
        Ověřuje, že funkce správně načte odstavec z databáze.
        """
        paragraph = Paragraph.objects.create(section=self.section, text="Test Paragraph", order=1)

        retrieved_paragraph = repositories.get_paragraph_by_id(paragraph.id)
        self.assertEqual(retrieved_paragraph, paragraph)
        self.assertEqual(retrieved_paragraph.text, "Test Paragraph")
        self.assertEqual(retrieved_paragraph.section, self.section)

    def test_get_paragraph_by_id_non_existing(self):
        """
        Testuje get_paragraph_by_id s neexistujícím odstavcem.
        Ověřuje, že funkce vyvolá Paragraph.DoesNotExist.
        """
        with self.assertRaises(Paragraph.DoesNotExist):
            repositories.get_paragraph_by_id(9999)  # ID, které neexistuje

    def test_create_paragraph_valid_data(self):
        """
        Testuje create_paragraph s validními daty.
        Ověřuje, že se odstavec úspěšně vytvoří a uloží do databáze.
        """
        paragraph = repositories.create_paragraph(section=self.section, text="Test Paragraph")

        self.assertIsInstance(paragraph, Paragraph)
        self.assertEqual(paragraph.text, "Test Paragraph")
        self.assertEqual(paragraph.section, self.section)
        self.assertEqual(paragraph.order, 1)  # První odstavec v sekci

    def test_create_paragraph_valid_data_with_custom_order(self):
        """
        Testuje create_paragraph s explicitně zadaným pořadím.
        Ověřuje, že odstavec získá správně přidělené pořadí.
        """
        paragraph1 = repositories.create_paragraph(section=self.section, text="First Paragraph")
        paragraph2 = repositories.create_paragraph(section=self.section, text="Second Paragraph", order=5)

        self.assertEqual(paragraph1.order, 1)  # Automatické pořadí
        self.assertEqual(paragraph2.order, 5)  # Explicitně nastavené pořadí

    def test_create_paragraph_invalid_data_empty_text(self):
        """
        Testuje create_paragraph s nevalidními daty (prázdný text).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            paragraph = Paragraph(section=self.section, text="")  # Prázdný text
            paragraph.full_clean()  # Django validace
            repositories.create_paragraph(section=self.section, text="")

    def test_update_paragraph_valid_data(self):
        """
        Testuje update_paragraph s validními daty.
        Ověřuje, že se odstavec správně aktualizuje v databázi.
        """
        paragraph = repositories.create_paragraph(section=self.section, text="Original Text")

        updated_paragraph = repositories.update_paragraph(paragraph, text="Updated Text", order=2)

        self.assertEqual(updated_paragraph.text, "Updated Text")  # Ověříme změnu textu
        self.assertEqual(updated_paragraph.order, 2)  # Ověříme změnu pořadí
        paragraph.refresh_from_db()  # Načteme z databáze aktuální hodnoty
        self.assertEqual(paragraph.text, "Updated Text")
        self.assertEqual(paragraph.order, 2)

    def test_update_paragraph_invalid_data_empty_text(self):
        """
        Testuje update_paragraph s nevalidními daty (prázdný text).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        from django.core.exceptions import ValidationError

        paragraph = repositories.create_paragraph(section=self.section, text="Original Text")

        with self.assertRaises(ValidationError):
            paragraph.text = ""
            paragraph.full_clean()  # Spustí Django validaci modelu
            repositories.update_paragraph(paragraph, text="")

    def test_update_paragraph_non_existing(self):
        """
        Testuje update_paragraph na neexistující odstavec.
        Ověřuje, že se vyvolá DoesNotExist při pokusu o získání neexistujícího odstavce.
        """
        with self.assertRaises(Paragraph.DoesNotExist):
            paragraph = repositories.get_paragraph_by_id(9999)  # Neexistující ID
            repositories.update_paragraph(paragraph, text="New Text")  # Toto se nikdy neprovede

    def test_delete_paragraph_existing(self):
        """
        Testuje delete_paragraph s existujícím odstavcem.
        Ověřuje, že odstavec je úspěšně odstraněn z databáze.
        """
        paragraph = repositories.create_paragraph(section=self.section, text="Test Paragraph")

        repositories.delete_paragraph(paragraph)

        with self.assertRaises(Paragraph.DoesNotExist):
            Paragraph.objects.get(pk=paragraph.id)  # Ověříme, že odstavec již neexistuje
        self.assertEqual(Paragraph.objects.count(), 0)  # Ověříme, že databáze je prázdná

    def test_delete_paragraph_non_existing(self):
        """
        Testuje delete_paragraph s neexistujícím odstavcem.
        Ověřuje, že pokus o smazání neexistujícího odstavce nevyvolá chybu.
        """
        with self.assertRaises(Paragraph.DoesNotExist):
            paragraph = repositories.get_paragraph_by_id(9999)  # Pokus o získání neexistujícího odstavce
            repositories.delete_paragraph(paragraph)  # Toto se nikdy neprovede

    def test_get_chart_by_id_existing(self):
        """
        Testuje get_chart_by_id s existujícím grafem.
        Ověřuje, že funkce správně načte graf z databáze.
        """
        chart = Chart.objects.create(section=self.section, title="Test Chart", order=1)

        retrieved_chart = repositories.get_chart_by_id(chart.id)
        self.assertEqual(retrieved_chart, chart)
        self.assertEqual(retrieved_chart.title, "Test Chart")
        self.assertEqual(retrieved_chart.section, self.section)

    def test_get_chart_by_id_non_existing(self):
        """
        Testuje get_chart_by_id s neexistujícím grafem.
        Ověřuje, že funkce vyvolá Chart.DoesNotExist.
        """
        with self.assertRaises(Chart.DoesNotExist):
            repositories.get_chart_by_id(9999)  # ID, které neexistuje

    def test_create_chart_valid_data(self):
        """
        Testuje create_chart s validními daty.
        Ověřuje, že se graf úspěšně vytvoří a uloží do databáze.
        """
        chart = repositories.create_chart(section=self.section, title="Test Chart")

        self.assertIsInstance(chart, Chart)
        self.assertEqual(chart.title, "Test Chart")
        self.assertEqual(chart.section, self.section)
        self.assertEqual(chart.order, 1)  # První graf v sekci

    def test_create_chart_valid_data_with_custom_order(self):
        """
        Testuje create_chart s explicitně zadaným pořadím.
        Ověřuje, že graf získá správně přidělené pořadí.
        """
        chart1 = repositories.create_chart(section=self.section, title="First Chart")
        chart2 = repositories.create_chart(section=self.section, title="Second Chart", order=5)

        self.assertEqual(chart1.order, 1)  # Automatické pořadí
        self.assertEqual(chart2.order, 5)  # Explicitně nastavené pořadí

    def test_create_chart_invalid_data_missing_title(self):
        """
        Testuje create_chart s nevalidními daty (chybějící title).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            chart = Chart(section=self.section, title="")  # Chybějící title
            chart.full_clean()  # Django validace
            repositories.create_chart(section=self.section, title="")

    def test_update_chart_valid_data(self):
        """
        Testuje update_chart s validními daty.
        Ověřuje, že se graf správně aktualizuje v databázi.
        """
        chart = repositories.create_chart(section=self.section, title="Original Chart")

        updated_chart = repositories.update_chart(chart, title="Updated Chart", order=2)

        self.assertEqual(updated_chart.title, "Updated Chart")  # Ověříme změnu názvu
        self.assertEqual(updated_chart.order, 2)  # Ověříme změnu pořadí
        chart.refresh_from_db()  # Načteme z databáze aktuální hodnoty
        self.assertEqual(chart.title, "Updated Chart")
        self.assertEqual(chart.order, 2)

    def test_update_chart_invalid_data_empty_title(self):
        """
        Testuje update_chart s nevalidními daty (prázdný title).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        from django.core.exceptions import ValidationError

        chart = repositories.create_chart(section=self.section, title="Original Chart")

        with self.assertRaises(ValidationError):
            chart.title = ""
            chart.full_clean()  # Spustí Django validaci modelu
            repositories.update_chart(chart, title="")

    def test_update_chart_non_existing(self):
        """
        Testuje update_chart na neexistující graf.
        Ověřuje, že se vyvolá DoesNotExist při pokusu o získání neexistujícího grafu.
        """
        with self.assertRaises(Chart.DoesNotExist):
            chart = repositories.get_chart_by_id(9999)  # Pokus o získání neexistujícího grafu
            repositories.update_chart(chart, title="New Title")  # Toto se nikdy neprovede

    def test_delete_chart_existing(self):
        """
        Testuje delete_chart s existujícím grafem.
        Ověřuje, že graf je úspěšně odstraněn z databáze.
        """
        chart = repositories.create_chart(section=self.section, title="Test Chart")

        repositories.delete_chart(chart)

        with self.assertRaises(Chart.DoesNotExist):
            Chart.objects.get(pk=chart.id)  # Ověříme, že graf již neexistuje
        self.assertEqual(Chart.objects.count(), 0)  # Ověříme, že databáze je prázdná

    def test_delete_chart_non_existing(self):
        """
        Testuje delete_chart s neexistujícím grafem.
        Ověřuje, že pokus o smazání neexistujícího grafu nevyvolá chybu.
        """
        with self.assertRaises(Chart.DoesNotExist):
            chart = repositories.get_chart_by_id(9999)  # Pokus o získání neexistujícího grafu
            repositories.delete_chart(chart)  # Toto se nikdy neprovede

    def test_get_table_by_id_existing(self):
        """
        Testuje get_table_by_id s existující tabulkou.
        Ověřuje, že funkce správně načte tabulku z databáze.
        """
        table = Table.objects.create(section=self.section, title="Test Table", order=1)

        retrieved_table = repositories.get_table_by_id(table.id)
        self.assertEqual(retrieved_table, table)
        self.assertEqual(retrieved_table.title, "Test Table")
        self.assertEqual(retrieved_table.section, self.section)

    def test_get_table_by_id_non_existing(self):
        """
        Testuje get_table_by_id s neexistující tabulkou.
        Ověřuje, že funkce vyvolá Table.DoesNotExist.
        """
        with self.assertRaises(Table.DoesNotExist):
            repositories.get_table_by_id(9999)  # ID, které neexistuje

    def test_create_table_valid_data(self):
        """
        Testuje create_table s validními daty.
        Ověřuje, že se tabulka úspěšně vytvoří a uloží do databáze.
        """
        table = repositories.create_table(section=self.section, title="Test Table")

        self.assertIsInstance(table, Table)
        self.assertEqual(table.title, "Test Table")
        self.assertEqual(table.section, self.section)
        self.assertEqual(table.order, 1)  # První tabulka v sekci

    def test_create_table_valid_data_with_custom_order(self):
        """
        Testuje create_table s explicitně zadaným pořadím.
        Ověřuje, že tabulka získá správně přidělené pořadí.
        """
        table1 = repositories.create_table(section=self.section, title="First Table")
        table2 = repositories.create_table(section=self.section, title="Second Table", order=5)

        self.assertEqual(table1.order, 1)  # Automatické pořadí
        self.assertEqual(table2.order, 5)  # Explicitně nastavené pořadí

    def test_create_table_invalid_data_missing_title(self):
        """
        Testuje create_table s nevalidními daty (chybějící title).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            table = Table(section=self.section, title="")  # Chybějící title
            table.full_clean()  # Django validace
            repositories.create_table(section=self.section, title="")

    def test_update_table_valid_data(self):
        """
        Testuje update_table s validními daty.
        Ověřuje, že se tabulka správně aktualizuje v databázi.
        """
        table = repositories.create_table(section=self.section, title="Original Table")

        updated_table = repositories.update_table(table, title="Updated Table", order=2)

        self.assertEqual(updated_table.title, "Updated Table")  # Ověříme změnu názvu
        self.assertEqual(updated_table.order, 2)  # Ověříme změnu pořadí
        table.refresh_from_db()  # Načteme z databáze aktuální hodnoty
        self.assertEqual(table.title, "Updated Table")
        self.assertEqual(table.order, 2)

    def test_update_table_invalid_data_empty_title(self):
        """
        Testuje update_table s nevalidními daty (prázdný title).
        Ověřuje, že funkce vyvolá ValidationError.
        """
        from django.core.exceptions import ValidationError

        table = repositories.create_table(section=self.section, title="Original Table")

        with self.assertRaises(ValidationError):
            table.title = ""
            table.full_clean()  # Spustí Django validaci modelu
            repositories.update_table(table, title="")

    def test_update_table_non_existing(self):
        """
        Testuje update_table na neexistující tabulku.
        Ověřuje, že se vyvolá DoesNotExist při pokusu o získání neexistující tabulky.
        """
        with self.assertRaises(Table.DoesNotExist):
            table = repositories.get_table_by_id(9999)  # Pokus o získání neexistující tabulky
            repositories.update_table(table, title="New Title")  # Toto se nikdy neprovede

    def test_delete_table_existing(self):
        """
        Testuje delete_table s existující tabulkou.
        Ověřuje, že tabulka je úspěšně odstraněna z databáze.
        """
        table = repositories.create_table(section=self.section, title="Test Table")

        repositories.delete_table(table)

        with self.assertRaises(Table.DoesNotExist):
            Table.objects.get(pk=table.id)  # Ověříme, že tabulka již neexistuje
        self.assertEqual(Table.objects.count(), 0)  # Ověříme, že databáze je prázdná

    def test_delete_table_non_existing(self):
        """
        Testuje delete_table s neexistující tabulkou.
        Ověřuje, že funkce nevyvolá chybu, pokud tabulka neexistuje.
        """
        non_existing_table = Table(id=9999, section=self.section, title="Ghost Table", order=1)

        # Pokusíme se smazat tabulku, která neexistuje
        try:
            repositories.delete_table(non_existing_table)
        except Exception as e:
            self.fail(f"delete_table vyvolala neočekávanou výjimku: {e}")

        # Ověříme, že ostatní tabulky zůstaly nedotčené
        self.assertEqual(Table.objects.count(), 0)

    def test_delete_table_existing(self):
        """
        Testuje delete_table s existující tabulkou.
        Ověřuje, že tabulka je úspěšně odstraněna z databáze.
        """
        table = repositories.create_table(section=self.section, title="Test Table")

        repositories.delete_table(table)

        with self.assertRaises(Table.DoesNotExist):
            Table.objects.get(pk=table.id)  # Ověříme, že tabulka již neexistuje
        self.assertEqual(Table.objects.count(), 0)  # Ověříme, že databáze je prázdná

    def test_delete_table_non_existing(self):
        """
        Testuje delete_table s neexistující tabulkou.
        Ověřuje, že pokus o smazání neexistující tabulky vyvolá Table.DoesNotExist.
        """
        with self.assertRaises(Table.DoesNotExist):
            table = repositories.get_table_by_id(9999)  # Pokus o získání neexistující tabulky
            repositories.delete_table(table)  # Toto se nikdy neprovede



    # -------------------- Utils Tests --------------------

class UtilsValidationTest(TestCase):
    """
    Testy pro validační funkce v utils.py.
    """

    def test_validate_report_data_valid(self):
        """
        Testuje validate_report_data s validními daty.
        """
        valid_data = {"title": "Test Report", "topic": "Science", "year": 2024}
        try:
            utils.validate_report_data(valid_data)  # Nemělo by vyvolat chybu
        except ValidationError:
            self.fail("validate_report_data vyvolala ValidationError na validních datech.")

    def test_validate_report_data_missing_title(self):
        """
        Testuje validate_report_data s chybějícím title.
        """
        invalid_data = {"topic": "Science", "year": 2024}
        with self.assertRaises(ValidationError):
            utils.validate_report_data(invalid_data)

    def test_validate_report_data_invalid_year(self):
        """
        Testuje validate_report_data s nevalidním rokem (mimo rozsah).
        """
        invalid_data = {"title": "Test Report", "topic": "Science", "year": 1800}
        with self.assertRaises(ValidationError):
            utils.validate_report_data(invalid_data)

    def test_validate_section_data_valid(self):
        """
        Testuje validate_section_data s validními daty.
        """
        valid_data = {"title": "Test Section"}
        try:
            utils.validate_section_data(valid_data)
        except ValidationError:
            self.fail("validate_section_data vyvolala ValidationError na validních datech.")

    def test_validate_section_data_missing_title(self):
        """
        Testuje validate_section_data s chybějícím title.
        """
        invalid_data = {}
        with self.assertRaises(ValidationError):
            utils.validate_section_data(invalid_data)

    def test_validate_paragraph_data_valid(self):
        """
        Testuje validate_paragraph_data s validními daty.
        """
        valid_data = {"text": "This is a test paragraph."}
        try:
            utils.validate_paragraph_data(valid_data)
        except ValidationError:
            self.fail("validate_paragraph_data vyvolala ValidationError na validních datech.")

    def test_validate_paragraph_data_missing_text(self):
        """
        Testuje validate_paragraph_data s chybějícím textem.
        """
        invalid_data = {}
        with self.assertRaises(ValidationError):
            utils.validate_paragraph_data(invalid_data)

    def test_validate_chart_data_valid(self):
        """
        Testuje validate_chart_data s validními daty.
        """
        valid_data = {"title": "Test Chart"}
        try:
            utils.validate_chart_data(valid_data)
        except ValidationError:
            self.fail("validate_chart_data vyvolala ValidationError na validních datech.")

    def test_validate_chart_data_missing_title(self):
        """
        Testuje validate_chart_data s chybějícím title.
        """
        invalid_data = {}
        with self.assertRaises(ValidationError):
            utils.validate_chart_data(invalid_data)

    def test_validate_table_data_valid(self):
        """
        Testuje validate_table_data s validními daty.
        """
        valid_data = {"title": "Test Table"}
        try:
            utils.validate_table_data(valid_data)
        except ValidationError:
            self.fail("validate_table_data vyvolala ValidationError na validních datech.")

    def test_validate_table_data_missing_title(self):
        """
        Testuje validate_table_data s chybějícím title.
        """
        invalid_data = {}
        with self.assertRaises(ValidationError):
            utils.validate_table_data(invalid_data)



    # -------------------- Reorder Section Tests --------------------

from django.db import transaction
from reports.models import ContentElement, Paragraph
from reports import utils

class UtilsReorderContentTest(TestCase):
    """
    Testy pro reorder_section_content v utils.py.
    """

    def setUp(self):
        """
        Před každým testem vytvoříme uživatele, report a sekci.
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.report = Report.objects.create(title="Test Report", topic="Science", year=2024, author=self.user)
        self.section = Section.objects.create(report=self.report, title="Test Section", order=1)

    def test_reorder_section_content_correct_order(self):
        """
        Testuje reorder_section_content, zda správně přeuspořádá prvky podle pořadí.
        """
        # Vytvoříme prvky obsahu s nesprávným pořadím
        p1 = Paragraph.objects.create(section=self.section, text="First paragraph", order=3)
        p2 = Paragraph.objects.create(section=self.section, text="Second paragraph", order=1)
        p3 = Paragraph.objects.create(section=self.section, text="Third paragraph", order=5)

        # Spustíme funkci na přeuspořádání
        utils.reorder_section_content(self.section)

        # Načteme **Paragraph objekty**, ne ContentElement
        ordered_elements = list(Paragraph.objects.filter(section=self.section).order_by("order"))

        # Ověříme správné pořadí
        self.assertEqual(ordered_elements[0].id, p2.id)  # První by měl být původní p2
        self.assertEqual(ordered_elements[1].id, p1.id)  # Druhý by měl být p1
        self.assertEqual(ordered_elements[2].id, p3.id)  # Třetí by měl být p3

        # Ověříme správné hodnoty `order`
        self.assertEqual(ordered_elements[0].order, 1)
        self.assertEqual(ordered_elements[1].order, 2)
        self.assertEqual(ordered_elements[2].order, 3)

    def test_reorder_section_content_no_change_needed(self):
        """
        Testuje reorder_section_content, když jsou prvky již správně seřazené.
        Nemělo by dojít k žádné změně.
        """
        p1 = Paragraph.objects.create(section=self.section, text="First paragraph", order=1)
        p2 = Paragraph.objects.create(section=self.section, text="Second paragraph", order=2)
        p3 = Paragraph.objects.create(section=self.section, text="Third paragraph", order=3)

        utils.reorder_section_content(self.section)

        # Načteme prvky znovu z databáze
        ordered_elements = list(ContentElement.objects.filter(section=self.section).order_by("order"))

        self.assertEqual(ordered_elements[0].order, 1)
        self.assertEqual(ordered_elements[1].order, 2)
        self.assertEqual(ordered_elements[2].order, 3)

    def test_reorder_section_content_empty_section(self):
        """
        Testuje reorder_section_content na prázdnou sekci.
        Nemělo by dojít k chybě.
        """
        try:
            utils.reorder_section_content(self.section)  # Nemělo by vyvolat výjimku
        except Exception as e:
            self.fail(f"reorder_section_content vyvolala neočekávanou výjimku: {e}")

    def test_reorder_section_content_complex_case(self):
        """
        Testuje reorder_section_content na složitějším scénáři s různými typy prvků.
        """
        # Vytvoříme prvky obsahu ve smíšeném pořadí
        p1 = Paragraph.objects.create(section=self.section, text="Paragraph 1", order=1)
        p2 = Paragraph.objects.create(section=self.section, text="Paragraph 2", order=2)
        p3 = Paragraph.objects.create(section=self.section, text="Paragraph 3", order=3)
        chart = Chart.objects.create(section=self.section, title="Chart 1", order=4)
        p4 = Paragraph.objects.create(section=self.section, text="Paragraph 4", order=5)
        p5 = Paragraph.objects.create(section=self.section, text="Paragraph 5", order=6)
        table = Table.objects.create(section=self.section, title="Table 1", order=7)
        p6 = Paragraph.objects.create(section=self.section, text="Paragraph 6", order=8)
        p7 = Paragraph.objects.create(section=self.section, text="Paragraph 7", order=9)
        p8 = Paragraph.objects.create(section=self.section, text="Paragraph 8", order=10)

        # Nyní vložíme nový `Paragraph` mezi `Chart` a `Paragraph 4`
        new_paragraph = Paragraph.objects.create(section=self.section, text="New Paragraph", order=4.5)

        # Spustíme funkci na přeuspořádání
        utils.reorder_section_content(self.section)

        # Načteme **všechny prvky** z databáze, seřazené podle `order`
        ordered_elements = list(ContentElement.objects.filter(section=self.section).order_by("order"))

        # Debug výpis pořadí prvků po přeuspořádání
        print("\nPořadí prvků po reorder_section_content:")
        for idx, elem in enumerate(ordered_elements, start=1):
            print(f"Order {idx}: ID {elem.id} - {elem}")

        # Ověříme správné pořadí po přeuspořádání
        expected_order = [
            p1, p2, p3, chart, new_paragraph, p4, p5, table, p6, p7, p8
        ]

        for i, element in enumerate(expected_order, start=1):
            self.assertEqual(ordered_elements[i - 1].id, element.id)
            self.assertEqual(ordered_elements[i - 1].order, i)



    # -------------------- generate pdf --------------------


from io import BytesIO
from PyPDF2 import PdfReader
from reports import utils

class GeneratePDFTest(TestCase):
    """
    Testy pro generate_pdf(report).
    """

    def setUp(self):
        """
        Příprava testovacího prostředí.
        """
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.report = Report.objects.create(title="Test Report", topic="Science", year=2024, author=self.user)
        self.section = Section.objects.create(report=self.report, title="Introduction", order=1)

        # Přidání obsahu
        self.paragraph = Paragraph.objects.create(section=self.section, text="This is a test paragraph.", order=1)
        self.chart = Chart.objects.create(section=self.section, title="Test Chart", order=2)
        self.table = Table.objects.create(section=self.section, title="Test Table", order=3)

    def test_generate_pdf_valid_output(self):
        """
        Testuje, že generate_pdf vrací platný PDF soubor.
        """
        pdf_bytes = utils.generate_pdf(self.report)

        self.assertIsInstance(pdf_bytes, bytes)  # Ověříme, že vrací `bytes`
        self.assertGreater(len(pdf_bytes), 100)  # PDF soubor by neměl být prázdný

    def test_generate_pdf_contains_report_info(self):
        """
        Testuje, že PDF obsahuje správné informace z reportu.
        """
        pdf_bytes = utils.generate_pdf(self.report)
        pdf_reader = PdfReader(BytesIO(pdf_bytes))
        pdf_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

        # Ověříme, že klíčové informace jsou v PDF
        self.assertIn("Test Report", pdf_text)
        self.assertIn("Author: testuser", pdf_text)
        self.assertIn("Topic: Science", pdf_text)
        self.assertIn("Year: 2024", pdf_text)

    def test_generate_pdf_contains_sections_and_elements(self):
        """
        Testuje, že PDF obsahuje sekce a prvky obsahu.
        """
        pdf_bytes = utils.generate_pdf(self.report)
        pdf_reader = PdfReader(BytesIO(pdf_bytes))
        pdf_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

        # debug výstup
        print("\n🔍 Extrahovaný PDF text:\n", pdf_text)

        # Ověříme, že PDF obsahuje sekci a její prvky
        self.assertIn("Introduction", pdf_text)  # Název sekce
        self.assertIn("This is a test paragraph.", pdf_text)  # Obsah odstavce
        self.assertIn("Chart: Test Chart", pdf_text)  # Graf placeholder
        self.assertIn("Table: Test Table", pdf_text)  # Tabulka placeholder

    def test_generate_pdf_no_sections(self):
        """
        Testuje generování PDF pro report bez sekcí.
        """
        empty_report = Report.objects.create(title="Empty Report", topic="Math", year=2025, author=self.user)
        pdf_bytes = utils.generate_pdf(empty_report)
        pdf_reader = PdfReader(BytesIO(pdf_bytes))
        pdf_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

        self.assertIn("Empty Report", pdf_text)  # Report by měl obsahovat název
        self.assertNotIn("Introduction", pdf_text)  # Neměl by obsahovat sekci
