SECRET_KEY = 'tests'
INSTALLED_APPS = [
    "drynk",
    "drynk.tests",
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'drynk.sqlite3',
    }
}
