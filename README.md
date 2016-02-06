[![PyPI](https://img.shields.io/pypi/v/django-drynk.svg)](https://pypi.python.org/pypi/django-drynk)

Introduction
------------

DRYNK: for DRY Natural Keys.
To use [Django natural keys](https://docs.djangoproject.com/en/1.9/topics/serialization/#natural-keys), you end up repeating yourself.
You have to define a `natural_key` method on the Model and a `get_by_natural_key` method on the Manager, but they both contain the same fields!
With DRYNK, instead you add a single decorator to your model which takes care of everything.

The old way:

    class Thing(models.Model):
    	name = models.CharField(max_length=5, unique=True)
    	some_data = models.IntegerField()
    	
    	objects = models.Manager()
    	objects.get_by_natural_key = lambda self, x: return self.get(name=x)
    	
    	def natural_key(self):
    		return self.name

But you've got DRYNK:

	@with_natural_key(["name"])
    class Thing(models.Model):
    	name = models.CharField(max_length=50, unique=True)
    	some_data = models.IntegerField()


Requirements and Installation
-----------------------------

The project has no dependencies outside of Django itself.
It works with Python 3.4 / 3.5; other versions being tested soon.

* `pip install django-drynk`
* Add `drynk` to your `INSTALLED_APPS` (maybe - checking that).


Use
---

	from django.db import models
	from drynk import with_natural_key

	@with_natural_key(["name"])
    class Thing(models.Model):
    	name = models.CharField(max_length=50, unique=True)
    	some_data = models.IntegerField()

Also works with fields that are foreign keys, so long as those foreign objects also have a natural key.

	from django.db import models
	from drynk import with_natural_key

	@with_natural_key(["name"])
    class Kind(models.Model):
    	name = models.CharField(max_length=10, unique=True)

	@with_natural_key(["name", "kind"])
    class Thing(models.Model):
    	name = models.CharField(max_length=50)
    	kind = models.ForeignKey(Kind)


Tests
-----

`./run-tests.sh`.


Limitations
-----------

* Is opinionated: Believes it should be the default Manager and be called `object`.
* Probably breaks if you've already specified a manager, even by another name, on the model class.


Contributions
-------------

I built this little project to satisfy a personal need, but thought it might be useful enough for others.
If you have contributions, please don't hesitate to send a PR.
Let's keep the tests passing and all will be well.
My personal stack is currently Django 1.9 on Python 3.4, so that will be the most-tested.
I will eventually set Travis up to cover Django 1.7, 1.8, and 1.9 on Python 2.7, 3.3-3.5, and nightly.
