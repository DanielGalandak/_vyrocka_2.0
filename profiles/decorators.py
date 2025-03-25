# profiles/decorators.py
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def role_required(roles):
    """
    Dekorátor, který vyžaduje, aby uživatel měl alespoň jednu z požadovaných rolí.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')  # Přesměrování na přihlášení
            if not hasattr(request.user, 'profile'):
                raise PermissionDenied("Uživatel nemá profil.")

            if request.user.profile.role not in roles:
                raise PermissionDenied("Nemáte oprávnění k zobrazení této stránky.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator