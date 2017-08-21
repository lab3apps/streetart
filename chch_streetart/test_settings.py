from .settings import *

# make tests faster
SOUTH_TESTS_MIGRATE = False
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
    }
}