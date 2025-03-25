from django.db import models

class DataSource(models.Model):
    class SourceType(models.TextChoices):
        CSV = "CSV", "CSV File"
        JSON = "JSON", "JSON File"
        EXCEL = "EXCEL", "Excel File"
        API = "API", "API Endpoint"

    name = models.CharField(max_length=200)
    source_type = models.CharField(max_length=10, choices=SourceType.choices)
    file = models.FileField(upload_to="data_sources/", null=True, blank=True)
    api_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class Data(models.Model):
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name="data_entries")
    content = models.JSONField()  # Uložená data jako JSON

    def __str__(self):
        return f"Data for {self.data_source.name}"

