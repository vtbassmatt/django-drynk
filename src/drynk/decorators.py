"""
Decorators for Django models
"""
from functools import reduce
from inspect import signature, Parameter

from django.core.exceptions import ImproperlyConfigured
from django.db import models


def with_natural_key(fields):
    """
    Decorator to add DRY natural key support to a Django model.

    Adds a Manager class with get_by_natural_key and a corresponding natural_key
    method on the model.
    """
    assert len(fields) > 0
    assert 'self' not in fields # for NaturalKeyManager

    def natural_key_wrapper(klass):
        def _natural_key_field(self, field_name):
            if isinstance(self._meta.get_field(field_name), models.fields.related.ForeignKey):
                real_field = getattr(self, self._meta.get_field(field_name).name)
                if getattr(real_field, 'natural_key', None):
                    return real_field.natural_key()
                else:
                    # if the foreign model can't provide a natural key, then the
                    # auto-generated get_by_natural_key won't work
                    raise ImproperlyConfigured("expected to find a `natural_key` method "
                                               "on {}".format(field_name))
            return (self.__dict__[field_name], )

        def _natural_key(self):
            return reduce(lambda x, y: x + y, [self._natural_key_field(x) for x in fields])

        klass._natural_key_field = _natural_key_field
        klass.natural_key = _natural_key
        klass.natural_key.__name__ = "natural_key"
        klass.natural_key.__doc__ = "Return a natural key for the model: ({})".format(
            ", ".join(fields))

        # determine and record dependencies
        # also, unroll dependencies and read their get_by_natural_key signatures
        dependencies = []
        unrolled_fields = []

        for field_name in fields:
            if isinstance(klass._meta.get_field(field_name), models.fields.related.ForeignKey):
                to_model = klass._meta.get_field(field_name).remote_field.to
                dependencies.append(_build_dependency(to_model, field_name))
                unrolled_fields.extend(_unroll_natural_key(to_model, field_name))
            else:
                unrolled_fields.append(field_name)

        if len(dependencies) > 0:
            klass.natural_key.dependencies = dependencies


        class NaturalKeyManager(models.Manager):
            """
            Implements get_by_natural_key for {}
            """
            def get_by_natural_key(self, *args):
                """
                Find an object by its natural key
                """
                if len(args) != len(unrolled_fields):
                    raise RuntimeError("expected {} arguments ({}), got {}".format(
                        len(unrolled_fields), ", ".join(unrolled_fields), len(args)
                    ))

                return self.get(**dict(zip(unrolled_fields, args)))

        NaturalKeyManager.__name__ = klass.__name__ + "NaturalKeyManager"
        NaturalKeyManager.__doc__ = NaturalKeyManager.__doc__.format(klass.__name__)

        # fix up the signature to show the expected positional parameters instead of "*args"
        # this cleans up help() but also allows later models to use this in constructing
        # their get_by_natural_key method
        sig = signature(NaturalKeyManager.get_by_natural_key)
        sig = sig.replace(parameters=[Parameter(f, Parameter.POSITIONAL_ONLY) for f in ['self'] + unrolled_fields])
        setattr(NaturalKeyManager.get_by_natural_key, "__signature__", sig)

        _m = NaturalKeyManager()
        # opinionated choice here: this should be the default manager and be called `objects`
        _m.contribute_to_class(klass, "objects")

        return klass

    return natural_key_wrapper


def _build_dependency(model, field_name):
    app_name = model._meta.app_config.label
    model_name = model.__name__
    return "{}.{}".format(app_name, model_name)


def _unroll_natural_key(model, field_name):
    try:
        foreign_gbnk = model.objects.get_by_natural_key
    except AttributeError as e:
        raise ImproperlyConfigured("expected to find a manager called "
                                   "`objects` with a `get_by_natural_key` method") from e
    sig = signature(foreign_gbnk)
    return ["{}__{}".format(field_name, k) for k,v in sig.parameters.items()]
