from django.db import models


class Blog(models.Model):
    text = models.TextField()


class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(blank=True, upload_to="media/logo")

    def __str__(self):
        return self.name


class Mall(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='mall')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    mall = models.ForeignKey(Mall, on_delete=models.CASCADE, related_name='product')
    price = models.PositiveIntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name

