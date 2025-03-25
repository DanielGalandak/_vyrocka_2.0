# reports/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from data_sources.models import DataSource
from polymorphic.models import PolymorphicModel

User = get_user_model()

class Report(models.Model):
    class ReportStatus(models.TextChoices):
        OPEN = "OPEN", "Open"
        PUBLISHED = "PUBLISHED", "Published"

    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=100)  # Pokud je topic samostatná entita, bude to ForeignKey
    year = models.IntegerField()
    status = models.CharField(max_length=10, choices=ReportStatus.choices, default=ReportStatus.OPEN)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('reports:report_detail', kwargs={'pk': self.pk})

class Section(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"

# ----------------- model ContentElement -----------------

class ContentElement(PolymorphicModel):
    class ContentElementStatus(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        STAGED = "STAGED", "Staged"
        APPROVED = "APPROVED", "Approved"

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="content_elements")
    order = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10,
        choices=ContentElementStatus.choices,
        default=ContentElementStatus.DRAFT
    )

    class Meta:
        ordering = ["order"]

# ----------------- Konkrétní typy obsahu -----------------

class Paragraph(ContentElement):
    text = models.TextField()

    def __str__(self):
        return f"Paragraph {self.order} in {self.section.title}"

class Chart(ContentElement):
    title = models.CharField(max_length=200)
    dataset = models.FileField(upload_to="charts/")  # Dataset pro graf (např. CSV, JSON)
    data_source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Chart: {self.title} in {self.section.title}"

class Table(ContentElement):
    title = models.CharField(max_length=200)
    data = models.JSONField(null=True, blank=True)  # Uloží strukturovaná data jako JSON
    data_source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, null=True, blank=True) # Přidáno data_source

    def __str__(self):
        return f"Table: {self.title} in {self.section.title}"