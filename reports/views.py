# reports/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Report
from django.core.exceptions import ValidationError
from django.views.generic import ListView, DetailView
from .services import add_paragraph, add_chart, add_table
from django.contrib import messages
from .forms import ParagraphForm, ChartForm, TableForm
from django.contrib.auth.decorators import login_required, permission_required

def index(request):
    """
    Zobrazuje úvodní stránku s přihlašovacím formulářem a výpisem nejnovějších reportů.
    """
    if request.method == 'POST':
        if 'logout' in request.POST:
            logout(request)
            return redirect('reports:index')
        else:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('reports:index')
                else:
                    # Chybná kombinace jména a hesla
                    form.add_error(None, "Neplatné přihlašovací údaje.")
    else:
        form = AuthenticationForm()

    # Načtení nejnovějších publikovaných reportů (např. posledních 5)
    latest_reports = Report.objects.filter(status=Report.ReportStatus.PUBLISHED).order_by('-year')[:5]

    context = {
        'form': form,
        'latest_reports': latest_reports,
    }
    return render(request, 'home.html', context)

class PublishedReportListView(ListView):
    model = Report
    template_name = 'reports/published_report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.filter(status=Report.ReportStatus.PUBLISHED)


class OpenReportListView(ListView):
    model = Report
    template_name = 'reports/open_report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.exclude(status=Report.ReportStatus.PUBLISHED)
    
class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/report_detail.html'

    def get_queryset(self):
        return Report.objects.prefetch_related('sections__content_elements')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paragraph_form'] = ParagraphForm()
        context['chart_form'] = ChartForm()
        context['table_form'] = TableForm()
        return context
    
@login_required
@permission_required('reports.can_edit_report', raise_exception=True)
def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        paragraph_form = ParagraphForm(request.POST)
        chart_form = ChartForm(request.POST)
        table_form = TableForm(request.POST)
        
        if 'add_paragraph' in request.POST and paragraph_form.is_valid():
            try:
                #TODO: Získat section. Pro zjednodušení zatím použijeme první
                section = report.sections.first() #Zde by měla být logika pro výběr section
                if not section:
                    messages.error(request, "Neexistuje žádná sekce pro vložení odstavce.")
                else:
                  add_paragraph(section, paragraph_form.cleaned_data['text']) #  TODO: Přidat section
                  messages.success(request, "Odstavec přidán")
            except ValidationError as e:
                messages.error(request, e.message)
            return redirect('reports:report_detail', pk=pk)
        
        elif 'add_chart' in request.POST and chart_form.is_valid():
            try:
                section = report.sections.first()
                if not section:
                    messages.error(request, "Neexistuje žádná sekce pro vložení grafu.")
                else:
                  add_chart(section, chart_form.cleaned_data['title'], chart_form.cleaned_data.get('dataset')) #  TODO: Přidat section
                  messages.success(request, "Graf přidán")
            except ValidationError as e:
                messages.error(request, e.message)
            return redirect('reports:report_detail', pk=pk)

        elif 'add_table' in request.POST:
            try:
                section = report.sections.first()
                if not section:
                    messages.error(request, "Neexistuje žádná sekce pro vložení tabulky.")
                else:
                  add_table(section, table_form.cleaned_data['title']) #  TODO: Přidat section
                  messages.success(request, "Tabulka přidána")
            except ValidationError as e:
                messages.error(request, e.message)
            return redirect('reports:report_detail', pk=pk)

    context = {
        'report': report,
        'paragraph_form': ParagraphForm(),
        'chart_form': ChartForm(),
        'table_form': TableForm(),
    }
    return render(request, 'reports/report_detail.html', context)