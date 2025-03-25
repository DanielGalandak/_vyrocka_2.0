from django.contrib import admin
from .models import Report, Section, Paragraph, Chart, Table

# -- inlines ---
class ParagraphInline(admin.TabularInline):
    model = Paragraph
    extra = 0

class ChartInline(admin.TabularInline):
    model = Chart
    extra = 0

class TableInline(admin.TabularInline):
    model = Table
    extra = 0

# -- Report admin --
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'year')
    ordering = ('year',)

# -- Section admin s inline editací obsahu --
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'report', 'order')
    list_filter = ('report',)
    ordering = ('report', 'order')
    inlines = [ParagraphInline, ChartInline, TableInline]

# Paragraph Admin
class ParagraphAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'get_report', 'section', 'order')
    ordering = ('section__report', 'section', 'order')

    @admin.display(description='Report')
    def get_report(self, obj):
        return obj.section.report.title

    @admin.display(description='Text')
    def short_text(self, obj):
        return (obj.text[:50] + '...') if len(obj.text) > 50 else obj.text

# podobně Chart a Table admin...
class ChartAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'get_report', 'order')
    ordering = ('section__report', 'section', 'order')

    @admin.display(description='Report')
    def get_report(self, obj):
        return obj.section.report.title

class TableAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'get_report', 'order')
    ordering = ('section__report', 'section', 'order')

    @admin.display(description='Report')
    def get_report(self, obj):
        return obj.section.report.title

# --- Registrace modelů ---
admin.site.register(Report, ReportAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Paragraph, ParagraphAdmin)
admin.site.register(Chart, ChartAdmin)
admin.site.register(Table, TableAdmin)
