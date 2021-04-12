from django.db import models


class Afa(models.Model):
    title = models.CharField(max_length=255)
    useful_life = models.PositiveIntegerField()
    source = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Entity(models.Model):
    name = models.CharField(max_length=255)
    date_of_purchase = models.DateField()
    afa_type = models.ForeignKey("Afa", on_delete=models.PROTECT)
