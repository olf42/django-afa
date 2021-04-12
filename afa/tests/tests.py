from datetime import date
from django.test import TestCase
from afa.models import Afa, Entity
from afa.afa2json import Afa2Json
from djmoney.money import Money

BIERZELT_ID = 'Zelte, Bier- '

class AfaTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        for entry in Afa2Json.from_url().data:
            if not entry["useful_life"]:
                entry["useful_life"] = 0
            a = Afa.objects.create(
                title=entry["title"],
                useful_life=entry["useful_life"],
                source=entry["source"]
            )
            a.save()

    def test_entity_creation(self):
        bierzelt_type = Afa.objects.get(title=BIERZELT_ID)
        e = Entity.objects.create(
            name="Unser Bierzelt",
            price=Money(12345.67, "EUR"),
            date_of_purchase=date(year=2021, month=4, day=21),
            afa_type=bierzelt_type
        )
        e.save()
