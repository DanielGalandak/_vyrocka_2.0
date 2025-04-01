# reports/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Report, Section, Paragraph
from django.core.exceptions import ValidationError
from django.views.generic import ListView, DetailView, UpdateView
from .services import add_paragraph, add_chart, add_table
from django.contrib import messages
from .models import Paragraph
from .forms import ParagraphForm, ChartForm, TableForm
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from . import repositories
from . import utils
from .services import add_paragraph
from django.db import transaction

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
    latest_reports = Report.objects.filter(status=Report.ReportStatus.OPEN).order_by('-year')[:5]

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
    
# class ReportDetailView(DetailView):
#     model = Report
#     template_name = 'reports/report_detail.html'

#     def get_queryset(self):
#         return Report.objects.prefetch_related('sections__content_elements')
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['paragraph_form'] = ParagraphForm()
#         context['chart_form'] = ChartForm()
#         context['table_form'] = TableForm()
#         return context

# class ReportDetailView(DetailView):
#     model = Report
#     template_name = 'reports/report_detail.html'

#     def get_queryset(self):
#         return Report.objects.prefetch_related('sections__content_elements')
    
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()  # Načteme report pro použití v get_context_data
#         if 'add_paragraph' in request.POST:
#             section_id = request.POST.get('section_id') # Získáme ID sekce z POST dat
#             section = get_object_or_404(Section, pk=section_id) # Načteme sekci
#             try:
#                 repositories.create_paragraph(section=section, text="Zadejte text odstavce")  # Vytvoříme nový odstavec s placeholderem
#                 messages.success(request, "Odstavec byl úspěšně přidán.")
#             except Exception as e:
#                 messages.error(request, f"Chyba při přidávání odstavce: {e}")
#             return redirect('reports:report_detail', pk=self.object.pk)
#         else:
#             return super().post(request, *args, **kwargs)  # Jiné POST požadavky (např. editace)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['paragraph_form'] = ParagraphForm()
#         context['chart_form'] = ChartForm()
#         context['table_form'] = TableForm()
#         return context


class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/report_detail.html'

    def get_queryset(self):
        return Report.objects.prefetch_related('sections__content_elements')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Načteme report pro použití v get_context_data

        if 'add_paragraph' in request.POST:
            return self.handle_add_paragraph(request)
        elif 'move_paragraph_up' in request.POST:
            return self.handle_move_paragraph(request, direction='up')
        elif 'move_paragraph_down' in request.POST:
            return self.handle_move_paragraph(request, direction='down')
        else:
            return super().post(request, *args, **kwargs)  # Jiné POST požadavky (např. editace)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paragraph_form'] = ParagraphForm()
        context['chart_form'] = ChartForm()
        context['table_form'] = TableForm()
        return context

    def handle_add_paragraph(self, request):
        section_id = request.POST.get('section_id')  # Získáme ID sekce z POST dat
        section = get_object_or_404(Section, pk=section_id)  # Načteme sekci
        try:
            add_paragraph(section=section, text="Zadejte text odstavce")  # Vytvoříme nový odstavec pomocí servisní funkce
            messages.success(request, "Odstavec byl úspěšně přidán.")
        except Exception as e:
            messages.error(request, f"Chyba při přidávání odstavce: {e}")
        return redirect('reports:report_detail', pk=self.object.pk)

    def handle_move_paragraph(self, request, direction):
        paragraph_id = request.POST.get('paragraph_id')
        paragraph = get_object_or_404(Paragraph, pk=paragraph_id)
        section = paragraph.section

        # Získat všechny odstavce v sekci, seřazené podle 'order'
        paragraphs = list(Paragraph.objects.filter(section=section).order_by('order'))

        # Najít index přesouvaného odstavce
        try:
            index = paragraphs.index(paragraph)
        except ValueError:
            messages.error(request, "Odstavec nenalezen v sekci.")
            return redirect('reports:report_detail', pk=self.object.pk)

        # Určit nový index a cílový odstavec
        if direction == 'up':
            new_index = index - 1
        elif direction == 'down':
            new_index = index + 1
        else:
            messages.error(request, "Neplatný směr přesunu.")
            return redirect('reports:report_detail', pk=self.object.pk)

        # Kontrola mezí
        if new_index < 0 or new_index >= len(paragraphs):
            messages.info(request, "Odstavec nelze přesunout dál.")
            return redirect('reports:report_detail', pk=self.object.pk)

        # Prohodit 'order' hodnoty odstavců v paměti
        target_paragraph = paragraphs[new_index]
        current_order = paragraph.order
        paragraph.order = target_paragraph.order
        target_paragraph.order = current_order

        with transaction.atomic():
            paragraph.save()
            target_paragraph.save()

        utils.reorder_section_content(section)

        messages.success(request, "Odstavec byl úspěšně přesunut.")
        return redirect('reports:report_detail', pk=self.object.pk)

@method_decorator(login_required, name='dispatch') #  Zabezpečí, že se do view dostane pouze přihlášený uživatel
class ReportEditView(UpdateView):
    model = Report
    template_name = 'reports/report_form.html'
    fields = ['title', 'topic', 'year'] #  Zde uveď, která pole chceš mít editovatelná
    success_url = reverse_lazy('reports:index')  # Po úspěšném uložení se přesměruje na index

    def get_queryset(self):
        # Omezí přístup pouze na autory reportu (a adminy, pokud je to potřeba)
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

@method_decorator(login_required, name='dispatch')
class ParagraphUpdateView(UpdateView):
    model = Paragraph
    form_class = ParagraphForm  #  Používáš ParagraphForm
    template_name = 'reports/paragraph_form.html'
    #  Potřebuješ definovat success_url.  Bude to report_detail
    #  s ID reportu
    #  (jak získat report_id?  -- Třeba z URL, nebo z  Paragraph)
    def get_success_url(self):
        return reverse_lazy('reports:report_detail', kwargs={'pk': self.object.section.report.pk}) # report.pk získáš z instance Paragraph