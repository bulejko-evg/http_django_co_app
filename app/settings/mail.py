from decouple import config

# SMTP
DEFAULT_EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = config("EMAIL_BACKEND", default=DEFAULT_EMAIL_BACKEND)
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config("EMAIL_PORT", default=25, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="??????@gmail.com")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST", default="***********")
EMAIL_ADMIN = "admin@mail.com"