# profiles/utils.py

from .models import UserProfile

def get_all_roles():
    """
    Vrací list všech definovaných rolí v UserProfile.Role.
    """
    return [choice[0] for choice in UserProfile.Role.choices]