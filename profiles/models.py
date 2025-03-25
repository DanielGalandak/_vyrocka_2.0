from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        EDITOR = 'EDITOR', 'Editor'
        WRITER = 'WRITER', 'Writer'
        READER = 'READER', 'Reader'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.READER,
    )
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    # Další pole profilu (např. oblíbené téma, kontaktní informace, atd.)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_editor(self):
        return self.role == self.Role.EDITOR

    def is_writer(self):
        return self.role == self.Role.WRITER

    def is_reader(self):
        return self.role == self.Role.READER