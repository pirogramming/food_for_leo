from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Mall(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='malls')
    logo = models.URLField(blank=True, null=True)
    brand_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    mall = models.ForeignKey(Mall, on_delete=models.CASCADE, related_name='products')
    price = models.PositiveIntegerField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    product_url = models.URLField(blank=True, null=True)
    img_main = models.URLField(blank=True, null=True)
    img_detail = models.URLField(blank=True, null=True)
    made_in = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name