# profiles/views.py

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import login
from .models import UserProfile

def register(request: HttpRequest) -> HttpResponse:
    """
    Zobrazí registrační formulář a zpracuje jeho odeslání.

    Pokud je požadavek typu POST a formulář je validní, uloží nového uživatele,
    automaticky ho přihlásí, zobrazí zprávu o úspěšné registraci a přesměruje
    na úvodní stránku aplikace 'reports'.  V opačném případě zobrazí prázdný
    registrační formulář.

    Args:
        request: Objekt HttpRequest reprezentující požadavek od uživatele.

    Returns:
        Objekt HttpResponse, který vykresluje registrační formulář nebo přesměrovává
        uživatele po úspěšné registraci.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            user_profile = UserProfile.objects.get(user=user)
            user_profile.role = UserProfile.Role.READER
            user_profile.save()
            
            login(request, user)  # automatické přihlášení po registraci
            messages.success(request, "Registrace byla úspěšná. Jste přihlášeni.")
            return redirect('reports:index')  # přesměrování po registraci
    else:
        form = UserRegistrationForm()

    return render(request, 'profiles/register.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profiles/profile.html', {'user': user})