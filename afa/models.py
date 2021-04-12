from django.db import models
from djmoney.models.fields import MoneyField


class Afa(models.Model):
    title = models.CharField(max_length=255)
    useful_life = models.PositiveIntegerField()
    source = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Entity(models.Model):
    name = models.CharField(max_length=255)
    date_of_purchase = models.DateField()
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    afa_type = models.ForeignKey("Afa", on_delete=models.PROTECT)
