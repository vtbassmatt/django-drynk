import os
from setuptools import setup, find_packages

version = '0.1.2'
README = """
django-drynk gives you DRY natural keys.

Instead of defining a `natural_key` method on the Model and a `get_by_natural_key` method on the Manager, instead you add a simple decorator to your model which takes care of everything.
"""

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-drynk',
    version = version,
    description = 'django-drynk gives you DRY natural keys.',
    long_description = README,
    keywords = 'django natural_key',
    license = 'MIT License',
    author = 'Matt Cooper',
    author_email = 'vtbassmatt@gmail.com',
    url = 'http://github.com/vtbassmatt/django-drynk/',
    install_requires = ['django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_dir = {'': 'src'},
    packages = ['drynk'],
    include_package_data = True,
)

