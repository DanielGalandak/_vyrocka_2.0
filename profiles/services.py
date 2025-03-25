# profiles/services.py

from .repositories import create_user_profile, update_user_profile

def create_user_profile_service(user, data):
    profile_fields = {
        "role": data.get("role", "READER"),
        "bio": data.get("bio", ""),
        "profile_picture": data.get("profile_picture", None),
    }
    return create_user_profile(user, **profile_fields)

def update_user_profile_service(user_profile, data):
    profile_fields = {key: data[key] for key in ["role", "bio", "profile_picture"] if key in data}
    return update_user_profile(user_profile, **profile_fields)

# -------------- Autentization and autorization ----------------------

# profiles/services.py
from django.core.exceptions import PermissionDenied
from .models import UserProfile

def can_edit_report(user, report):
    """
    Ověří, zda má uživatel oprávnění editovat report.
    Oprávnění mají administrátoři a autoři reportu (pokud report není publikovaný).
    """
    if user.profile.role == UserProfile.Role.ADMIN:
        return True
    if user == report.author and report.status not in [UserProfile.ReportStatus.PUBLISHED]:
        return True
    return False

def can_approve_report(user, report):
    """
    Ověří, zda má uživatel oprávnění schválit report.
    Oprávnění mají pouze editoři a administrátoři.
    """
    return user.profile.role in [UserProfile.Role.EDITOR, UserProfile.Role.ADMIN]

def can_publish_report(user, report):
    """
    Ověří, zda má uživatel oprávnění publikovat report.
    Oprávnění mají pouze administrátoři.
    """
    return user.profile.role == UserProfile.Role.ADMIN

def can_delete_report(user, report):
    """
    Ověří, zda má uživatel oprávnění smazat report.
    Oprávnění mají pouze administrátoři.
    """
    return user.profile.role == UserProfile.Role.ADMIN

# Další funkce pro kontrolu oprávnění k dalším akcím (vytváření sekcí, editaci obsahu, atd.)
