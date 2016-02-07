"""
Models for testing DRYNK
"""
from django.db import models

from drynk import with_natural_key


@with_natural_key(["name"])
class TestModel1(models.Model):
    name = models.CharField(max_length=50)


@with_natural_key(["name", "size"])
class TestModel2(models.Model):
    name = models.CharField(max_length=50)
    size = models.IntegerField()


@with_natural_key(["name", "size", "stocked"])
class TestModel3(models.Model):
    name = models.CharField(max_length=50)
    size = models.IntegerField()
    stocked = models.BooleanField(default=False)


@with_natural_key(["title"])
class Category1(models.Model):
    title = models.CharField(max_length=50)


@with_natural_key(["name", "category"])
class Widget1(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category1)


@with_natural_key(["name", "widget"])
class SubWidget(models.Model):
    name = models.CharField(max_length=50)
    widget = models.ForeignKey(Widget1)


@with_natural_key(["size", "color"])
class Category2(models.Model):
    size = models.IntegerField()
    color = models.CharField(max_length=50)


@with_natural_key(["name", "category"])
class Widget2(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category2)
