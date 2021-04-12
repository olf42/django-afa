from datetime import date
from django.test import TestCase
from afa.models import Afa, Entity, AfaYearError
from afa.afa2json import Afa2Json
from djmoney.money import Money

BIERZELT_ID = "Zelte, Bier- "
BIERZELT_NAME = "Unser Bierzelt"


class AfaCreateCase(TestCase):
    """
    Tests the initial data fetching and object creation.
    """

    @classmethod
    def setUpTestData(cls):
        for entry in Afa2Json.from_url().data:
            if not entry["useful_life"]:
                entry["useful_life"] = 0
            a = Afa.objects.create(
                title=entry["title"],
                useful_life=entry["useful_life"],
                source=entry["source"],
            )
            a.save()

    def test_entity_creation(self):
        bierzelt_type = Afa.objects.get(title=BIERZELT_ID)
        ub = Entity.objects.create(
            name=BIERZELT_NAME,
            price=Money(9600.00, "EUR"),
            date_of_purchase=date(year=2021, month=4, day=21),
            afa_type=bierzelt_type,
        )
        ub.save()


class AfaUseCase(TestCase):
    """
    Tests if the cool calculates correctly.
    """

    @classmethod
    def setUpTestData(cls):
        for entry in Afa2Json.from_url().data:
            if not entry["useful_life"]:
                entry["useful_life"] = 0
            a = Afa.objects.create(
                title=entry["title"],
                useful_life=entry["useful_life"],
                source=entry["source"],
            )
            a.save()
        bierzelt_type = Afa.objects.get(title=BIERZELT_ID)
        ub = Entity.objects.create(
            name=BIERZELT_NAME,
            price=Money(9600.00, "EUR"),
            date_of_purchase=date(year=2021, month=4, day=21),
            afa_type=bierzelt_type,
        )
        ub.save()

    def test_deduction_raises(self):
        nb = Entity.objects.get(name=BIERZELT_NAME)
        self.assertRaises(AfaYearError, nb.deduction, 2020)

    def test_deduction_first_year(self):
        nb = Entity.objects.get(name=BIERZELT_NAME)
        self.assertEqual(nb.deduction(2021), Money(900.00, "EUR"))

    def test_deduction_inbetween_year(self):
        nb = Entity.objects.get(name=BIERZELT_NAME)
        for year in range(2022, 2029):
            self.assertEqual(nb.deduction(year), Money(1200.00, "EUR"))

    def test_deduction_last_year(self):
        nb = Entity.objects.get(name=BIERZELT_NAME)
        self.assertEqual(nb.deduction(2029), Money(300.00, "EUR"))
