# Register your models here.
# profiles/admin.py
from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile)
