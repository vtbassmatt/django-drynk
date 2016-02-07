from django.test import TestCase

from drynk import with_natural_key
from drynk.tests.models import (
    TestModel1,
    TestModel2,
    TestModel3,
    Category1,
    Widget1,
    Category2,
    Widget2,
    SubWidget)


class SanityTests(TestCase):

    def test_reality(self):
        """
        Make sure nothing broke just by importing.
        """
        self.assertTrue(True)


class NaturalKeyTests(TestCase):

    def test_single(self):
        """
        One field natural key.
        """
        tm1 = TestModel1(name="Widget 1")
        tm2 = TestModel1(name="Widget 2")

        self.assertEqual(tm1.natural_key(), ('Widget 1', ))
        self.assertEqual(tm2.natural_key(), ('Widget 2', ))

    def test_two(self):
        """
        Two field natural key.
        """
        tm1 = TestModel2(name="Widget 1", size=5)
        tm2 = TestModel2(name="Widget 2", size=10)

        self.assertEqual(tm1.natural_key(), ('Widget 1', 5))
        self.assertEqual(tm2.natural_key(), ('Widget 2', 10))

    def test_three(self):
        """
        Three field natural key.
        """
        tm1 = TestModel3(name="Widget 1", size=5, stocked=False)
        tm2 = TestModel3(name="Widget 2", size=10, stocked=True)

        self.assertEqual(tm1.natural_key(), ('Widget 1', 5, False))
        self.assertEqual(tm2.natural_key(), ('Widget 2', 10, True))

    def test_foreign(self):
        """
        Natural key spanning a foreign relationship
        """
        cat1 = Category1(title="Category 1")
        cat2 = Category1(title="Category 2")
        widget1 = Widget1(name="Widget X", category=cat1)
        widget2 = Widget1(name="Widget X", category=cat2)
        widget3 = Widget1(name="Widget Y", category=cat1)

        self.assertEqual(widget1.natural_key(), ('Widget X', 'Category 1'))
        self.assertEqual(widget2.natural_key(), ('Widget X', 'Category 2'))
        self.assertEqual(widget3.natural_key(), ('Widget Y', 'Category 1'))

    def test_foreign_multiple(self):
        """
        Natural key spanning a foreign relationship (two fields)
        """
        cat1 = Category2(size=1, color="red")
        cat2 = Category2(size=1, color="blue")
        cat3 = Category2(size=5, color="blue")
        widget1 = Widget2(name="Widget X", category=cat1)
        widget2 = Widget2(name="Widget X", category=cat2)
        widget3 = Widget2(name="Widget X", category=cat3)

        self.assertEqual(widget1.natural_key(), ('Widget X', 1, 'red'))
        self.assertEqual(widget2.natural_key(), ('Widget X', 1, 'blue'))
        self.assertEqual(widget3.natural_key(), ('Widget X', 5, 'blue'))

    def test_foreign_foreign(self):
        """
        Natural key spanning two foreign relationships
        """
        cat1 = Category1(title="Category")
        widget1 = Widget1(name="Widget X", category=cat1)
        widget2 = Widget1(name="Widget Y", category=cat1)
        sub1 = SubWidget(name="Sub A", widget=widget1)
        sub2 = SubWidget(name="Sub A", widget=widget2)
        sub3 = SubWidget(name="Sub B", widget=widget2)

        self.assertEqual(sub1.natural_key(), ('Sub A', 'Widget X', 'Category'))
        self.assertEqual(sub2.natural_key(), ('Sub A', 'Widget Y', 'Category'))
        self.assertEqual(sub3.natural_key(), ('Sub B', 'Widget Y', 'Category'))


class ManagerTests(TestCase):

    def test_basic(self):
        """
        Lookup by one-field natural key.
        """
        tm1 = TestModel1.objects.create(name="Widget 1")
        tm2 = TestModel1.objects.create(name="Widget 2")

        self.assertEqual(TestModel1.objects.get_by_natural_key('Widget 1'), tm1)
        self.assertEqual(TestModel1.objects.get_by_natural_key('Widget 2'), tm2)
        with self.assertRaises(TestModel1.DoesNotExist):
            TestModel1.objects.get_by_natural_key('Widget X')

    def test_two(self):
        """
        Lookup by two-field natural key.
        """
        tm1 = TestModel2.objects.create(name="Widget 1", size=5)
        tm2 = TestModel2.objects.create(name="Widget 2", size=10)

        self.assertEqual(TestModel2.objects.get_by_natural_key('Widget 1', 5), tm1)
        self.assertEqual(TestModel2.objects.get_by_natural_key('Widget 2', 10), tm2)
        with self.assertRaises(TestModel2.DoesNotExist):
            TestModel2.objects.get_by_natural_key('Widget 1', 10)

    def test_foreign(self):
        """
        Lookup by a key spanning a foreign relationship
        """
        cat1 = Category1.objects.create(title="Category 1")
        cat2 = Category1.objects.create(title="Category 2")
        widget1 = Widget1.objects.create(name="Widget X", category=cat1)
        widget2 = Widget1.objects.create(name="Widget X", category=cat2)
        widget3 = Widget1.objects.create(name="Widget Y", category=cat1)

        self.assertEqual(Widget1.objects.get_by_natural_key('Widget X', 'Category 1'), widget1)
        self.assertEqual(Widget1.objects.get_by_natural_key('Widget X', 'Category 2'), widget2)
        self.assertEqual(Widget1.objects.get_by_natural_key('Widget Y', 'Category 1'), widget3)
        with self.assertRaises(Widget1.DoesNotExist):
            Widget1.objects.get_by_natural_key('Widget Y', 'Category 2')
