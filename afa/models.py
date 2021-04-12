from django.db import models
from djmoney.models.fields import MoneyField


class AfaYearError(Exception):
    pass


class Afa(models.Model):
    title = models.CharField(max_length=255)
    useful_life = models.PositiveIntegerField()
    source = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Entity(models.Model):
    name = models.CharField(max_length=255)
    date_of_purchase = models.DateField()
    price = MoneyField(max_digits=14, decimal_places=2, default_currency="EUR")
    afa_type = models.ForeignKey("Afa", on_delete=models.PROTECT)

    def deduction(self, year: int):
        month_of_purchase = self.date_of_purchase.month
        useful_life = self.afa_type.useful_life
        months_1st_year = 12 - month_of_purchase + 1
        months_last_year = 12 - months_1st_year
        if year < self.date_of_purchase.year:
            raise AfaYearError(
                "Deduction is only allowed in or after the year of purchase."
            )
        if (year - self.date_of_purchase.year) == 0:
            return (months_1st_year / (12 * useful_life)) * self.price
        elif (year - self.date_of_purchase.year) < useful_life:
            return 1 / useful_life * self.price
        else:
            return (months_last_year / (12 * useful_life)) * self.price

    @property
    def deduction_plan(self):
        pass
