import unittest
from django.db import models
from drynk import with_natural_key


class SanityTests(unittest.TestCase):

    def test_reality(self):
        """
        Make sure nothing broke just by importing.
        """
        self.assertTrue(True)

    def test_single(self):
        """
        One field natural key.
        """
        @with_natural_key(["name"])
        class Widget(models.Model):
            name = models.CharField(max_length=50, unique=True)

            class Meta:
                app_label = "drynk"

        widget1 = Widget(name="Widget 1")
        widget2 = Widget(name="Widget 2")

        self.assertEqual(widget1.natural_key(), ('Widget 1', ))
        self.assertEqual(widget2.natural_key(), ('Widget 2', ))

    def test_two(self):
        """
        Two field natural key.
        """
        @with_natural_key(["name", "size"])
        class Widget(models.Model):
            name = models.CharField(max_length=50, unique=True)
            size = models.IntegerField()

            class Meta:
                app_label = "drynk"

        widget1 = Widget(name="Widget 1", size=5)
        widget2 = Widget(name="Widget 2", size=10)

        self.assertEqual(widget1.natural_key(), ('Widget 1', 5))
        self.assertEqual(widget2.natural_key(), ('Widget 2', 10))

    def test_two(self):
        """
        Three field natural key.
        """
        @with_natural_key(["name", "size", "stocked"])
        class Widget(models.Model):
            name = models.CharField(max_length=50, unique=True)
            size = models.IntegerField()
            stocked = models.BooleanField(default=False)

            class Meta:
                app_label = "drynk"

        widget1 = Widget(name="Widget 1", size=5, stocked=False)
        widget2 = Widget(name="Widget 2", size=10, stocked=True)

        self.assertEqual(widget1.natural_key(), ('Widget 1', 5, False))
        self.assertEqual(widget2.natural_key(), ('Widget 2', 10, True))
