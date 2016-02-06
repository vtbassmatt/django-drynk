from pkg_resources import get_distribution, DistributionNotFound

try:
    _dist = get_distribution('django-drynk')
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version
VERSION = __version__

from .decorators import with_natural_key
