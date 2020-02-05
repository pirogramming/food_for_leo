from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(blank=True, upload_to="media/client/img")
    tel = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class Pet(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='pets')
    kind = models.CharField(max_length=255)
    petInfo = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
