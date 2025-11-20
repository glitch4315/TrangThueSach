from djongo import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    _id = models.ObjectIdField(primary_key=True)

def avatar_upload_path(instance, filename):
    return f'avatars/{instance.user.username}/{filename}'

class Profile(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
