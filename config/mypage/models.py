from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    img = models.ImageField(blank=True, null=True, upload_to="media/user_profile/img")
    tel = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Pet(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='pet', blank=True, null=True)
    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=255)
    img = img = models.ImageField(blank=True, null=True, upload_to="media/user_pet/img")
    petInfo = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Diary(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='diary', blank=True, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    img = models.ImageField(blank=True, null=True, upload_to="media/user_diary/img")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
