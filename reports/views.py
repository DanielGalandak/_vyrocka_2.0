# reports/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Report, Section, Paragraph
from django.core.exceptions import ValidationError
from django.views.generic import ListView, DetailView, UpdateView
from .services import add_paragraph, add_chart, add_table
from django.contrib import messages
from .models import Paragraph, Chart, Table, ContentElement
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

@method_decorator(login_required, name='dispatch')
class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/report_detail.html'

    def get_queryset(self):
        return Report.objects.prefetch_related('sections__content_elements')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        actions = {
            'add_paragraph': lambda req: self.handle_add_element(req, 'Paragraph'),
            'add_chart': lambda req: self.handle_add_element(req, 'Chart'),
            'move_element_up': lambda req: self.handle_move_element(req, 'up'),
            'move_element_down': lambda req: self.handle_move_element(req, 'down'),
        }

        for action, handler in actions.items():
            if action in request.POST:
                return handler(request)

        return redirect('reports:report_detail', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'paragraph_form': ParagraphForm(),
            'chart_form': ChartForm(),
            'table_form': TableForm(),
        })
        return context

    def handle_add_element(self, request, element_type):
        section_id = request.POST.get('section_id')
        section = get_object_or_404(Section, pk=section_id)

        try:
            if element_type == 'Paragraph':
                add_paragraph(section=section, text="Zadejte text odstavce", author=request.user)
                messages.success(request, "Odstavec byl úspěšně přidán.")
            elif element_type == 'Chart':
                add_chart(section=section, title="Nový graf",author=request.user)
                messages.success(request, "Graf byl úspěšně přidán.")
            # Další typy (např. Table) lze snadno přidat sem
        except Exception as e:
            messages.error(request, f"Chyba při přidávání prvku ({element_type}): {e}")

        return redirect('reports:report_detail', pk=self.object.pk)

    def handle_move_element(self, request, direction):
        element_id = request.POST.get('element_id')
        element_base = get_object_or_404(ContentElement, pk=request.POST.get('element_id'))

        # Rozpoznání podle reálné instance
        if isinstance(element_base, Paragraph):
            element = element_base
        elif isinstance(element_base, Chart):
            element = element_base
        elif isinstance(element_base, Table):
            element = element_base
        else:
            messages.error(request, "Neznámý typ prvku.")
            return redirect('reports:report_detail', pk=self.object.pk)

        elements = list(ContentElement.objects.filter(section=element.section).order_by('order'))

        try:
            index = elements.index(element)
            new_index = index - 1 if direction == 'up' else index + 1
            if not (0 <= new_index < len(elements)):
                raise IndexError
            target = elements[new_index]
        except (ValueError, IndexError):
            messages.info(request, "Prvek nelze přesunout.")
            return redirect('reports:report_detail', pk=self.object.pk)

        element.order, target.order = target.order, element.order

        with transaction.atomic():
            element.save()
            target.save()

        utils.reorder_section_content(element.section)
        messages.success(request, "Prvek byl úspěšně přesunut.")
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

@method_decorator(login_required, name='dispatch')
class ChartUpdateView(UpdateView):
    model = Chart
    form_class = ChartForm
    template_name = 'reports/chart_form.html'

    def form_valid(self, form):
        chart = form.save(commit=False)

        # vykresli graf jako PNG a ulož ho
        data_x = [x.strip() for x in form.cleaned_data['data_x'].split(',')]
        data_y = [float(y.strip()) for y in form.cleaned_data['data_y'].split(',')]
        color = form.cleaned_data['color']
        chart_type = form.cleaned_data['chart_type']

        from .utils import render_chart_image
        chart.dataset = render_chart_image(chart.title, chart_type, data_x, data_y, color)
        chart.save()

        messages.success(self.request, "Graf byl úspěšně upraven.")
        return redirect('reports:report_detail', pk=chart.section.report.pk)

