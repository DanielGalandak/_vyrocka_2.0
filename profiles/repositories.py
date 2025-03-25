from .models import UserProfile

def get_user_profile_by_user_id(user_id):
    return UserProfile.objects.select_related('user').get(user__id=user_id)

def create_user_profile(user, **fields):
    profile = UserProfile.objects.create(user=user, **fields)
    return profile

def update_user_profile(user_profile, **fields):
    for key, value in fields.items():
        setattr(user_profile, key, value)
    user_profile.save()
    return user_profile
