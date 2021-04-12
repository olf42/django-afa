from django.test import TestCase

from afa.models import Afa
from afa.afa2json import Afa2Json


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

    def test_something(self):
        self.assertTrue(True)
