import unittest
from decimal import Decimal
from django.db import models
from drynk import with_natural_key


class SanityTests(unittest.TestCase):

    def test_base_behavior(self):
        """
        Sanity test to make sure nothing broke just by importing.
        """
        self.assertTrue(True)
