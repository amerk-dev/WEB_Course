from django.db import models

# Create your models here.
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Watch(models.Model):
    TYPE_CHOICES = [
        ('ANALOG', 'Analog'),
        ('DIGITAL', 'Digital'),
        ('SMART', 'Smart'),
    ]

    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    watch_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    image = models.ImageField(
        upload_to='watches/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    in_stock = models.BooleanField(default=True)