from .base import *  # noqa: F403

DEBUG = False
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB", default="nexor_test"),  # noqa: F405
        "USER": config("POSTGRES_USER", default="nexor"),  # noqa: F405
        "PASSWORD": config("POSTGRES_PASSWORD", default="nexor_dev_password"),  # noqa: F405
        "HOST": config("POSTGRES_HOST", default="localhost"),  # noqa: F405
        "PORT": config("POSTGRES_PORT", default="5432"),  # noqa: F405
    }
}
