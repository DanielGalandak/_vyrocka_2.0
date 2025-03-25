# reports/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Report
from django.views.generic import ListView

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

def logout_view(request):
    logout(request)
    return redirect('index')

