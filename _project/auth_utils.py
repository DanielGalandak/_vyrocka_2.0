# _project/auth_utils.py

from profiles.models import UserProfile

def get_roles_with_publish_permission():
    """
    Vrací seznam rolí, které mají oprávnění publikovat reporty.
    """
    return [UserProfile.Role.ADMIN]

def get_roles_with_approve_permission():
    """
    Vrací seznam rolí, které mají oprávnění schvalovat reporty.
    """
    return [UserProfile.Role.ADMIN, UserProfile.Role.EDITOR]

# A tak dále pro další akce...